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
    background: radial-gradient(ellipse at center, #131b3a 0%, #0b1020 70%);
    font-family: -apple-system, "Segoe UI", sans-serif; color: #eaf1ff; }
  #scene { position: fixed; inset: 0; display: block; cursor: grab; }
  #scene:active { cursor: grabbing; }
  .card {
    position: absolute; top: 32px; left: 32px; z-index: 2;
    background: rgba(19, 27, 58, 0.55);
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    padding: 24px 32px; border-radius: 18px; max-width: 440px;
    box-shadow: 0 12px 40px rgba(0,0,0,.55), inset 0 0 0 1px rgba(255,255,255,.05);
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
<script>
(function () {
  const canvas = document.getElementById('scene');
  const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(0, 0, 95);

  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.35));
  const lightCyan = new THREE.PointLight(0x22d3ee, 1.3, 260);
  lightCyan.position.set(50, 30, 60); scene.add(lightCyan);
  const lightPink = new THREE.PointLight(0xf472b6, 1.3, 260);
  lightPink.position.set(-50, -30, 60); scene.add(lightPink);
  const lightTop = new THREE.PointLight(0xffffff, 0.45, 220);
  lightTop.position.set(0, 80, 40); scene.add(lightTop);

  // DNA helix
  const dna = new THREE.Group();
  scene.add(dna);

  const N = 44;
  const radius = 9;
  const spacing = 1.9;
  const turns = 5;
  const totalAngle = turns * Math.PI * 2;
  const totalHeight = (N - 1) * spacing;

  const sphereGeo = new THREE.SphereGeometry(0.85, 24, 24);
  const cylGeo = new THREE.CylinderGeometry(0.18, 0.18, 1, 12);

  const matStrandA = new THREE.MeshStandardMaterial({
    color: 0x22d3ee, emissive: 0x0e7490, emissiveIntensity: 0.5,
    roughness: 0.25, metalness: 0.5
  });
  const matStrandB = new THREE.MeshStandardMaterial({
    color: 0xf472b6, emissive: 0xa21caf, emissiveIntensity: 0.5,
    roughness: 0.25, metalness: 0.5
  });

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

    const sA = new THREE.Mesh(sphereGeo, matStrandA);
    sA.position.copy(a); dna.add(sA);

    const sB = new THREE.Mesh(sphereGeo, matStrandB);
    sB.position.copy(b); dna.add(sB);

    // Rainbow base pair rung
    const hue = ((i / N) * 280 + 180) % 360;
    const baseColor = new THREE.Color().setHSL(hue / 360, 0.95, 0.62);
    const baseMat = new THREE.MeshStandardMaterial({
      color: baseColor, emissive: baseColor, emissiveIntensity: 0.85,
      roughness: 0.4, metalness: 0.2
    });
    const cyl = new THREE.Mesh(cylGeo, baseMat);
    const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
    cyl.position.copy(mid);
    const dir = new THREE.Vector3().subVectors(b, a);
    cyl.scale.y = dir.length();
    cyl.quaternion.setFromUnitVectors(yAxis, dir.clone().normalize());
    dna.add(cyl);
  }

  // Background stars
  const starsGeo = new THREE.BufferGeometry();
  const starCount = 600;
  const starPos = new Float32Array(starCount * 3);
  for (let i = 0; i < starCount; i++) {
    starPos[i * 3]     = (Math.random() - 0.5) * 400;
    starPos[i * 3 + 1] = (Math.random() - 0.5) * 400;
    starPos[i * 3 + 2] = (Math.random() - 0.5) * 400;
  }
  starsGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
  const starsMat = new THREE.PointsMaterial({
    color: 0xffffff, size: 0.5, transparent: true, opacity: 0.55, sizeAttenuation: true
  });
  scene.add(new THREE.Points(starsGeo, starsMat));

  // Controls
  const controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.autoRotate = true;
  controls.autoRotateSpeed = 0.6;
  controls.minDistance = 35;
  controls.maxDistance = 220;
  controls.enablePan = false;
  controls.target.set(0, 0, 0);

  // Resize
  window.addEventListener('resize', function () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // Animate
  const clock = new THREE.Clock();
  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    dna.position.y = Math.sin(t * 0.4) * 1.5;
    lightCyan.position.x = Math.cos(t * 0.3) * 60;
    lightCyan.position.z = Math.sin(t * 0.3) * 60;
    lightPink.position.x = Math.cos(t * 0.3 + Math.PI) * 60;
    lightPink.position.z = Math.sin(t * 0.3 + Math.PI) * 60;
    controls.update();
    renderer.render(scene, camera);
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
