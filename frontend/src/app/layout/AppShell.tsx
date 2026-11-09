import { useEffect, useRef, useState } from 'react'
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../features/auth/context/AuthContext'

const links = [
  { to: '/inicio', icon: '⌂', label: 'Inicio' },
  { to: '/evaluacion', icon: '✓', label: 'Evaluación' },
  { to: '/orientacion-privada', icon: '◫', label: 'Orientación Privada' },
  { to: '/panel', icon: '◇', label: 'Panel personalizado' },
  { to: '/curso', icon: '▤', label: 'Curso' },
  { to: '/recursos', icon: '+', label: 'Recursos' },
  { to: '/mi-cuenta', icon: '●', label: 'Mi Cuenta' },
]

const pageTitles: Record<string, string> = {
  '/inicio': 'Inicio',
  '/evaluacion': 'Evaluación',
  '/orientacion-privada': 'Orientación Privada',
  '/panel': 'Panel Personalizado',
  '/curso': 'Curso',
  '/recursos': 'Recursos',
  '/evaluar-plataforma': 'Evaluar la Plataforma',
  '/mi-cuenta': 'Mi Cuenta',
}

export function AppShell() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [courseMenuExpanded, setCourseMenuExpanded] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const mainContentRef = useRef<HTMLElement>(null)
  const isCoursePage = location.pathname === '/curso'
  const sidebarCollapsed = isCoursePage && !courseMenuExpanded

  useEffect(() => {
    const pageTitle = pageTitles[location.pathname] ?? 'CiberSegura'
    document.title = `${pageTitle} | CiberSegura`
    mainContentRef.current?.focus()
    setMenuOpen(false)
    setCourseMenuExpanded(false)
  }, [location.pathname])

  const handleLogout = async () => {
    await logout()
    navigate('/acceso')
  }

  return (
    <div className={`app-shell ${isCoursePage ? 'course-focus' : ''}`}>
      <a className="skip-link" href="#contenido-principal">Saltar al contenido</a>
      <header className="mobile-header">
        <NavLink className="brand" to="/inicio">
          <span className="brand-mark" aria-hidden="true">CS</span>
          <span>CiberSegura</span>
          <span className="visually-hidden">Ir al inicio</span>
        </NavLink>
        <button
          className="menu-button"
          type="button"
          aria-expanded={menuOpen}
          aria-controls="navegacion-principal"
          onClick={() => setMenuOpen((value) => !value)}
        >
          <span aria-hidden="true">☰</span>
          <span className="visually-hidden">{menuOpen ? 'Cerrar menú' : 'Abrir menú'}</span>
        </button>
      </header>

      <aside
        className={`sidebar ${menuOpen ? 'sidebar-open' : ''} ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}
        id="navegacion-principal"
      >
        <div className="sidebar-heading">
          <NavLink className="brand sidebar-brand" to="/inicio" onClick={() => setMenuOpen(false)}>
            <span className="brand-mark" aria-hidden="true">CS</span>
            <span className="brand-label">CiberSegura</span>
            <span className="visually-hidden">Ir al inicio de CiberSegura</span>
          </NavLink>
          {isCoursePage && (
            <button
              className="sidebar-collapse-button"
              type="button"
              aria-label={sidebarCollapsed ? 'Ampliar menú principal' : 'Retraer menú principal'}
              aria-expanded={!sidebarCollapsed}
              onClick={() => setCourseMenuExpanded((current) => !current)}
            >
              <span aria-hidden="true">{sidebarCollapsed ? '›' : '‹'}</span>
            </button>
          )}
        </div>
        <div className="sidebar-intro">
          <span className="eyebrow">Tu espacio</span>
          <strong>Aprende. Detecta. Actúa.</strong>
        </div>
        <nav aria-label="Navegación principal">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              title={sidebarCollapsed ? link.label : undefined}
              aria-label={sidebarCollapsed ? link.label : undefined}
              onClick={() => setMenuOpen(false)}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <span className="nav-icon" aria-hidden="true">{link.icon}</span>
              <span className="nav-label">{link.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <NavLink
            className="user-chip"
            to="/mi-cuenta"
            title={sidebarCollapsed ? user?.full_name : undefined}
            aria-label={sidebarCollapsed ? `Mi cuenta: ${user?.full_name}` : undefined}
            onClick={() => setMenuOpen(false)}
          >
            <span className="avatar">
              {user?.avatar_url
                ? <img src={user.avatar_url} alt="" />
                : <span aria-hidden="true">{user?.full_name?.charAt(0).toUpperCase() || 'U'}</span>}
            </span>
            <span>
              <small>Sesión de</small>
              <strong>{user?.full_name}</strong>
            </span>
          </NavLink>
          <button className="logout-button" type="button" aria-label="Cerrar sesión" onClick={() => void handleLogout()}>
            <span className="logout-icon" aria-hidden="true">↪</span>
            <span className="logout-label">Cerrar sesión</span>
          </button>
        </div>
      </aside>

      {menuOpen && <button className="menu-backdrop" type="button" aria-label="Cerrar menú" onClick={() => setMenuOpen(false)} />}

      <main ref={mainContentRef} id="contenido-principal" className="main-content" tabIndex={-1}>
        <Outlet />
      </main>
    </div>
  )
}
