// static/js/drag.js
let draggedPerson = null;
let offsetX, offsetY;

// Функция для получения текущих параметров трансформации
function getContainerTransform() {
    const treeContainer = document.querySelector('.tree-container');
    const style = window.getComputedStyle(treeContainer);
    const matrix = new DOMMatrixReadOnly(style.transform);
    
    return {
        scale: matrix.a,
        translateX: matrix.e,
        translateY: matrix.f
    };
}

// Функция для преобразования координат с учетом масштаба
function getScaledCoordinates(clientX, clientY) {
    const transform = getContainerTransform();
    const treeContainer = document.querySelector('.tree-container');
    const containerRect = treeContainer.getBoundingClientRect();
    
    // Преобразуем координаты с учетом масштаба и смещения
    const scaledX = (clientX - containerRect.left - transform.translateX) / transform.scale;
    const scaledY = (clientY - containerRect.top - transform.translateY) / transform.scale;
    
    return { x: scaledX, y: scaledY };
}

// Функция для обновления позиции в базе данных
function updatePersonPosition(personId, x, y) {
    fetch('/api/update_position', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            person_id: personId,
            x: Math.round(x),
            y: Math.round(y)
        })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error('Ошибка сохранения позиции:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

// Начало перетаскивания
document.addEventListener('mousedown', function(e) {
    if (e.target.closest('.edit-btn')) {
        return;
    }

    const personNode = e.target.closest('.person-node');
    if (personNode) {
        // Останавливаем всплытие только если это не кнопка
        if (!e.target.closest('.pan-btn') && !e.target.closest('.zoom-btn')) {
            e.stopPropagation();
            e.preventDefault();
            
            draggedPerson = personNode;
            
            // Получаем координаты с учетом масштаба
            const scaledCoords = getScaledCoordinates(e.clientX, e.clientY);
            const rect = personNode.getBoundingClientRect();
            
            // Вычисляем смещение с учетом масштаба
            offsetX = scaledCoords.x - parseInt(personNode.style.left || 0);
            offsetY = scaledCoords.y - parseInt(personNode.style.top || 0);
            
            // Добавляем класс для визуального эффекта
            draggedPerson.classList.add('dragging');
            draggedPerson.style.zIndex = '1000';
            
            // Блокируем панорамирование только для перемещения людей
            document.addEventListener('mousemove', handlePersonMove);
            document.addEventListener('mouseup', handlePersonUp);
        }
    }
});

// Перемещение человека
function handlePersonMove(e) {
    if (draggedPerson) {
        e.preventDefault();
        
        // Получаем координаты с учетом масштаба
        const scaledCoords = getScaledCoordinates(e.clientX, e.clientY);
        
        // Вычисляем новую позицию
        const treeContainer = document.querySelector('.tree-container');
        const containerRect = treeContainer.getBoundingClientRect();
        const transform = getContainerTransform();
        
        // Масштабируем размеры контейнера для правильного ограничения
        const scaledWidth = containerRect.width / transform.scale;
        const scaledHeight = containerRect.height / transform.scale;
        
        let newX = scaledCoords.x - offsetX;
        let newY = scaledCoords.y - offsetY;
        
        // Ограничиваем перемещение within контейнера (в масштабированных координатах)
        newX = Math.max(0, Math.min(newX, scaledWidth - draggedPerson.offsetWidth));
        newY = Math.max(0, Math.min(newY, scaledHeight - draggedPerson.offsetHeight));
        
        // Применяем новую позицию
        draggedPerson.style.left = newX + 'px';
        draggedPerson.style.top = newY + 'px';
    }
}

// Завершение перетаскивания
function handlePersonUp(e) {
    if (draggedPerson) {
        e.preventDefault();
        
        // Сохраняем позицию в базу данных
        const personId = draggedPerson.dataset.personId;
        
        if (personId) {
            const x = parseInt(draggedPerson.style.left) || 0;
            const y = parseInt(draggedPerson.style.top) || 0;
            
            updatePersonPosition(personId, x, y);
        }
        
        // Убираем классы и сбрасываем z-index
        draggedPerson.classList.remove('dragging');
        draggedPerson.style.zIndex = '';
        
        // Убираем обработчики
        document.removeEventListener('mousemove', handlePersonMove);
        document.removeEventListener('mouseup', handlePersonUp);
        
        draggedPerson = null;

        refreshConnections();
    }
}

// Отмена перетаскивания при выходе за пределы окна
document.addEventListener('mouseleave', function() {
    if (draggedPerson) {
        draggedPerson.classList.remove('dragging');
        draggedPerson.style.zIndex = '';
        
        document.removeEventListener('mousemove', handlePersonMove);
        document.removeEventListener('mouseup', handlePersonUp);
        
        draggedPerson = null;
    }
});