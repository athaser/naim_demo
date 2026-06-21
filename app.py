from flask import Flask

app = Flask(__name__)

# DNA animation technique adapted from Amit Sheen's "DNA of CSS" pen
# (https://codepen.io/amit_sheen/pen/VwPojrm) — pure CSS 3D, no JS.
HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cloud Engineering Demo - Naim</title>
<style>
  *, *::before, *::after { padding: 0; margin: 0 auto; box-sizing: border-box; }

  body {
    background-color: #0a0d18;
    color: #eaf1ff;
    min-height: 100vh;
    overflow: hidden;
    font-family: -apple-system, "Segoe UI", sans-serif;
  }

  .stage {
    position: fixed; inset: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: clamp(14px, 1.4vw, 22px);
    perspective: 20em;
  }

  .dna {
    position: relative;
    transform: rotate(15deg);
    transform-style: preserve-3d;
  }

  .link {
    margin: 1em auto;
    width: 10em;
    height: 1em;
    transform-style: preserve-3d;
    animation: linkY 15s infinite linear;
    animation-delay: var(--iad);
  }

  /* Stagger each rung's start so they form a helix. 24 links · 15s loop. */
  .link:nth-child(1)  { --iad:   0s;    }
  .link:nth-child(2)  { --iad:  -0.625s;}
  .link:nth-child(3)  { --iad:  -1.25s; }
  .link:nth-child(4)  { --iad:  -1.875s;}
  .link:nth-child(5)  { --iad:  -2.5s;  }
  .link:nth-child(6)  { --iad:  -3.125s;}
  .link:nth-child(7)  { --iad:  -3.75s; }
  .link:nth-child(8)  { --iad:  -4.375s;}
  .link:nth-child(9)  { --iad:  -5s;    }
  .link:nth-child(10) { --iad:  -5.625s;}
  .link:nth-child(11) { --iad:  -6.25s; }
  .link:nth-child(12) { --iad:  -6.875s;}
  .link:nth-child(13) { --iad:  -7.5s;  }
  .link:nth-child(14) { --iad:  -8.125s;}
  .link:nth-child(15) { --iad:  -8.75s; }
  .link:nth-child(16) { --iad:  -9.375s;}
  .link:nth-child(17) { --iad: -10s;    }
  .link:nth-child(18) { --iad: -10.625s;}
  .link:nth-child(19) { --iad: -11.25s; }
  .link:nth-child(20) { --iad: -11.875s;}
  .link:nth-child(21) { --iad: -12.5s;  }
  .link:nth-child(22) { --iad: -13.125s;}
  .link:nth-child(23) { --iad: -13.75s; }
  .link:nth-child(24) { --iad: -14.375s;}

  /* 4-colour rotating palette — picked to suggest A/T/G/C nucleobases. */
  .link:nth-child(4n+1) { --clr1: hsl( 60, 100%, 75%); --clr2: hsl(240, 100%, 75%); }
  .link:nth-child(4n+2) { --clr1: hsl(150, 100%, 75%); --clr2: hsl(330, 100%, 75%); }
  .link:nth-child(4n+3) { --clr1: hsl(240, 100%, 75%); --clr2: hsl(420, 100%, 75%); }
  .link:nth-child(4n+4) { --clr1: hsl(330, 100%, 75%); --clr2: hsl(510, 100%, 75%); }

  /* Two nested divs form the translucent ribbon between the two beads. */
  .link > div {
    position: absolute; top: 0; left: 0;
    width: 100%; height: 100%;
    opacity: 0.5;
    background-image:
      radial-gradient(#000, #0000),
      linear-gradient(90deg, var(--clr1), var(--clr2));
    box-shadow: 0 0 0.5em #fff7;
    animation: linkX 7.5s infinite linear reverse;
  }
  .link > div:nth-child(1) { animation-delay: calc(var(--iad) + 0s); }
  .link > div:nth-child(2) { animation-delay: calc(var(--iad) + -3.75s); }

  /* The two glowing beads at each end of a rung. */
  .link::before, .link::after {
    content: "";
    position: absolute;
    top: -0.5em;
    width: 2em; height: 2em;
    border-radius: 50%;
    animation: linkY 15s infinite linear reverse;
    animation-delay: inherit;
  }
  .link::before {
    left: -1.75em;
    box-shadow: 0 0 1em var(--clr1);
    background-image: radial-gradient(circle at 50% 25%, #fff, var(--clr1), #000 90%);
  }
  .link::after {
    right: -1.75em;
    box-shadow: 0 0 1em var(--clr2);
    background-image: radial-gradient(circle at 50% 25%, #fff, var(--clr2), #000 90%);
  }

  @keyframes linkY { 0% { transform: rotateY(0deg);   } 100% { transform: rotateY(360deg); } }
  @keyframes linkX { 0% { transform: rotateX(0deg);   } 100% { transform: rotateX(360deg); } }

  /* Overlay UI */
  .card {
    position: absolute; top: 32px; left: 32px; z-index: 2;
    background: rgba(10, 14, 32, 0.55);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    padding: 24px 32px; border-radius: 18px; max-width: 440px;
    box-shadow: 0 12px 40px rgba(0,0,0,.6), inset 0 0 0 1px rgba(255,255,255,.06);
    font-size: 16px;
  }
  .card h1 { font-weight: 600; margin: 0 0 6px; font-size: 22px; letter-spacing: -.01em; }
  .card p  { margin: 0; opacity: .68; font-size: 14px; line-height: 1.55; }
  .badge {
    display: inline-block; margin-top: 12px; padding: 4px 10px;
    border-radius: 999px; background: rgba(34, 211, 238, 0.15);
    color: #22d3ee; font-size: 11px; font-weight: 600;
    letter-spacing: .04em; text-transform: uppercase;
  }
  .hint {
    position: absolute; bottom: 22px; left: 0; right: 0;
    text-align: center; font-size: 12px; opacity: .35;
    z-index: 2; pointer-events: none; letter-spacing: .04em;
  }

  @media (prefers-reduced-motion: reduce) {
    .link, .link > div, .link::before, .link::after { animation: none !important; }
  }
</style>
</head>
<body>
<div class="stage">
  <div class="dna">
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
    <div class="link"><div></div><div></div></div>
  </div>
</div>
<div class="card">
  <h1>Hello Naim, welcome to my cloud engineering demo.</h1>
  <p>Deployed by Sinartisis Cloud Engineer on Azure App Service.</p>
  <span class="badge">DNA &middot; Pharma &middot; Pure CSS</span>
</div>
<div class="hint">animation by Amit Sheen &middot; deployed by Sinartisis Cloud Engineer</div>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
