// static/js/connections.js
let familyConnections = [];

async function loadFamilyConnections() {
    try {
        const response = await fetch('/api/family_connections');
        familyConnections = await response.json();
        updateConnections();
    } catch (error) {
        console.error('Ошибка загрузки связей:', error);
    }
}
function updateConnections() {
    const svg = document.getElementById('connectionsSVG');
    if (!svg) return;
    
    // Очищаем предыдущие линии
    svg.innerHTML = '';
    
    // Получаем текущую трансформацию контейнера
    const treeContainer = document.querySelector('.tree-container');
    const containerRect = treeContainer.getBoundingClientRect();
    const style = window.getComputedStyle(treeContainer);
    const matrix = new DOMMatrix(style.transform);
    const scale = matrix.a;
    const translateX = matrix.e;
    const translateY = matrix.f;
    
    // Создаем линии для каждой связи
    familyConnections.forEach(connection => {
        const fromNode = document.querySelector(`[data-person-id="${connection.from_id}"]`);
        const toNode = document.querySelector(`[data-person-id="${connection.to_id}"]`);
        
        if (fromNode && toNode) {
            const fromRect = fromNode.getBoundingClientRect();
            const toRect = toNode.getBoundingClientRect();
            
            // Вычисляем координаты центров узлов с учетом трансформации
            const fromX = (fromRect.left + fromRect.width / 2 - containerRect.left) / scale;
            const fromY = (fromRect.top + fromRect.height / 2 - containerRect.top) / scale;
            const toX = (toRect.left + toRect.width / 2 - containerRect.left) / scale;
            const toY = (toRect.top + toRect.height / 2 - containerRect.top) / scale;
            
            // Вычисляем середину линии
            const midX = (fromX + toX) / 2;
            const midY = (fromY + toY) / 2;
            
            // Вычисляем угол наклона линии
            const angle = Math.atan2(toY - fromY, toX - fromX) * 180 / Math.PI;
            
            // Создаем линию
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', fromX);
            line.setAttribute('y1', fromY);
            line.setAttribute('x2', toX);
            line.setAttribute('y2', toY);
            line.setAttribute('class', `connection-line line-${connection.type}`);
            
            // Создаем маркер (стрелку) посередине линии
            const marker = document.createElementNS('http://www.w3.org/2000/svg', 'path');
            const arrowSize = 6 / scale; // Масштабируем размер стрелки
            marker.setAttribute('d', `M0,0 L-${arrowSize},-${arrowSize} L-${arrowSize},${arrowSize} Z`);
            marker.setAttribute('class', `connection-marker`);
            marker.setAttribute('transform', `translate(${midX},${midY}) rotate(${angle})`);
            
            svg.appendChild(line);
            svg.appendChild(marker);
        }
    });
}

// Делаем функцию глобально доступной
window.refreshConnections = function() {
    updateConnections();
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    loadFamilyConnections();
    
    // Обновляем связи при изменении размера окна
    window.addEventListener('resize', debounce(refreshConnections, 250));
});

// Debounce функция для оптимизации
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}