const { chromium } = require('../.validation/node_modules/playwright');
const { default: AxeBuilder } = require('../.validation/node_modules/@axe-core/playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { pathToFileURL, fileURLToPath } = require('node:url');

(async () => {
  const root = path.resolve(__dirname, '..');
  const output = path.join(root, '.validation', 'results');
  fs.mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 1080 }, reducedMotion: 'reduce' });
  const page = await context.newPage();
  const errors = [];
  const remoteRequests = [];
  page.on('pageerror', error => errors.push(error.message));
  await context.route(/^https?:/, route => { remoteRequests.push(route.request().url()); return route.abort(); });
  const pages = ['index.html', 'noticias/apple.html', 'noticias/tesla.html', 'noticias/nvidia.html', 'creditos.html'];
  const report = [];
  try {
    for (const width of [1440, 768, 360]) {
      await page.setViewportSize({ width, height: 1080 });
      for (const filename of pages) {
        await page.goto(pathToFileURL(path.join(root, filename)).href);
        await page.evaluate(() => document.fonts.ready);
        await page.evaluate(() => document.querySelectorAll('img[loading="lazy"]').forEach(image => image.loading = 'eager'));
        await page.locator('footer').scrollIntoViewIfNeeded();
        await page.waitForFunction(() => [...document.images].every(image => image.complete));
        const images = await page.evaluate(() => [...document.images].every(image => image.naturalWidth > 0));
        assert(images, `Missing image: ${filename} at ${width}`);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Horizontal overflow: ${filename} at ${width}`);
        assert.equal(await page.locator('h1').count(), 1, `Single H1 in ${filename}`);
        assert(await page.evaluate(() => document.fonts.check('16px "Space Grotesk"') && document.fonts.check('16px "Source Sans 3"')), 'Fonts load');
        const links = await page.locator('a[href]').evaluateAll(elements => elements.map(element => element.href));
        for (const link of links) {
          if (!link.startsWith('file:')) continue;
          const url = new URL(link);
          const hash = decodeURIComponent(url.hash.slice(1));
          url.hash = '';
          const file = fileURLToPath(url);
          assert(fs.existsSync(file), `Missing local link: ${link}`);
          if (hash && file.endsWith('.html')) {
            const target = fs.readFileSync(file, 'utf8');
            assert(target.includes(`id="${hash}"`), `Missing anchor: ${link}`);
          }
        }
        await page.evaluate(() => scrollTo(0, 0));
        if (filename === 'index.html') {
          await page.screenshot({ path: path.join(output, `home-${width}.png`), fullPage: true });
          await page.screenshot({ path: path.join(output, `top-${width}.png`) });
          const geometry = await page.evaluate(() => {
            const hero = document.querySelector('.hero-section').getBoundingClientRect();
            const phones = [...document.querySelectorAll('.preview-phone')].map(p => p.getBoundingClientRect());
            const next = document.querySelector('.topic-intro a').getBoundingClientRect();
            return {overlap:Math.max(...phones.map(p=>p.bottom))-hero.bottom, clear:next.top>Math.max(...phones.map(p=>p.bottom))};
          });
          assert(geometry.overlap < 150 && geometry.overlap > -150, `Phone overlap at ${width}: ${JSON.stringify(geometry)}`);
          assert(geometry.clear, `Phone covers next section at ${width}`);
          for (const link of await page.locator('.phone-copy a').all()) {
            await link.scrollIntoViewIfNeeded();
            const clear = await link.evaluate(el => {
              const r = el.getBoundingClientRect();
              const top = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
              if (!top) return false;
              if (el.contains(top)) return true;
              return Boolean(top.closest('.preview-phone'));
            });
            assert(clear, `Phone link obstructed at ${width}`);
          }
        }
        if (filename === 'noticias/apple.html' && width === 1440) await page.screenshot({ path: path.join(output, 'apple-1440.png'), fullPage: true });
        const axe = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
        report.push({ page: filename, width, violations: axe.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => ({target:n.target, summary:n.failureSummary})) })) });
        console.log(`Checked ${filename} at ${width}px: ${axe.violations.length} accessibility violations`);
      }
    }
    await page.goto(pathToFileURL(path.join(root, 'index.html')).href);
    const visibleCards = page.locator('[data-news-card]:visible');
    assert.equal(await visibleCards.count(), 3);
    await page.locator('[data-filter="gaming"]').click();
    assert.equal(await visibleCards.count(), 1);
    await page.locator('#news-search').fill('apple');
    assert.equal(await visibleCards.count(), 0);
    await assert.doesNotReject(() => page.locator('#no-results').waitFor({state:'visible'}));
    await page.locator('#clear-query').click();
    assert.equal(await visibleCards.count(), 1, 'Clear query preserves gaming filter');
    assert.equal(await page.locator('[data-filter="gaming"]').getAttribute('aria-pressed'), 'true');
    assert(await page.locator('#clear-query').isHidden());
    await page.locator('#news-search').fill('apple');
    await page.locator('#clear-search').click();
    assert.equal(await visibleCards.count(), 3);
    await page.locator('#news-search').fill('INNOVACION');
    assert.equal(await visibleCards.count(), 1, 'Search ignores accents and case');
    await page.locator('#news-search').fill('  iPhone  ');
    assert.equal(await visibleCards.count(), 1, 'Search trims whitespace');
    await page.locator('#news-search').fill('');
    await page.locator('[data-filter="lanzamientos"]').click();
    assert.equal(await visibleCards.count(), 2);
    await page.locator('[data-filter="ia"]').click();
    assert.equal(await visibleCards.count(), 3);
    await page.locator('[data-filter="all"]').click();
    await page.locator('.menu-toggle').click();
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
    await page.locator('.menu-toggle').click();
    await page.locator('.site-nav a[href="#contacto"]').click();
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'), 'false');
    assert.equal(new URL(page.url()).hash, '#contacto');
    await page.locator('.header-search').click();
    assert(await page.locator('#news-search').evaluate(element => element === document.activeElement), 'Header search focuses input');
    await page.locator('.news-card h3 a').first().click();
    assert(page.url().endsWith('/noticias/apple.html'));
    await page.locator('.back-link').click();
    assert(new URL(page.url()).hash === '#noticias');
    await page.setViewportSize({ width:1440,height:1080 });
    await page.goto(pathToFileURL(path.join(root, 'index.html')).href);
    await page.emulateMedia({reducedMotion:'no-preference'});
    const preview = page.locator('.hero-preview');
    const box = await preview.boundingBox();
    await page.mouse.move(box.x + box.width*.8, box.y+box.height*.25);
    await page.waitForFunction(()=>parseFloat(document.querySelector('.hero-preview').style.getPropertyValue('--tilt-y'))>0);
    const tilt = await preview.evaluate(el=>[parseFloat(el.style.getPropertyValue('--tilt-x')),parseFloat(el.style.getPropertyValue('--tilt-y'))]);
    assert(tilt.every(v=>Math.abs(v)<=4));
    await page.mouse.move(10,10);
    await page.waitForFunction(()=>document.querySelector('.hero-preview').style.getPropertyValue('--tilt-y')==='0deg');
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.mouse.move(box.x+box.width*.8,box.y+box.height*.25);
    assert.equal(await preview.evaluate(el=>el.style.getPropertyValue('--tilt-y')), '0deg');
    assert.equal(errors.length, 0, `JavaScript errors: ${errors}`);
    assert.equal(remoteRequests.length, 0, `Unexpected internet requests: ${remoteRequests}`);
    fs.writeFileSync(path.join(output, 'report.json'), JSON.stringify({ report, errors, remoteRequests, interactions:'passed' }, null, 2));
    assert(report.every(row => row.violations.length === 0), 'Accessibility violations: see .validation/results/report.json');
    console.log('PASS: 15 responsive/offline checks, local links, image and font loading, filters, search, mobile menu, article navigation, 0 JS errors, 0 external requests.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
