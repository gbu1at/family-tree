// static/js/pan.js
let scale = 1;
let translateX = 0;
let translateY = 0;
const treeContainer = document.getElementById('treeContainer');
const treeWrapper = document.querySelector('.tree-wrapper');
const panStep = 50;
const zoomStep = 0.2;

// Функции панорамирования с ограничениями
function panUp() {
    const maxY = treeContainer.offsetHeight * scale - treeWrapper.offsetHeight;
    translateY = Math.min(translateY + panStep, maxY);
    updateTransform();
}

function panDown() {
    translateY = Math.max(translateY - panStep, 0);
    updateTransform();
}

function panLeft() {
    const maxX = treeContainer.offsetWidth * scale - treeWrapper.offsetWidth;
    translateX = Math.min(translateX + panStep, maxX);
    updateTransform();
}

function panRight() {
    translateX = Math.max(translateX - panStep, 0);
    updateTransform();
}

// Функции масштабирования с ограничениями
function zoomIn() {
    scale = Math.min(scale + zoomStep, 2);
    constrainViewport();
    updateTransform();
}

function zoomOut() {
    scale = Math.max(scale - zoomStep, 0.3);
    constrainViewport();
    updateTransform();
}

// Ограничение видимой области
function constrainViewport() {
    const maxX = Math.max(0, treeContainer.offsetWidth * scale - treeWrapper.offsetWidth);
    const maxY = Math.max(0, treeContainer.offsetHeight * scale - treeWrapper.offsetHeight);
    
    translateX = Math.min(Math.max(translateX, 0), maxX);
    translateY = Math.min(Math.max(translateY, 0), maxY);
}

function resetView() {
    scale = 1;
    translateX = 0;
    translateY = 0;
    updateTransform();
}

function updateTransform() {
    treeContainer.style.transform = `translate(${-translateX}px, ${-translateY}px) scale(${scale})`;
    refreshConnections();
}

// Обработка клавиатуры
document.addEventListener('keydown', function(e) {
    if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        switch(e.key) {
            case 'ArrowUp': e.preventDefault(); panUp(); break;
            case 'ArrowDown': e.preventDefault(); panDown(); break;
            case 'ArrowLeft': e.preventDefault(); panLeft(); break;
            case 'ArrowRight': e.preventDefault(); panRight(); break;
            case '+': case '=': e.preventDefault(); zoomIn(); break;
            case '-': e.preventDefault(); zoomOut(); break;
            case '0': e.preventDefault(); resetView(); break;
        }
    }
});

// Инициализация
updateTransform();
treeContainer.style.transition = 'transform 0.3s ease';