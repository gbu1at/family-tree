let currentPersonId = null;

// Открытие модального окна
function openModal(personId, event) {    
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    console.log("open");
    currentPersonId = personId;
    
    // ПОКАЗЫВАЕМ модальное окно
    const modal = document.getElementById('personModal');
    modal.style.display = 'block';
    modal.style.opacity = '1';
    
    // Загружаем данные
    loadPersonData(personId);
}

// Закрытие модального окна
function closeModal() {
    console.log("close");
    const modal = document.getElementById('personModal');
    modal.style.display = 'none';
    currentPersonId = null;
    document.getElementById('personForm').reset();
}

// Загрузка данных человека
async function loadPersonData(personId) {
    try {
        const response = await fetch(`/api/person/${personId}`);
        const person = await response.json();
        
        // Заполняем форму данными
        document.getElementById('birthDate').value = person.date_birth || '';
        document.getElementById('birthPlace').value = person.place_birth || '';
        document.getElementById('age').value = person.age || '';
        document.getElementById('deathDate').value = person.date_death || '';
        document.getElementById('deathPlace').value = person.place_death || '';
        document.getElementById('history').value = person.history || '';
        document.getElementById('education').value = person.education ? JSON.parse(person.education).join(', ') : '';
        document.getElementById('work').value = person.work ? JSON.parse(person.work).join(', ') : '';
        
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        alert('Не удалось загрузить данные');
        closeModal(); // Закрываем окно при ошибке
    }
}

// Обработка отправки формы
document.getElementById('personForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = {
        id: currentPersonId,
        date_birth: formData.get('birth_date'),
        place_birth: formData.get('birth_place'),
        age: parseInt(formData.get('age')) || null,
        date_death: formData.get('death_date'),
        place_death: formData.get('death_place'),
        history: formData.get('history'),
        education: formData.get('education'),
        work: formData.get('work')
    };
    
    try {
        const response = await fetch('/api/update_person', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('Данные успешно сохранены!');
            closeModal();
        } else {
            alert('Ошибка сохранения: ' + result.error);
        }
        
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Ошибка сохранения данных');
    }
});
