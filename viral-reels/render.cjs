// Renders one of the phone-native reels frame by frame with headless Chromium and pipes the frames into ffmpeg.
//   node viral-reels/render.cjs imessage                  -> viral-reels/out/imessage-silent.mp4 + imessage.cues.json
//   node viral-reels/render.cjs imessage --stills 1,4.5   -> viral-reels/out/stills/imessage-<sec>.png
// Then `python3 viral-reels/sfx.py imessage` lays the sound effects in and writes viral-reels/out/imessage.mp4.
// Needs Playwright (NODE_PATH="$(npm root -g)" works with a global install) and ffmpeg.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const [name, ...args] = process.argv.slice(2);
const page_ = path.join(__dirname, name || '', 'index.html');
if (!name || !fs.existsSync(page_)) { console.error('usage: node render.cjs <reel folder> [--stills t1,t2]'); process.exit(1); }
const OUT = path.join(__dirname, 'out');
const flag = f => { const i = args.indexOf(f); return i >= 0 ? args[i + 1] : null; };

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--font-render-hinting=none', '--force-color-profile=srgb'] });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + page_);
  await page.waitForFunction(() => window.READY === true);
  const { duration, cues } = await page.evaluate(() => ({ duration: window.DURATION, cues: window.CUES || [] }));
  const shot = async t => { await page.evaluate(x => window.render(x), t); return page.screenshot({ type: 'png' }); };

  if (flag('--stills')) {
    const dir = path.join(OUT, 'stills');
    fs.mkdirSync(dir, { recursive: true });
    for (const t of flag('--stills').split(',').map(Number)) fs.writeFileSync(path.join(dir, `${name}-${t.toFixed(2)}.png`), await shot(t));
  } else {
    fs.writeFileSync(path.join(OUT, `${name}.cues.json`), JSON.stringify({ duration, cues }));
    const file = path.join(OUT, `${name}-silent.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-colorspace', 'bt709',
      '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', file], { stdio: ['pipe', 'inherit', 'inherit'] });
    const done = new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exited ' + c)))));
    const n = Math.round(duration * FPS);
    for (let i = 0; i < n; i++) {
      const buf = await shot(i / FPS);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end();
    await done;
    console.log('wrote', file);
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
