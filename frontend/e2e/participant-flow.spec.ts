import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'


const demoPassword = process.env.E2E_DEMO_PASSWORD

async function expectAccessible(page: Page) {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .exclude('.video-frame iframe')
    .analyze()
  expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([])
}

async function followMainNavigation(page: Page, linkName: string) {
  const menuButton = page.locator('button[aria-controls="navegacion-principal"]')
  if (await menuButton.isVisible()) {
    await menuButton.press('Enter')
    await expect(menuButton).toHaveAttribute('aria-expanded', 'true')
  }
  await page.getByRole('link', { name: linkName, exact: true }).click()
}

test('protege el sistema y completa el recorrido diagnóstico personalizado', async ({ page }) => {
  test.skip(!demoPassword, 'Define E2E_DEMO_PASSWORD para ejecutar el recorrido real.')

  await page.goto('/')
  await expect(page).toHaveURL(/\/acceso$/)
  await expect(page.getByRole('heading', { name: 'Inicia sesión' })).toBeVisible()
  await expectAccessible(page)

  await page.getByRole('link', { name: 'Crear una cuenta' }).click()
  await expect(page).toHaveURL(/\/registro$/)
  await expect(page.getByRole('heading', { name: 'Crea tu cuenta' })).toBeVisible()
  await expectAccessible(page)

  await page.evaluate(() => sessionStorage.setItem('cibersegura_pending_email', 'prueba@universidad.edu'))
  await page.goto('/verificar-correo')
  await expect(page.getByRole('heading', { name: 'Revisa tu correo' })).toBeVisible()
  await expectAccessible(page)
  await page.getByRole('link', { name: 'Cambiar correo' }).click()
  await page.getByRole('link', { name: 'Iniciar sesión' }).click()
  await expect(page).toHaveURL(/\/acceso$/)

  await page.getByLabel('Correo institucional').fill('demo')
  await page.locator('#password').fill(demoPassword as string)
  const authenticationResponse = page.waitForResponse((response) => (
    response.url().endsWith('/api/auth/token/')
      && response.request().method() === 'POST'
  ))
  await page.getByRole('button', { name: 'Entrar a mi espacio' }).click()
  expect((await authenticationResponse).status()).toBe(200)
  await expect(page).toHaveURL(/\/inicio$/, { timeout: 15_000 })
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Hola')

  await followMainNavigation(page, 'Evaluación')
  await expect(page).toHaveURL(/\/evaluacion$/)
  await expect(page.getByText('Escenario 1 de 16')).toBeVisible()
  await expectAccessible(page)

  for (let scenario = 1; scenario <= 16; scenario += 1) {
    await page.getByRole('radio').first().check()
    const buttonName = scenario === 16
      ? 'Generar mi curso personalizado'
      : 'Siguiente escenario'
    await page.getByRole('button', { name: buttonName }).click()
  }

  await expect(page).toHaveURL(/\/panel$/)
  await expect(page.getByRole('heading', {
    name: /Tu ruta preventiva está lista|Primera prioridad:|Prioridades principales:/,
  })).toBeVisible()
  await expectAccessible(page)

  await page.getByRole('link', { name: 'Comenzar mi curso personalizado' }).click()
  await expect(page).toHaveURL(/\/curso$/)
  await expect(page.locator('.sidebar')).toHaveClass(/sidebar-collapsed/)
  await expect(page.getByRole('navigation', { name: 'Unidades del curso' })).toBeVisible()
  await expect(page.getByRole('button', { name: /Unidad 1.*Disponible/ })).toBeVisible()
  await expect(page.getByRole('button', { name: /Unidad 2.*Bloqueada/ })).toBeDisabled()
  await expect(page.getByText(/Las actividades no solicitan nombres ni relatos personales/)).toBeVisible()
  await expect(page.locator('.learning-experience')).toHaveCount(1)
  await page.getByRole('button', { name: /Experiencia 1: Video:/ }).click()
  await expect(page.getByText('Video para aprender')).toBeVisible()
  await expect(page.locator('.course-page')).toHaveClass(/course-theme-/)
  await expect(page.locator('.video-frame iframe')).toHaveCount(1)
  await expect(page.getByText(/no se reproduce automáticamente/)).toBeVisible()
  await expect(page.getByRole('checkbox')).toHaveCount(0)
  await expect(page.getByText(/video visto hasta el final|mira el video hasta el final/)).toBeVisible()
  await expect(page.getByText(/resumen accesible/i)).toHaveCount(0)
  await expect(page.getByRole('navigation', { name: 'Progreso de la unidad' })).toBeVisible()
  await expect(page.getByRole('link', { name: 'Evaluar la plataforma' })).toHaveCount(0)
  await expectAccessible(page)

  await followMainNavigation(page, 'Recursos')
  await expect(page).toHaveURL(/\/recursos$/)
  await expect(page.getByRole('heading', { name: 'Recursos oficiales' })).toBeVisible()
  await expectAccessible(page)

})
