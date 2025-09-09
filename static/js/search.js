// static/js/search.js
let currentHighlightedPerson = null;

function searchPerson(event) {
    event.preventDefault(); // Предотвращаем отправку формы
    
    const lastName = document.getElementById('searchLastName').value.trim().toLowerCase();
    const firstName = document.getElementById('searchFirstName').value.trim().toLowerCase();
    const patronymic = document.getElementById('searchPatronymic').value.trim().toLowerCase();
    
    // Проверяем, что хотя бы одно поле заполнено
    if (!lastName && !firstName && !patronymic) {
        alert('Заполните хотя бы одно поле для поиска');
        return;
    }
    
    const persons = document.querySelectorAll('.person-node');
    let foundPerson = null;
    
    // Ищем человека по всем трем полям
    persons.forEach(person => {
        const personLastName = person.querySelector('.person-name')?.textContent.split(' ')[0]?.toLowerCase() || '';
        const personFirstName = person.querySelector('.person-name')?.textContent.split(' ')[1]?.toLowerCase() || '';
        const personPatronymic = person.querySelector('.person-patronymic')?.textContent.toLowerCase() || '';
        
        // Проверяем совпадение по всем заполненным полям
        const matchesLastName = !lastName || personLastName.includes(lastName);
        const matchesFirstName = !firstName || personFirstName.includes(firstName);
        const matchesPatronymic = !patronymic || personPatronymic.includes(patronymic);
        
        if (matchesLastName && matchesFirstName && matchesPatronymic) {
            foundPerson = person;
            return;
        }
    });
    
    if (foundPerson) {
        // Убираем предыдущее выделение
        if (currentHighlightedPerson) {
            currentHighlightedPerson.classList.remove('highlighted');
        }
        
        // Выделяем найденного человека
        foundPerson.classList.add('highlighted');
        currentHighlightedPerson = foundPerson;
        
        // Перемещаем экран к человеку
        centerOnPerson(foundPerson);
    } else {
        alert('Человек не найден');
    }
}

function centerOnPerson(personElement) {
    const treeWrapper = document.querySelector('.tree-wrapper');
    const treeContainer = document.querySelector('.tree-container');
    const transform = getContainerTransform();
    
    // Получаем координаты человека
    const personX = parseInt(personElement.style.left) || 0;
    const personY = parseInt(personElement.style.top) || 0;
    
    // Вычисляем центр видимой области
    const centerX = treeWrapper.offsetWidth / 2;
    const centerY = treeWrapper.offsetHeight / 2;
    
    // Вычисляем новые координаты трансформации
    const targetX = personX * transform.scale - centerX;
    const targetY = personY * transform.scale - centerY;
    
    // Плавное перемещение
    translateX = targetX;
    translateY = targetY;
    
    // Ограничиваем перемещение
    constrainViewport();
    updateTransform();
    
    // Масштабируем для лучшего обзора
    scale = 1.5;
    updateTransform();
}

function clearSearch() {
    document.getElementById('searchLastName').value = '';
    document.getElementById('searchFirstName').value = '';
    document.getElementById('searchPatronymic').value = '';
    
    if (currentHighlightedPerson) {
        currentHighlightedPerson.classList.remove('highlighted');
        currentHighlightedPerson = null;
    }
    
    // Возвращаем обычный масштаб
    scale = 1;
    updateTransform();
}

// Поиск по нажатию Enter в любом поле
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchPerson(e);
        }
    });
});

// Фокус на следующее поле при нажатии Enter
document.querySelectorAll('.form-input').forEach((input, index, inputs) => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && index < inputs.length - 1) {
            e.preventDefault();
            inputs[index + 1].focus();
        }
    });
});