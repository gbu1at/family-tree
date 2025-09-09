from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
from database import PersonDB
from model import PersonInfo

app = Flask(__name__)   
db = PersonDB()

@app.route('/')
def index():
    persons = db.get_all_persons()
    relations = db.get_all_relation()
    return render_template('index.html', persons=persons, relations=relations)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    """Страница добавления нового человека"""
    if request.method == 'POST':
        try:
            person = PersonInfo()

            person.set( first_name=request.form.get('first_name'),
                        second_name=request.form.get('second_name'),
                        third_name=request.form.get('third_name'),
                        gender=request.form.get('gender'),
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



@app.route('/api/person/<int:person_id>')
def get_person_data(person_id):
    """Получение данных человека включая информацию о родителях"""
    try:
        person = db.get_person(person_id)
        if person:
            # Получаем информацию о родителях
            mother_name = None
            father_name = None
            if person.mom_id:
                mother = db.get_person(person.mom_id)
                mother_name = f"{mother.second_name} {mother.first_name} {mother.third_name or ''}"
            if person.dad_id:
                father = db.get_person(person.dad_id)
                father_name = f"{father.second_name} {father.first_name} {father.third_name or ''}"

            print(person.gender)


            return jsonify({
                'id': person.id,
                'date_birth': person.date_birth.isoformat() if person.date_birth else None,
                'place_birth': person.place_birth,
                'age': person.age,
                "gender": person.gender,
                'date_death': person.date_death.isoformat() if person.date_death else None,
                'place_death': person.place_death,
                'history': person.history,
                'education': person.education,
                'work': person.work,
                'mother_id': person.mom_id,
                'father_id': person.dad_id,
                'mother_name': mother_name,
                'father_name': father_name
            })
        return jsonify({'error': 'Person not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/persons')
def get_persons():
    """API для получения всех людей в формате JSON"""
    try:
        persons = db.get_all_persons()
        persons_data = []
        
        for person in persons:
            persons_data.append({
                'id': person.id,
                'first_name': person.first_name,
                'second_name': person.second_name,
                'third_name': person.third_name,
            })
        
        return jsonify(persons_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/list_relation')
def list_relation():
    persons = db.get_all_persons()
    return render_template('list_relation.html', persons=persons)


@app.route('/person/<int:person_id>')
def person_page(person_id):
    person = db.get_person(person_id)
    if not person:
        return "Пользователь не найден", 404
    return render_template('person_page.html', person=person)



@app.route('/api/family_connections')
def get_family_connections():
    """API для получения семейных связей"""
    try:
        # Здесь должен быть код для получения связей из вашей базы данных
        # Пример возвращаемых данных:
        connections = db.get_all_relation()

        print(connections)
        
        return jsonify(connections)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)