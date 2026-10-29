from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import UserProfile
from .university_email import find_university
from .use_cases import generate_unique_username, issue_verification_code
from .validators import validate_birth_date, validate_full_name, validate_strong_password


User = get_user_model()
CODE_PATTERN = r"^\d{6}$"


class RegisterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        min_length=2,
        max_length=120,
        write_only=True,
        validators=[validate_full_name],
    )
    email = serializers.EmailField(max_length=254)
    birth_date = serializers.DateField(validators=[validate_birth_date])
    password = serializers.CharField(min_length=10, max_length=128, write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    accepted_terms = serializers.BooleanField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "birth_date",
            "password",
            "confirm_password",
            "full_name",
            "accepted_terms",
        )

    def validate_email(self, value):
        normalized = value.strip().lower()
        domain = normalized.rsplit("@", 1)[-1]
        if find_university(domain) is None:
            raise serializers.ValidationError(
                "El dominio no pertenece a una universidad reconocida. "
                "Utiliza el correo institucional asignado por tu universidad."
            )
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return normalized

    def validate_accepted_terms(self, value):
        if not value:
            raise serializers.ValidationError("Debes aceptar el aviso de uso orientativo.")
        return value

    def validate(self, attrs):
        password = attrs["password"]
        if password != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ["Las contraseñas no coinciden."]}
            )
        candidate = User(email=attrs["email"])
        try:
            validate_strong_password(password, user=candidate)
        except serializers.ValidationError as error:
            raise serializers.ValidationError({"password": error.detail}) from error
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        full_name = validated_data.pop("full_name")
        birth_date = validated_data.pop("birth_date")
        accepted_terms = validated_data.pop("accepted_terms")
        validated_data.pop("confirm_password")
        username = generate_unique_username(full_name, validated_data["email"])
        user = User.objects.create_user(
            username=username,
            **validated_data,
            is_active=False,
            is_staff=False,
            is_superuser=False,
        )
        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            birth_date=birth_date,
            accepted_terms_at=timezone.now() if accepted_terms else None,
        )
        issue_verification_code(user)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    code = serializers.RegexField(
        CODE_PATTERN,
        error_messages={"invalid": "Ingresa el código de 6 dígitos."},
    )

    def validate_email(self, value):
        return value.strip().lower()


class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)

    def validate_email(self, value):
        return value.strip().lower()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    university = serializers.SerializerMethodField()
    academic_program = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()

    def _profile_value(self, obj, field):
        profile = getattr(obj, "profile", None)
        return getattr(profile, field, "") if profile else ""

    def get_full_name(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.full_name if profile and profile.full_name else obj.username

    def get_birth_date(self, obj):
        birth_date = self._profile_value(obj, "birth_date")
        return birth_date.isoformat() if birth_date else None

    def get_age(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.age if profile else None

    def get_university(self, obj):
        return self._profile_value(obj, "university")

    def get_academic_program(self, obj):
        return self._profile_value(obj, "academic_program")

    def get_bio(self, obj):
        return self._profile_value(obj, "bio")

    def get_avatar_url(self, obj):
        profile = getattr(obj, "profile", None)
        return profile.avatar.url if profile and profile.avatar else ""


class ProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        min_length=2,
        max_length=120,
        validators=[validate_full_name],
    )
    birth_date = serializers.DateField(
        allow_null=True,
        required=False,
        validators=[validate_birth_date],
    )
    university = serializers.CharField(max_length=150, allow_blank=True, required=False)
    academic_program = serializers.CharField(max_length=150, allow_blank=True, required=False)
    bio = serializers.CharField(max_length=300, allow_blank=True, required=False)
    avatar = serializers.ImageField(write_only=True, required=False)
    remove_avatar = serializers.BooleanField(write_only=True, required=False, default=False)

    def validate_avatar(self, value):
        if value.size > 3 * 1024 * 1024:
            raise serializers.ValidationError("La fotografía no puede superar los 3 MB.")
        if value.content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise serializers.ValidationError("Utiliza una imagen JPG, PNG o WEBP.")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        profile, _ = UserProfile.objects.get_or_create(user=instance)
        new_avatar = validated_data.pop("avatar", None)
        remove_avatar = validated_data.pop("remove_avatar", False)
        for field, value in validated_data.items():
            setattr(profile, field, value.strip() if isinstance(value, str) else value)
        if (new_avatar or remove_avatar) and profile.avatar:
            profile.avatar.delete(save=False)
        if new_avatar:
            profile.avatar = new_avatar
        elif remove_avatar:
            profile.avatar = ""
        profile.save()
        return User.objects.select_related("profile").get(pk=instance.pk)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=10, max_length=128, write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("La contraseña actual no es correcta.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": ["Las contraseñas nuevas no coinciden."]}
            )
        if attrs["current_password"] == attrs["new_password"]:
            raise serializers.ValidationError(
                {"new_password": ["La contraseña nueva debe ser diferente a la actual."]}
            )
        try:
            validate_strong_password(
                attrs["new_password"],
                user=self.context["request"].user,
            )
        except serializers.ValidationError as error:
            raise serializers.ValidationError({"new_password": error.detail}) from error
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save(update_fields=("password",))
        return user
