// Scene, Camera, and Renderer Setup
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, -4, 4);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
container.appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const pointLight = new THREE.PointLight(0x00ffcc, 1.5, 50);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// Helper for Parametric Geometry compatibility
function createParametricGeometry(func, slices, stacks) {
    if (typeof THREE.ParametricGeometry !== 'undefined') {
        return new THREE.ParametricGeometry(func, slices, stacks);
    }
    if (typeof THREE.ParametricBufferGeometry !== 'undefined') {
        return new THREE.ParametricBufferGeometry(func, slices, stacks);
    }
    const geometry = new THREE.BufferGeometry();
    const vertices = [];
    const indices = [];
    const p = new THREE.Vector3();

    for (let i = 0; i <= stacks; i++) {
        const u = i / stacks;
        for (let j = 0; j <= slices; j++) {
            const v = j / slices;
            func(u, v, p);
            vertices.push(p.x, p.y, p.z);
        }
    }

    for (let i = 0; i < stacks; i++) {
        for (let j = 0; j < slices; j++) {
            const a = i * (slices + 1) + j;
            const b = i * (slices + 1) + j + 1;
            const c = (i + 1) * (slices + 1) + j;
            const d = (i + 1) * (slices + 1) + j + 1;
            indices.push(a, b, d);
            indices.push(a, d, c);
        }
    }

    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();
    return geometry;
}

// Toroidal Geometry Generation Function
let R_major = 2.0;
let r_minor = 0.8;
let mesh;

function createToroidalMesh(densityFactor, timeMod) {
    if (mesh) scene.remove(mesh);

    // Parametric surface geometry mapping complex impedance reflection to torus
    const geometry = createParametricGeometry((u, v, target) => {
        // u ranges from 0 to 2PI (poloidal), v ranges from 0 to 2PI (toroidal)
        const theta = u * Math.PI * 2;
        const phi = v * Math.PI * 2;

        // Dynamic modification of minor radius based on plenum density rho and phase t
        const dynamicR = r_minor * (1.0 + 0.15 * Math.sin(densityFactor * theta + timeMod));

        const x = (R_major + dynamicR * Math.cos(theta)) * Math.cos(phi);
        const y = (R_major + dynamicR * Math.cos(theta)) * Math.sin(phi);
        const z = dynamicR * Math.sin(theta);

        target.set(x, y, z);
    }, 60, 60);

    const material = new THREE.MeshStandardMaterial({
        color: 0x00aa88,
        wireframe: true,
        roughness: 0.3,
        metalness: 0.8,
        emissive: 0x002222
    });

    mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);
}

// Initial build
createToroidalMesh(1.0, 0.0);

// UI Controls Binding
const densitySlider = document.getElementById('densitySlider');
const freqSlider = document.getElementById('freqSlider');
const densityVal = document.getElementById('densityVal');
const freqVal = document.getElementById('freqVal');

densitySlider.addEventListener('input', (e) => {
    densityVal.textContent = e.target.value;
    updateScene();
});

freqSlider.addEventListener('input', (e) => {
    freqVal.textContent = e.target.value;
    updateScene();
});

function updateScene() {
    const rho = parseFloat(densitySlider.value);
    const t = parseFloat(freqSlider.value);
    createToroidalMesh(rho, t);
}

// Animation Loop for subtle rotation
let clock = new THREE.Clock();
function animate() {
    requestAnimationFrame(animate);
    
    if (mesh) {
        mesh.rotation.z += 0.002;
    }

    renderer.render(scene, camera);
}
animate();

// Window resizing handler
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
