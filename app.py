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
    print("--------------------------------------------------------------")
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



if __name__ == '__main__':
    app.run(debug=True)