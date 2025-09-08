from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from database import PersonDB
from model import PersonInfo

app = Flask(__name__)   
db = PersonDB()

@app.route('/')
def index():
    persons = db.get_all_persons()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    """Страница добавления нового человека"""
    if request.method == 'POST':
        try:
            person = PersonInfo()

            person.set( first_name=request.form.get('first_name'),
                        second_name=request.form.get('second_name'),
                        third_name=request.form.get('third_name'),
                        x=random.randint(0, 200),
                        y=random.randint(0, 200),)
            
            person_id = db.add_person(person)
            
            return redirect(url_for('index'))
            
        except Exception as e:
            return f"Ошибка при добавлении: {str(e)}"
    
    return render_template('add_person.html')

@app.route('/api/update_position', methods=['POST'])
def update_position():
    """Обновление позиции человека"""
    try:
        data = request.get_json()
        person_id = data.get('person_id')
        x = data.get('x')
        y = data.get('y')
        
        if db.update_person_position(person_id, x, y):
            return jsonify({'success': True, 'message': 'Position updated'})
        else:
            return jsonify({'success': False, 'error': 'Person not found'})
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/delete/<int:person_id>')
def delete_person(person_id):
    """Удаление человека"""
    if db.delete_person(person_id):
        return redirect(url_for('index'))
    return "Человек не найден"



@app.route('/api/person/<int:person_id>')
def get_person_data(person_id):
    """Получение данных человека"""
    try:
        person = db.get_person(person_id)
        if person:
            return jsonify({
                'date_birth': person.date_birth.isoformat() if person.date_birth else None,
                'place_birth': person.place_birth,
                'age': person.age,
                'date_death': person.date_death.isoformat() if person.date_death else None,
                'place_death': person.place_death,
                'history': person.history,
                'education': person.education,
                'work': person.work
            })
        return jsonify({'error': 'Person not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_person', methods=['POST'])
def update_person_data():
    """Обновление данных человека"""
    try:
        data = request.get_json()
        
        print(data)

        person_id = data.get('id')

        person = db.get_person(person_id)

        person.set_kwargs(data)

        db.update_person(person_id, person)

        return jsonify({'success': True, 'message': 'Data updated'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)