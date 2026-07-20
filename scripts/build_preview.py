#!/usr/bin/env python3
"""Build a self-contained neon preview.html by inlining every generated SVG."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "assets"


def g(n): return (A / n).read_text()


def main():
    port, card, heat = g("avi-ascii.svg"), g("info-card.svg"), g("contrib-heatmap.svg")
    tech, wave, impact = g("tech-stack.svg"), g("wave.svg"), g("impact.svg")
    snake, streak = g("snake.svg"), g("streak.svg")
    badges = "".join(
        f'<span style="--c:{c}">{t}</span>' for t, c in [
            ("Python", "#3776AB"), ("Django", "#092E20"), ("FastAPI", "#009688"),
            ("AWS Bedrock", "#FF9900"), ("Docker", "#2496ED"), ("PostgreSQL", "#4169E1"),
            ("TensorFlow", "#FF6F00"), ("Jenkins", "#D24939"), ("GitHub Actions", "#2088FF"),
            ("OpenCV", "#5C3EE8"), ("Linux", "#FCC624"), ("Git", "#F05032")])
    socials = "".join(
        f'<span style="--c:{c}">{t}</span>' for t, c in [
            ("Portfolio ↗ akarshit-portfolio.netlify.app", "#39FF14"),
            ("Code ↗ codebyakarshit.netlify.app", "#00E5FF"),
            ("LinkedIn", "#0A66C2"), ("Email", "#EA4335"), ("Instagram", "#E4405F")])

    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Akarshit Bansal — neon profile preview</title>
<style>
 :root{{--bg:#05070d;--fg:#c9f7e8;--dim:#6f8ea0;--green:#39ff14;--cyan:#00e5ff;--mag:#ff2bd6;}}
 *{{box-sizing:border-box}}
 body{{margin:0;color:var(--fg);min-height:100vh;padding:0 0 60px;
   font-family:'JetBrains Mono',ui-monospace,Consolas,monospace;
   background:radial-gradient(900px 500px at 50% -8%,#0c1a1e,transparent),
     radial-gradient(700px 500px at 90% 20%,#1a0a1e,transparent),linear-gradient(#05070d,#05070d);}}
 body::before{{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
   background-image:linear-gradient(#0affce0a 1px,transparent 1px),linear-gradient(90deg,#0affce0a 1px,transparent 1px);
   background-size:34px 34px;mask:radial-gradient(circle at 50% 30%,#000,transparent 80%)}}
 .wrap{{max-width:1000px;margin:0 auto;position:relative;z-index:1;padding:30px 16px 0}}
 h1{{text-align:center;font-size:30px;margin:8px 0 2px;font-weight:800;letter-spacing:1px;
   background:linear-gradient(90deg,var(--cyan),var(--green),var(--mag));
   -webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 14px #00e5ff55)}}
 .tag{{text-align:center;color:var(--dim);font-size:13px;margin:0 0 6px}}
 .sub{{text-align:center;color:#5f7f72;font-size:12px;margin:0 0 20px}}
 .win{{border-radius:16px;overflow:hidden;position:relative;background:linear-gradient(#0a0f18,#070b12);
   border:1px solid #12303a;box-shadow:0 0 0 1px #0affce18,0 0 60px #00e5ff22,0 30px 80px #000a}}
 .bar{{display:flex;align-items:center;gap:8px;padding:12px 16px;background:#070b12;border-bottom:1px solid #12303a}}
 .dot{{width:12px;height:12px;border-radius:50%;box-shadow:0 0 8px currentColor}}
 .r{{background:#ff5f6d;color:#ff5f6d}}.y{{background:#ffcc33;color:#ffcc33}}.g{{background:#39ff14;color:#39ff14}}
 .bar .t{{margin-left:8px;color:var(--dim);font-size:12.5px}}
 .body{{padding:26px 22px 34px}}
 .prompt{{color:var(--green);margin:4px 2px 16px;font-size:14px;text-shadow:0 0 10px #39ff1466}}
 .prompt .u{{color:var(--cyan)}} .prompt .c{{color:var(--fg);text-shadow:none}}
 .cursor{{display:inline-block;width:8px;height:15px;background:var(--green);margin-left:4px;vertical-align:-2px;
   animation:bl 1s step-end infinite;box-shadow:0 0 8px #39ff14}}
 @keyframes bl{{50%{{opacity:0}}}}
 .row{{display:flex;flex-wrap:wrap;gap:22px;align-items:flex-start;justify-content:center}}
 .center{{display:flex;justify-content:center;margin-top:8px}}
 .center svg,.row svg{{max-width:100%;height:auto}}
 .mt{{margin-top:26px}} .mt2{{margin-top:14px}}
 .divider{{display:flex;justify-content:center;margin:22px 0}}
 .badges{{text-align:center;margin-top:26px;line-height:2.4}}
 .badges span{{display:inline-block;padding:6px 13px;margin:4px;border-radius:7px;font-size:12px;font-weight:700;
   color:#eaffff;background:color-mix(in srgb,var(--c) 22%,#0a0f18);border:1px solid var(--c);
   box-shadow:0 0 12px color-mix(in srgb,var(--c) 45%,transparent)}}
 .foot{{text-align:center;color:var(--dim);font-size:12px;margin:26px auto 0;max-width:900px;line-height:1.7}}
 .lbl{{text-align:center;color:#5f7f72;font-size:11px;letter-spacing:2px;margin:22px 0 8px}}
</style></head>
<body><div class="wrap">
 <h1>&lt; AKARSHIT BANSAL /&gt;</h1>
 <p class="tag">Python Developer · Backend &amp; Full-Stack @ Mittal Books · Delhi, India</p>
 <p class="sub">neon preview · portrait rendered from your photo · heatmap/snake/streak use sample data until the first GitHub Action run</p>
 <div class="win">
  <div class="bar"><span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
    <span class="t">akarshit@mittalbooks: ~/profile — zsh</span></div>
  <div class="body">
    <div class="prompt"><span class="u">~/akarshit</span> $ <span class="c">./whoami --animated</span><span class="cursor"></span></div>
    <div class="row">
      <div style="flex:0 0 auto;max-width:330px">{port}</div>
      <div style="flex:0 0 auto;max-width:560px">{card}</div>
    </div>
    <div class="divider">{wave}</div>
    <div class="lbl">// TECH STACK</div>
    <div class="center">{tech}</div>
    <div class="center mt">{impact}</div>
    <div class="divider">{wave}</div>
    <div class="prompt mt2"><span class="u">~/akarshit</span> $ <span class="c">git log --graph --contributions</span></div>
    <div class="center">{heat}</div>
    <div class="lbl">// SNAKE EATING THE GRAPH</div>
    <div class="center">{snake}</div>
    <div class="center mt">{streak}</div>
    <div class="badges">{badges}</div>
    <div class="divider">{wave}</div>
    <div class="badges">{socials}</div>
  </div>
 </div>
 <p class="foot">Faithful preview of the layout GitHub will render — every SVG auto-plays on load (refresh to replay). On the live profile the heatmap, snake and streak are built from your real contribution graph and refresh daily; the tech badges become clickable shields with logos.</p>
</div></body></html>"""
    (ROOT / "preview.html").write_text(html, encoding="utf-8")
    print("wrote preview.html", len(html), "bytes")


if __name__ == "__main__":
    main()
