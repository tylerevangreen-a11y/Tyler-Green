// Renders the transparent PNG overlays used by compose.sh (caption + end lower third).
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  for (const [name, h] of [['caption', 260], ['lowerthird', 230]]) {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    await p.goto('file://' + path.join(__dirname, name + '.html'));
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(__dirname, name + '.png'), omitBackground: true });
    await p.close();
  }
  await b.close();
})();
