let map = document.getElementById('map');
let tracking = document.getElementById('tracking');
let context = map.getContext('2d');

fetch('map.json')
    .then((result) => {
        return result.json()
    })
    .then((result) => {
        context.clearRect(0, 0, map.width, map.height);
        context.font = '12px sans-serif';
        context.lineWidth = 4;
        for (let [x, y, w, h, colour, outline] of result.rects) {
            context.fillStyle = colour;
            context.strokeStyle = outline;
            context.fillRect(x, y, w, h);
            console.log('rect %o %o %o %o', x, y, w, h);
        }
        for (let [x, y, text, colour] of result.text) {
            context.strokeStyle = context.fillStyle = colour;
            context.fillText(text, x, y);
        }
        tracking.textContent = result.tracked.map((x) => JSON.stringify(x) + '\n');
    });
