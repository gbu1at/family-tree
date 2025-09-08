// static/js/parents.js
let currentParentType = null; // 'mother' или 'father'
let allPersons = [];

// Открытие окна выбора родителя
function openParentSelector(parentType) {
    currentParentType = parentType;
    const modal = document.getElementById('parentModal');
    modal.style.display = 'block';
    
    loadParentsList();
}

// Закрытие окна выбора родителя
function closeParentModal() {
    const modal = document.getElementById('parentModal');
    modal.style.display = 'none';
    currentParentType = null;
}

async function loadParentsList() {
    try {
        const response = await fetch('/api/persons');
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }
        
        const allPersons = await response.json();
        const parentsList = document.getElementById('parentsList');
        parentsList.innerHTML = '';
        
        if (allPersons.length === 0) {
            parentsList.innerHTML = '<div class="no-data">Нет людей в базе</div>';
            return;
        }
        
        allPersons.forEach(person => {
            const div = document.createElement('div');
            div.className = 'parent-item';
            div.innerHTML = `
                <strong>${person.second_name} ${person.first_name}</strong>
                ${person.third_name ? person.third_name : ''}
            `;
            div.onclick = () => selectParent(person);
            parentsList.appendChild(div);
        });
        
    } catch (error) {
        console.error('Ошибка загрузки списка людей:', error);
        const parentsList = document.getElementById('parentsList');
        parentsList.innerHTML = '<div class="error">Ошибка загрузки данных</div>';
    }
}

// Выбор родителя
function selectParent(person) {
    if (currentParentType === 'mother') {
        document.getElementById('motherId').value = person.id;
        document.getElementById('motherName').textContent = 
            `${person.second_name} ${person.first_name} ${person.third_name || ''}`;
    } else if (currentParentType === 'father') {
        document.getElementById('fatherId').value = person.id;
        document.getElementById('fatherName').textContent = 
            `${person.second_name} ${person.first_name} ${person.third_name || ''}`;
    }
    
    closeParentModal();
}

// Очистка выбора родителя
function clearParent(parentType) {
    if (parentType === 'mother') {
        document.getElementById('motherId').value = '';
        document.getElementById('motherName').textContent = 'Не выбрана';
    } else if (parentType === 'father') {
        document.getElementById('fatherId').value = '';
        document.getElementById('fatherName').textContent = 'Не выбран';
    }
}

// Поиск по списку родителей
document.getElementById('parentSearch').addEventListener('input', function(e) {
    const searchText = e.target.value.toLowerCase();
    const items = document.querySelectorAll('.parent-item');
    
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(searchText) ? 'block' : 'none';
    });
});
