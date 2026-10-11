// Renders the meme caption to a transparent PNG for the vertical cut.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 260 } });
  await p.goto('file://' + path.join(__dirname, 'caption.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: path.join(__dirname, 'caption.png'), omitBackground: true });
  await b.close();
})();
