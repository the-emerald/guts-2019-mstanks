let map = document.getElementById('map');
let tracking = document.getElementById('tracking');
let context = map.getContext('2d');
context.font = '12px sans-serif';
context.lineWidth = 4;
let data = null;
let ts = Date.now();

function update() {
    fetch('map.json')
        .then((result) => {
            return result.json()
        })
        .then((result) => {
            ts = Date.now();
            data = result;
            tracking.textContent = data.tracked.map((x) => JSON.stringify(x) + '\n');
        });
}

setInterval(update, 1000);

function render() {
    requestAnimationFrame(render);
    context.clearRect(0, 0, map.width, map.height);
    if (!data) {
        return;
    }
    const dt = (Date.now() - ts) / 1000;
    for (let [x, y, w, h, colour, outline, vx, vy] of data.rects) {
        context.fillStyle = colour;
        context.strokeStyle = outline;
        x += dt * vx;
        y += dt * vy;
        context.fillRect(x, y, w, h);
    }
    for (let [x, y, text, colour, vx, vy] of data.text) {
        context.strokeStyle = context.fillStyle = colour;
        x += dt * vx;
        y += dt * vy;
        context.fillText(text, x, y);
    }
}

requestAnimationFrame(render);
