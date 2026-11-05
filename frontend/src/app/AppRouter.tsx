import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from '../features/auth/context/AuthContext'
import { ProtectedRoute } from '../features/auth/components/ProtectedRoute'
import { LoginPage } from '../features/auth/pages/LoginPage'
import { RegisterPage } from '../features/auth/pages/RegisterPage'
import { VerifyEmailPage } from '../features/auth/pages/VerifyEmailPage'
import { CoursePage } from '../features/course/pages/CoursePage'
import { DashboardPage } from '../features/dashboard/pages/DashboardPage'
import { DiagnosticPage } from '../features/diagnostic/pages/DiagnosticPage'
import { ResourcesPage } from '../features/resources/pages/ResourcesPage'
import { AccountPage } from '../features/account/pages/AccountPage'
import { HomePage } from '../features/home/pages/HomePage'
import { TextReviewPage } from '../features/textReview/pages/TextReviewPage'
import { ProductFeedbackPage } from '../features/productValidation/pages/ProductFeedbackPage'
import { AppShell } from './layout/AppShell'
import { NotFoundPage } from './pages/NotFoundPage'

export function AppRouter() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/acceso" replace />} />
          <Route path="/acceso" element={<LoginPage />} />
          <Route path="/registro" element={<RegisterPage />} />
          <Route path="/verificar-correo" element={<VerifyEmailPage />} />
          <Route element={<ProtectedRoute />}>
            <Route element={<AppShell />}>
              <Route path="/inicio" element={<HomePage />} />
              <Route path="/panel" element={<DashboardPage />} />
              <Route path="/evaluacion" element={<DiagnosticPage />} />
              <Route path="/revision-texto" element={<TextReviewPage />} />
              <Route path="/curso" element={<CoursePage />} />
              <Route path="/recursos" element={<ResourcesPage />} />
              <Route path="/evaluar-plataforma" element={<ProductFeedbackPage />} />
              <Route path="/mi-cuenta" element={<AccountPage />} />
            </Route>
          </Route>
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}
