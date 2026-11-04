// node render_html.js page.html 秒數 fps 輸出資料夾 —— 逐格呼叫 window.setT(t) 截圖成 PNG（1920×1080）
const path = require('path');
const { launch } = require(path.join(process.env.HOME, '.claude/skills/svg-audio-animation/scripts/common'));
const [page, dur, fps, out] = process.argv.slice(2);
(async () => {
  const b = await launch(); const p = await b.newPage();
  await p.setViewport({ width: 1920, height: 1080 });
  await p.goto('file://' + path.resolve(page)); await p.evaluateHandle('document.fonts.ready');
  const n = Math.round(dur * fps);
  for (let i = 0; i < n; i++) {
    await p.evaluate(t => window.setT(t), i / fps);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png` });
  }
  console.log('frames', n); await Promise.race([b.close(), new Promise(r => setTimeout(r, 5000))]); process.exit(0);
})();
