from flask import Flask

app = Flask(__name__)

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cloud Engineering Demo - Naim</title>
<style>
  html, body { margin: 0; padding: 0; height: 100%; overflow: hidden;
    background: #040816;
    font-family: -apple-system, "Segoe UI", sans-serif; color: #eaf1ff; }
  #scene { position: fixed; inset: 0; display: block; cursor: grab; }
  #scene:active { cursor: grabbing; }
  .card {
    position: absolute; top: 32px; left: 32px; z-index: 2;
    background: rgba(10, 14, 32, 0.55);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    padding: 24px 32px; border-radius: 18px; max-width: 440px;
    box-shadow: 0 12px 40px rgba(0,0,0,.6), inset 0 0 0 1px rgba(255,255,255,.06);
  }
  h1 { font-weight: 600; margin: 0 0 6px; font-size: 22px; letter-spacing: -.01em; }
  p  { margin: 0; opacity: .68; font-size: 14px; line-height: 1.55; }
  .badge { display: inline-block; margin-top: 12px; padding: 4px 10px;
    border-radius: 999px; background: rgba(34, 211, 238, 0.15);
    color: #22d3ee; font-size: 11px; font-weight: 600;
    letter-spacing: .04em; text-transform: uppercase; }
  .hint { position: absolute; bottom: 22px; left: 0; right: 0;
    text-align: center; font-size: 12px; opacity: .35;
    z-index: 2; pointer-events: none; letter-spacing: .04em; }
</style>
</head>
<body>
<canvas id="scene"></canvas>
<div class="card">
  <h1>Hello Naim, welcome to my cloud engineering demo.</h1>
  <p>Deployed by Sinartisis Cloud Engineer on Azure App Service.</p>
  <span class="badge">DNA &middot; Pharma &middot; WebGL</span>
</div>
<div class="hint">drag to rotate &middot; scroll to zoom</div>

<script src="https://unpkg.com/three@0.128.0/build/three.min.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
<script src="https://unpkg.com/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>
<script>
(function () {
  const canvas = document.getElementById('scene');
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x040816, 1);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(0, 0, 60);

  // Lights — soft fill + two coloured kickers that orbit slowly.
  scene.add(new THREE.AmbientLight(0xffffff, 0.25));
  const lightA = new THREE.PointLight(0x38bdf8, 1.2, 220);
  lightA.position.set(40, 30, 50); scene.add(lightA);
  const lightB = new THREE.PointLight(0xec4899, 1.2, 220);
  lightB.position.set(-40, -30, 50); scene.add(lightB);
  const lightTop = new THREE.PointLight(0xffffff, 0.5, 220);
  lightTop.position.set(0, 80, 30); scene.add(lightTop);

  // 4-colour DNA base palette (A·T·G·C vibe).
  const basePalette = [
    new THREE.Color(0xec4899), // pink   (A)
    new THREE.Color(0xfde047), // yellow (T)
    new THREE.Color(0x22c55e), // green  (G)
    new THREE.Color(0x38bdf8), // blue   (C)
  ];

  // DNA helix
  const dna = new THREE.Group();
  scene.add(dna);

  const N = 30;
  const radius = 6;
  const spacing = 2.2;
  const turns = 3.5;
  const totalAngle = turns * Math.PI * 2;
  const totalHeight = (N - 1) * spacing;

  const sphereGeo = new THREE.SphereGeometry(1.4, 28, 28);
  const cylGeo = new THREE.CylinderGeometry(0.32, 0.32, 1, 14, 1, true);
  const yAxis = new THREE.Vector3(0, 1, 0);

  for (let i = 0; i < N; i++) {
    const t = i / (N - 1);
    const angle = t * totalAngle;
    const y = i * spacing - totalHeight / 2;

    const xA = Math.cos(angle) * radius;
    const zA = Math.sin(angle) * radius;
    const xB = Math.cos(angle + Math.PI) * radius;
    const zB = Math.sin(angle + Math.PI) * radius;

    const a = new THREE.Vector3(xA, y, zA);
    const b = new THREE.Vector3(xB, y, zB);

    const color = basePalette[i % basePalette.length];

    // Both backbone spheres share the rung's colour — that's what gives
    // the codepen reference its "candy bead" look once bloom is applied.
    const sphereMat = new THREE.MeshStandardMaterial({
      color: color, emissive: color, emissiveIntensity: 1.0,
      roughness: 0.28, metalness: 0.15
    });
    const sA = new THREE.Mesh(sphereGeo, sphereMat);
    sA.position.copy(a); dna.add(sA);

    const sB = new THREE.Mesh(sphereGeo, sphereMat);
    sB.position.copy(b); dna.add(sB);

    // Translucent glowing rung between the two beads.
    const rungMat = new THREE.MeshStandardMaterial({
      color: color, emissive: color, emissiveIntensity: 0.7,
      transparent: true, opacity: 0.55,
      roughness: 0.4, metalness: 0.05,
      side: THREE.DoubleSide
    });
    const cyl = new THREE.Mesh(cylGeo, rungMat);
    const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
    cyl.position.copy(mid);
    const dir = new THREE.Vector3().subVectors(b, a);
    cyl.scale.y = dir.length();
    cyl.quaternion.setFromUnitVectors(yAxis, dir.clone().normalize());
    dna.add(cyl);
  }

  // Subtle distant starfield — small + faint so bloom doesn't blow it out.
  const starsGeo = new THREE.BufferGeometry();
  const starCount = 320;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    starPos[i * 3]     = (Math.random() - 0.5) * 600;
    starPos[i * 3 + 1] = (Math.random() - 0.5) * 600;
    starPos[i * 3 + 2] = (Math.random() - 0.5) * 600 - 150;
  }
  starsGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  const starsMat = new THREE.PointsMaterial({
    color: 0x6b7ca6, size: 0.35, transparent: true, opacity: 0.45, sizeAttenuation: true
  });
  scene.add(new THREE.Points(starsGeo, starsMat));

  // Controls
  const controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.55;
  controls.minDistance = 22;
  controls.maxDistance = 180;
  controls.enablePan = false;
  controls.target.set(0, 0, 0);

  // Post-processing pipeline (bloom is the killer effect).
  const renderPass = new THREE.RenderPass(scene, camera);
  const bloomPass = new THREE.UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    1.15,   // strength
    0.55,   // radius
    0.15    // threshold (low → almost everything bloomy contributes)
  );
  const composer = new THREE.EffectComposer(renderer);
  composer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  composer.setSize(window.innerWidth, window.innerHeight);
  composer.addPass(renderPass);
  composer.addPass(bloomPass);

  // Resize
  window.addEventListener('resize', function () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    bloomPass.setSize(window.innerWidth, window.innerHeight);
  });

  // Animate
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    dna.position.y = Math.sin(t * 0.4) * 1.2;
    lightA.position.x = Math.cos(t * 0.3) * 55;
    lightA.position.z = Math.sin(t * 0.3) * 55;
    lightB.position.x = Math.cos(t * 0.3 + Math.PI) * 55;
    lightB.position.z = Math.sin(t * 0.3 + Math.PI) * 55;
    controls.update();
    composer.render();
  }
  animate();
})();
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
