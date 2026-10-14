// Renders index.html frame-by-frame with headless Chromium and pipes the frames into ffmpeg.
//   node render.cjs                      -> out/coffeespot-fit-reel.mp4 (30 fps)
//   FPS=60 node render.cjs               -> 60 fps
//   node render.cjs --stills 1,4.5,9     -> out/stills/t-<sec>.png
//   node render.cjs --poster 23.2        -> out/poster.png
// Needs Playwright (NODE_PATH="$(npm root -g)" works with a global install) and ffmpeg.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = Number(process.env.FPS || 30);
const OUT = path.join(__dirname, 'out');
const args = process.argv.slice(2);
const flag = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : null; };

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  await page.waitForFunction(() => window.READY === true);
  const duration = await page.evaluate(() => window.DURATION);

  const shot = async t => { await page.evaluate(x => window.render(x), t); return page.screenshot({ type: 'png' }); };

  if (flag('--stills')) {
    const dir = path.join(OUT, 'stills');
    fs.mkdirSync(dir, { recursive: true });
    for (const t of flag('--stills').split(',').map(Number)) fs.writeFileSync(path.join(dir, `t-${t.toFixed(2)}.png`), await shot(t));
  } else if (flag('--poster')) {
    fs.writeFileSync(path.join(OUT, 'poster.png'), await shot(Number(flag('--poster'))));
  } else {
    const file = path.join(OUT, process.env.OUTNAME || 'coffeespot-fit-reel.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '15', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-colorspace', 'bt709',
      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', file], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exited ' + c)))));
    const n = Math.round(duration * FPS);
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      const buf = await shot(i / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % (FPS * 2) === 0) process.stdout.write(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s\n`);
    }
    ff.stdin.end();
    await done;
    console.log('wrote', file);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
