import { useEffect, useState, type ChangeEvent, type FormEvent } from 'react'
import { PasswordInput } from '../../auth/components/PasswordInput'
import { useAuth } from '../../auth/context/AuthContext'
import { calculateAge, EARLIEST_BIRTH_DATE, sanitizeFullName, TODAY_DATE } from '../../auth/registrationValidation'
import { api, getErrorMessage } from '../../../shared/api/httpClient'


interface ProfileForm {
  full_name: string
  birth_date: string
  university: string
  academic_program: string
  bio: string
}

const EMPTY_PASSWORD_FORM = {
  current_password: '',
  new_password: '',
  confirm_password: '',
}


export function AccountPage() {
  const { user, refreshUser } = useAuth()
  const [profile, setProfile] = useState<ProfileForm>({
    full_name: user?.full_name ?? '',
    birth_date: user?.birth_date ?? '',
    university: user?.university ?? '',
    academic_program: user?.academic_program ?? '',
    bio: user?.bio ?? '',
  })
  const [avatar, setAvatar] = useState<File | null>(null)
  const [removeAvatar, setRemoveAvatar] = useState(false)
  const [profileStatus, setProfileStatus] = useState({ error: '', success: '' })
  const [passwords, setPasswords] = useState(EMPTY_PASSWORD_FORM)
  const [passwordStatus, setPasswordStatus] = useState({ error: '', success: '' })
  const [savingProfile, setSavingProfile] = useState(false)
  const [savingPassword, setSavingPassword] = useState(false)
  const [previewUrl, setPreviewUrl] = useState(user?.avatar_url ?? '')
  const currentAge = calculateAge(profile.birth_date)

  useEffect(() => {
    if (!avatar) {
      setPreviewUrl(removeAvatar ? '' : (user?.avatar_url ?? ''))
      return
    }
    const temporaryUrl = URL.createObjectURL(avatar)
    setPreviewUrl(temporaryUrl)
    return () => URL.revokeObjectURL(temporaryUrl)
  }, [avatar, removeAvatar, user?.avatar_url])

  const updateProfile = (field: keyof ProfileForm, value: string) => {
    setProfile((current) => ({ ...current, [field]: value }))
    setProfileStatus({ error: '', success: '' })
  }

  const selectAvatar = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] ?? null
    if (file && file.size > 3 * 1024 * 1024) {
      setProfileStatus({ error: 'La fotografía no puede superar los 3 MB.', success: '' })
      event.target.value = ''
      return
    }
    setAvatar(file)
    setRemoveAvatar(false)
    setProfileStatus({ error: '', success: '' })
  }

  const saveProfile = async (event: FormEvent) => {
    event.preventDefault()
    setProfileStatus({ error: '', success: '' })
    if (profile.full_name.trim().split(/\s+/).length < 2) {
      setProfileStatus({ error: 'Ingresa al menos un nombre y un apellido.', success: '' })
      return
    }
    const payload = new FormData()
    Object.entries(profile).forEach(([field, value]) => payload.append(field, value.trim()))
    if (avatar) payload.append('avatar', avatar)
    payload.append('remove_avatar', String(removeAvatar))
    setSavingProfile(true)
    try {
      await api.patch('/users/profile/', payload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      await refreshUser()
      setAvatar(null)
      setRemoveAvatar(false)
      setProfileStatus({ error: '', success: 'Tu información se actualizó correctamente.' })
    } catch (error) {
      setProfileStatus({ error: getErrorMessage(error), success: '' })
    } finally {
      setSavingProfile(false)
    }
  }

  const changePassword = async (event: FormEvent) => {
    event.preventDefault()
    setPasswordStatus({ error: '', success: '' })
    if (passwords.new_password !== passwords.confirm_password) {
      setPasswordStatus({ error: 'Las contraseñas nuevas no coinciden.', success: '' })
      return
    }
    setSavingPassword(true)
    try {
      const { data } = await api.post<{ detail: string }>('/users/password/', passwords)
      setPasswords(EMPTY_PASSWORD_FORM)
      setPasswordStatus({ error: '', success: data.detail })
    } catch (error) {
      setPasswordStatus({ error: getErrorMessage(error), success: '' })
    } finally {
      setSavingPassword(false)
    }
  }

  return (
    <div className="page-wrap account-page">
      <header className="page-header account-header">
        <div>
          <span className="eyebrow">Configuración Personal</span>
          <h1>Mi Cuenta</h1>
          <p>Actualiza tu información, tu fotografía y la seguridad de tu acceso.</p>
        </div>
      </header>

      <section className="account-card" aria-labelledby="profile-heading">
        <div className="account-card-heading">
          <div>
            <h2 id="profile-heading">Información Personal</h2>
            <p>El correo institucional y el usuario interno no pueden modificarse.</p>
          </div>
          <div className="profile-photo-preview">
            {previewUrl
              ? <img src={previewUrl} alt="Vista previa de la fotografía de perfil" />
              : <span aria-hidden="true">{profile.full_name.charAt(0).toUpperCase() || 'U'}</span>}
          </div>
        </div>

        {profileStatus.error && <div className="alert alert-danger" role="alert">{profileStatus.error}</div>}
        {profileStatus.success && <div className="alert alert-success" role="status">{profileStatus.success}</div>}

        <form onSubmit={saveProfile}>
          <div className="account-form-grid">
            <div>
              <label className="form-label" htmlFor="account-full-name">Nombre Completo</label>
              <input id="account-full-name" className="form-control" maxLength={120} value={profile.full_name} onChange={(event) => updateProfile('full_name', sanitizeFullName(event.target.value))} required />
            </div>
            <div>
              <label className="form-label" htmlFor="account-email">Correo Institucional</label>
              <input id="account-email" className="form-control" value={user?.email ?? ''} readOnly disabled />
            </div>
            <div>
              <label className="form-label" htmlFor="account-university">Universidad</label>
              <input id="account-university" className="form-control" maxLength={150} value={profile.university} onChange={(event) => updateProfile('university', event.target.value)} />
            </div>
            <div>
              <label className="form-label" htmlFor="account-program">Carrera o Programa Académico</label>
              <input id="account-program" className="form-control" maxLength={150} value={profile.academic_program} onChange={(event) => updateProfile('academic_program', event.target.value)} />
            </div>
            <div>
              <label className="form-label" htmlFor="account-birth-date">Fecha de Nacimiento</label>
              <input id="account-birth-date" className="form-control" type="date" min={EARLIEST_BIRTH_DATE} max={TODAY_DATE} value={profile.birth_date} onChange={(event) => updateProfile('birth_date', event.target.value)} required />
            </div>
            <div>
              <label className="form-label" htmlFor="account-age">Edad Actual</label>
              <input id="account-age" className="form-control" value={currentAge === null ? 'Se calculará automáticamente' : `${currentAge} años`} readOnly disabled />
            </div>
            <div>
              <label className="form-label" htmlFor="account-avatar">Fotografía de Perfil</label>
              <input id="account-avatar" className="form-control" type="file" accept="image/jpeg,image/png,image/webp" onChange={selectAvatar} />
              <div className="form-text">JPG, PNG o WEBP. Tamaño máximo: 3 MB.</div>
              {(user?.avatar_url || avatar) && (
                <button className="btn btn-link remove-photo-button" type="button" onClick={() => { setAvatar(null); setRemoveAvatar(true) }}>
                  Quitar Fotografía
                </button>
              )}
            </div>
            <div className="account-form-full">
              <label className="form-label" htmlFor="account-bio">Acerca de Mí</label>
              <textarea id="account-bio" className="form-control" rows={4} maxLength={300} value={profile.bio} onChange={(event) => updateProfile('bio', event.target.value)} />
              <div className="form-text">{profile.bio.length}/300 caracteres</div>
            </div>
          </div>
          <button className="btn btn-primary mt-4" type="submit" disabled={savingProfile}>
            {savingProfile ? 'Guardando…' : 'Guardar Cambios'}
          </button>
        </form>
      </section>

      <section className="account-card" aria-labelledby="password-heading">
        <h2 id="password-heading">Cambiar Contraseña</h2>
        <p>Confirma tu contraseña actual antes de establecer una nueva.</p>
        {passwordStatus.error && <div className="alert alert-danger" role="alert">{passwordStatus.error}</div>}
        {passwordStatus.success && <div className="alert alert-success" role="status">{passwordStatus.success}</div>}
        <form onSubmit={changePassword}>
          <div className="account-form-grid">
            <div className="account-form-full">
              <label className="form-label" htmlFor="current-password">Contraseña Actual</label>
              <PasswordInput id="current-password" className="form-control" autoComplete="current-password" value={passwords.current_password} onChange={(event) => setPasswords((current) => ({ ...current, current_password: event.target.value }))} required />
            </div>
            <div>
              <label className="form-label" htmlFor="new-password">Nueva Contraseña</label>
              <PasswordInput id="new-password" className="form-control" minLength={10} maxLength={128} autoComplete="new-password" value={passwords.new_password} onChange={(event) => setPasswords((current) => ({ ...current, new_password: event.target.value }))} required />
            </div>
            <div>
              <label className="form-label" htmlFor="confirm-new-password">Confirmar Nueva Contraseña</label>
              <PasswordInput id="confirm-new-password" className="form-control" autoComplete="new-password" value={passwords.confirm_password} onChange={(event) => setPasswords((current) => ({ ...current, confirm_password: event.target.value }))} required />
            </div>
          </div>
          <div className="form-text mt-2">Mínimo 10 caracteres, con mayúscula, minúscula, número y símbolo.</div>
          <button className="btn btn-primary mt-4" type="submit" disabled={savingPassword}>
            {savingPassword ? 'Actualizando…' : 'Actualizar Contraseña'}
          </button>
        </form>
      </section>
    </div>
  )
}
