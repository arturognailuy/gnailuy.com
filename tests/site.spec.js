const { test, expect } = require('@playwright/test');

test('home and primary navigation are responsive', async ({ page }, testInfo) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Blog posts' })).toBeVisible();
  await expect(page.getByRole('navigation', { name: 'Primary navigation' })).toBeVisible();
  await expect(page.locator('.post-card')).toHaveCount(71);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
  await page.screenshot({ path: testInfo.outputPath('home.png'), fullPage: true });
});

test('archive reaches a preserved post URL', async ({ page }, testInfo) => {
  await page.goto('/archive/');
  const link = page.getByRole('link', { name: 'Accept imperfectness' });
  await expect(link).toHaveAttribute('href', '/me/2024/03/17/imperfectness/');
  await link.click();
  await expect(page.getByRole('heading', { name: 'Accept imperfectness' })).toBeVisible();
  await expect(page.locator('main')).toContainText('accept imperfectness');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
  await page.screenshot({ path: testInfo.outputPath('post.png'), fullPage: true });
});
