function selectGender(gender) {
    // Приводим к нижнему регистру для consistency
    gender = gender.toLowerCase();
    
    // Убираем выделение со всех кнопок
    document.querySelectorAll('.gender-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // Добавляем выделение выбранной кнопке
    const selectedBtn = document.querySelector(`.gender-btn[data-gender="${gender}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('selected');
    }
    
    // Устанавливаем значение в hidden input
    document.getElementById('gender').value = gender; // Сохраняем в верхнем регистре
}

// Валидация формы перед отправкой
document.querySelector('.person-form').addEventListener('submit', function(e) {
    const gender = document.getElementById('gender').value;
    if (!gender) {
        e.preventDefault();
        alert('Пожалуйста, выберите пол');
        return;
    }
});