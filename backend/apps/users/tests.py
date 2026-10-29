import os
import tempfile
from datetime import date, timedelta
from io import BytesIO, StringIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.management import call_command
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image

from .models import EmailVerification, UserProfile


User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class RoleAccessTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.demo = User.objects.create_user(
            username="demo",
            password="DemoSegura2026!",
            is_staff=False,
        )
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@cibersegura.local",
            password="AdminSegura2026!",
        )

    def test_private_routes_require_authentication(self):
        protected_routes = (
            "/api/users/dashboard/",
            "/api/users/profile/",
            "/api/diagnostics/questions/",
            "/api/courses/units/",
            "/api/resources/",
        )
        for route in protected_routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_demo_can_authenticate_in_educational_platform(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"identifier": "demo", "password": "DemoSegura2026!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_admin_cannot_authenticate_in_educational_platform(self):
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"identifier": "admin", "password": "AdminSegura2026!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_cannot_refresh_an_old_educational_token(self):
        refresh = RefreshToken.for_user(self.admin)
        response = self.client.post(
            reverse("token_refresh"),
            {"refresh": str(refresh)},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_cannot_use_educational_api(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/diagnostics/questions/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_admin_can_open_administration(self):
        self.client.force_authenticate(user=None)
        self.assertTrue(self.client.login(username="admin", password="AdminSegura2026!"))
        self.assertEqual(self.client.get("/admin/").status_code, status.HTTP_200_OK)
        self.client.logout()
        self.assertTrue(self.client.login(username="demo", password="DemoSegura2026!"))
        self.assertEqual(self.client.get("/admin/").status_code, status.HTTP_302_FOUND)

    def test_registration_creates_a_non_administrative_participant(self):
        with patch(
            "apps.users.use_cases.email_verification.secrets.randbelow",
            return_value=42381,
        ):
            response = self.client.post(
                reverse("register"),
                {
                    "email": "participante@espe.edu.ec",
                    "password": "Clave-Nueva-9842!",
                    "confirm_password": "Clave-Nueva-9842!",
                    "full_name": "Participante Nueva",
                    "birth_date": "2000-01-01",
                    "accepted_terms": True,
                },
                format="json",
            )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        participant = User.objects.get(email="participante@espe.edu.ec")
        self.assertRegex(participant.username, r"^participante\.nueva\.[a-f0-9]{10}$")
        self.assertFalse(participant.is_active)
        self.assertFalse(participant.is_staff)
        self.assertFalse(participant.is_superuser)
        self.assertEqual(participant.profile.birth_date, date(2000, 1, 1))
        self.assertIn("042381", mail.outbox[0].body)

        login_before_verification = self.client.post(
            reverse("token_obtain_pair"),
            {
                "identifier": "participante@espe.edu.ec",
                "password": "Clave-Nueva-9842!",
            },
            format="json",
        )
        self.assertEqual(
            login_before_verification.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        invalid_verification = self.client.post(
            reverse("verify_email"),
            {"email": "participante@espe.edu.ec", "code": "000000"},
            format="json",
        )
        self.assertEqual(invalid_verification.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            EmailVerification.objects.get(user=participant).attempts,
            1,
        )

        verification = self.client.post(
            reverse("verify_email"),
            {"email": "participante@espe.edu.ec", "code": "042381"},
            format="json",
        )
        self.assertEqual(verification.status_code, status.HTTP_200_OK)
        participant.refresh_from_db()
        self.assertTrue(participant.is_active)

        login = self.client.post(
            reverse("token_obtain_pair"),
            {
                "identifier": "participante@espe.edu.ec",
                "password": "Clave-Nueva-9842!",
            },
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.assertEqual(
            self.client.get("/api/diagnostics/questions/").status_code,
            status.HTTP_200_OK,
        )

    def test_registration_rejects_duplicate_email_ignoring_case(self):
        User.objects.create_user(
            username="existente",
            email="persona@espe.edu.ec",
            password="ExistenteSegura2026!",
        )
        response = self.client.post(
            reverse("register"),
            {
                "email": "PERSONA@ESPE.EDU.EC",
                "password": "OtraPersonaSegura2026!",
                "confirm_password": "OtraPersonaSegura2026!",
                "full_name": "Otra Persona",
                "birth_date": "2000-01-01",
                "accepted_terms": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_registration_requires_explicit_acceptance(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "sin-aceptar@espe.edu.ec",
                "password": "SinAceptarSegura2026!",
                "confirm_password": "SinAceptarSegura2026!",
                "full_name": "Sin Aceptar",
                "birth_date": "2000-01-01",
                "accepted_terms": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("accepted_terms", response.data)

    def test_registration_rejects_non_university_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "persona@gmail.com",
                "password": "Clave-Personal-9842!",
                "confirm_password": "Clave-Personal-9842!",
                "full_name": "Correo Personal",
                "birth_date": "2000-01-01",
                "accepted_terms": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_registration_requires_every_field(self):
        valid_payload = {
            "email": "campos@espe.edu.ec",
            "password": "Campos-Seguros-9842!",
            "confirm_password": "Campos-Seguros-9842!",
            "full_name": "Campos Obligatorios",
            "birth_date": "2000-01-01",
            "accepted_terms": True,
        }
        for field in valid_payload:
            with self.subTest(field=field):
                cache.clear()
                response = self.client.post(
                    reverse("register"),
                    {key: value for key, value in valid_payload.items() if key != field},
                    format="json",
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)

    def test_registration_rejects_incomplete_or_numeric_full_name(self):
        common_payload = {
            "password": "Nombre-Seguro-9842!",
            "confirm_password": "Nombre-Seguro-9842!",
            "birth_date": "2000-01-01",
            "accepted_terms": True,
        }
        incomplete = self.client.post(
            reverse("register"),
            {
                **common_payload,
                "email": "nombre-incompleto@espe.edu.ec",
                "full_name": "Shirley",
            },
            format="json",
        )
        numeric = self.client.post(
            reverse("register"),
            {
                **common_payload,
                "email": "nombre-numerico@espe.edu.ec",
                "full_name": "Shirley 2026",
            },
            format="json",
        )
        self.assertEqual(incomplete.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("full_name", incomplete.data)
        self.assertEqual(numeric.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("full_name", numeric.data)

    def test_registration_accepts_a_recognized_university_without_edu_suffix(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "estudiante@usm.cl",
                "password": "Universitaria-9842!",
                "confirm_password": "Universitaria-9842!",
                "full_name": "Estudiante Internacional",
                "birth_date": "2000-01-01",
                "accepted_terms": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(User.objects.get(email="estudiante@usm.cl").is_active)

    def test_registration_generates_different_usernames_for_equal_names(self):
        payload = {
            "password": "Ruta-Segura-9842!",
            "confirm_password": "Ruta-Segura-9842!",
            "full_name": "Nombre Repetido",
            "birth_date": "2000-01-01",
            "accepted_terms": True,
        }
        first = self.client.post(
            reverse("register"),
            {**payload, "email": "nombre-uno@espe.edu.ec"},
            format="json",
        )
        second = self.client.post(
            reverse("register"),
            {**payload, "email": "nombre-dos@espe.edu.ec"},
            format="json",
        )
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED)
        usernames = set(
            User.objects.filter(email__startswith="nombre-").values_list(
                "username", flat=True
            )
        )
        self.assertEqual(len(usernames), 2)

    def test_registration_rejects_weak_or_mismatched_password(self):
        weak = self.client.post(
            reverse("register"),
            {
                "email": "debil@espe.edu.ec",
                "password": "abcdefghij",
                "confirm_password": "abcdefghij",
                "full_name": "Clave Débil",
                "birth_date": "2000-01-01",
                "accepted_terms": True,
            },
            format="json",
        )
        self.assertEqual(weak.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", weak.data)

        mismatch = self.client.post(
            reverse("register"),
            {
                "email": "distinta@espe.edu.ec",
                "password": "Clave-Correcta-9842!",
                "confirm_password": "Clave-Diferente-9842!",
                "full_name": "Clave Distinta",
                "birth_date": "2000-01-01",
                "accepted_terms": True,
            },
            format="json",
        )
        self.assertEqual(mismatch.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("confirm_password", mismatch.data)


class AccountSynchronizationTests(APITestCase):
    def test_seed_preserves_registered_users_and_synchronizes_initial_roles(self):
        User.objects.create_user("participante-existente", password="Temporal2026!")
        environment = {
            "DEMO_USER_PASSWORD": "DemoSinPredecir2026!",
            "DEMO_ADMIN_PASSWORD": "AdminSinPredecir2026!",
        }
        with patch.dict(os.environ, environment):
            call_command("seed_initial_data", stdout=StringIO())

        self.assertEqual(
            set(User.objects.values_list("username", flat=True)),
            {"admin", "demo", "participante-existente"},
        )
        demo = User.objects.get(username="demo")
        admin = User.objects.get(username="admin")
        self.assertTrue(demo.is_active)
        self.assertFalse(demo.is_staff)
        self.assertFalse(demo.is_superuser)
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class ParticipantAccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="participante",
            email="participante@espe.edu.ec",
            password="Clave-Actual-9842!",
        )
        UserProfile.objects.create(user=self.user, full_name="Persona Participante")
        self.client.force_authenticate(self.user)

    def test_participant_can_update_optional_profile_information(self):
        response = self.client.patch(
            reverse("profile"),
            {
                "full_name": "Shirley Otuna",
                "university": "Universidad de las Fuerzas Armadas ESPE",
                "academic_program": "Ingeniería de Software",
                "birth_date": "2000-01-01",
                "bio": "Me interesa fortalecer la convivencia digital.",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.full_name, "Shirley Otuna")
        self.assertEqual(self.user.profile.birth_date, date(2000, 1, 1))
        self.assertEqual(response.data["age"], date.today().year - 2000)
        self.assertEqual(response.data["email"], "participante@espe.edu.ec")

    def test_profile_rejects_a_name_with_numbers(self):
        response = self.client.patch(
            reverse("profile"),
            {"full_name": "Shirley 2026"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("full_name", response.data)

    def test_profile_rejects_a_future_birth_date(self):
        response = self.client.patch(
            reverse("profile"),
            {"birth_date": (date.today() + timedelta(days=1)).isoformat()},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data)

    def test_participant_can_upload_a_profile_photo(self):
        with tempfile.TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
            image_bytes = BytesIO()
            Image.new("RGB", (20, 20), color="teal").save(image_bytes, format="PNG")
            avatar = SimpleUploadedFile(
                "avatar.png",
                image_bytes.getvalue(),
                content_type="image/png",
            )
            response = self.client.patch(
                reverse("profile"),
                {"avatar": avatar},
                format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("/media/profiles/avatars/", response.data["avatar_url"])

    def test_password_change_requires_the_current_password(self):
        response = self.client.post(
            reverse("password_change"),
            {
                "current_password": "Clave-Incorrecta-9842!",
                "new_password": "Clave-Nueva-5274!",
                "confirm_password": "Clave-Nueva-5274!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_password", response.data)

    def test_participant_can_change_password(self):
        response = self.client.post(
            reverse("password_change"),
            {
                "current_password": "Clave-Actual-9842!",
                "new_password": "Clave-Nueva-5274!",
                "confirm_password": "Clave-Nueva-5274!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("Clave-Nueva-5274!"))
