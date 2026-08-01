/*
  Emits book/folio-overlay.html — one 6x9in sheet per numbered page of the
  rebuilt book, carrying:
    - a silk patch that hides the original folio (pages that already had one)
    - the corrected folio, set to match the book: EB Garamond, 8.6pt,
      centred, baseline 28.8pt up from the foot of the page.

  The patch is an SVG rect, not a CSS background, so it survives
  printToPDF({printBackground:false}) — which is what keeps the rest of the
  overlay transparent when it is merged over the original pages.

  Usage: node book/make-folios.mjs <count>     (default 51)
*/
import { writeFileSync } from 'node:fs';

const COUNT = Number(process.argv[2] || 51);
const SILK = '#F8F4EC';

// Folio metrics read out of the original book with pypdf:
//   text baseline y = 28.8pt, centred on x ~= 216pt, EBGaramond-Medium 8.6pt
const BASELINE_PT = 28.8;
const SIZE_PT = 8.6;
// EB Garamond's baseline sits ~0.78em above the bottom of a line-height:1 box.
const BOX_BOTTOM_PT = (BASELINE_PT - SIZE_PT * 0.78).toFixed(2);

const sheets = Array.from({ length: COUNT }, (_, i) => {
  const n = i + 1;
  const last = i === COUNT - 1 ? ' last' : '';
  return `  <div class="sheet${last}">
    <svg class="patch" width="44" height="18" viewBox="0 0 44 18"><rect width="44" height="18" fill="${SILK}"/></svg>
    <div class="folio">${n}</div>
  </div>`;
}).join('\n');

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Folio overlay</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500&display=swap" rel="stylesheet">
<style>
  @page { size: 6in 9in; margin: 0; }
  *{ margin:0; padding:0; box-sizing:border-box; }
  html, body{ background:transparent; }
  .sheet{
    position:relative;
    width:6in; height:9in;
    page-break-after:always; break-after:page;
    overflow:hidden;
  }
  .sheet.last{ page-break-after:auto; break-after:auto; }
  /* Covers the original folio. Centred on x=216pt: 216 - 22 = 194pt. */
  .patch{ position:absolute; left:194pt; bottom:${(BASELINE_PT - 9).toFixed(2)}pt; }
  .folio{
    position:absolute; left:0; right:0; bottom:${BOX_BOTTOM_PT}pt;
    text-align:center; line-height:1;
    font-family:'EB Garamond', Georgia, serif; font-weight:500;
    font-size:${SIZE_PT}pt; color:#2B2723;
  }
</style>
</head>
<body>
${sheets}
</body>
</html>
`;

const out = new URL('./folio-overlay.html', import.meta.url);
writeFileSync(out, html);
console.log(`wrote folio-overlay.html with ${COUNT} sheets`);
