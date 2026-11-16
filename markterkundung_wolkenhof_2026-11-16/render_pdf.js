// render_pdf.js – rendert markterkundung_wolkenhof.html zu PDF (Chromium/Playwright)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'markterkundung_wolkenhof.html'), { waitUntil: 'load' });
  await page.pdf({
    path: path.join(dir, 'markterkundung_wolkenhof.pdf'),
    preferCSSPageSize: true,
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="font-size:7px;width:100%;padding:0 12mm;color:#5b6b72;display:flex;justify-content:space-between;font-family:Arial"><span>Markterkundung Wolkenhof GmbH · Stand 16.11.2026 · Datenbasis Websuche</span><span>Seite <span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  await browser.close();
  console.log('pdf ok');
})();
