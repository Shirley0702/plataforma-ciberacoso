import AxeBuilder from '@axe-core/playwright'
import { expect, test, type Page } from '@playwright/test'


const demoPassword = process.env.E2E_DEMO_PASSWORD

async function expectAccessible(page: Page) {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze()
  expect(results.violations, JSON.stringify(results.violations, null, 2)).toEqual([])
}

async function followMainNavigation(page: Page, linkName: string) {
  const menuButton = page.getByRole('button', { name: 'Abrir menú' })
  if (await menuButton.isVisible()) await menuButton.click()
  await page.getByRole('link', { name: linkName, exact: true }).click()
}

test('protege el sistema y completa el recorrido diagnóstico personalizado', async ({ page }) => {
  test.skip(!demoPassword, 'Define E2E_DEMO_PASSWORD para ejecutar el recorrido real.')

  await page.goto('/')
  await expect(page).toHaveURL(/\/acceso$/)
  await expect(page.getByRole('heading', { name: 'Inicia sesión' })).toBeVisible()
  await expectAccessible(page)

  await page.getByLabel('Correo institucional').fill('demo')
  await page.locator('#password').fill(demoPassword as string)
  await page.getByRole('button', { name: 'Entrar a mi espacio' }).click()
  await expect(page).toHaveURL(/\/inicio$/)
  await expect(page.getByRole('heading', { level: 1 })).toContainText('Hola')

  await followMainNavigation(page, 'Evaluación')
  await expect(page).toHaveURL(/\/evaluacion$/)
  await expect(page.getByText('Escenario 1 de 8')).toBeVisible()
  await expectAccessible(page)

  for (let scenario = 1; scenario <= 8; scenario += 1) {
    await page.getByRole('radio').first().check()
    const buttonName = scenario === 8
      ? 'Generar mi curso personalizado'
      : 'Siguiente escenario'
    await page.getByRole('button', { name: buttonName }).click()
  }

  await expect(page).toHaveURL(/\/panel$/)
  await expect(page.getByRole('heading', { name: /Tu ruta recomendada:/ })).toBeVisible()
  await expectAccessible(page)

  await page.getByRole('link', { name: 'Comenzar mi curso personalizado' }).click()
  await expect(page).toHaveURL(/\/curso$/)
  await expect(page.getByRole('region', { name: 'Resumen del curso' })).toBeVisible()
  await expectAccessible(page)

  await followMainNavigation(page, 'Recursos')
  await expect(page).toHaveURL(/\/recursos$/)
  await expect(page.getByRole('heading', { name: 'Recursos oficiales' })).toBeVisible()
  await expectAccessible(page)

  await followMainNavigation(page, 'Tu Opinión')
  await expect(page).toHaveURL(/\/opinion$/)
  await expect(page.getByRole('heading', { name: 'Cuéntanos cómo fue tu experiencia' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Guardar Mi Opinión' })).toBeVisible()
  await expectAccessible(page)
})
