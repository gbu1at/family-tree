import sqlite3
import json
from datetime import date
from typing import List, Optional, Dict, Any
from model import PersonInfo, person_to_dict, dict_to_person

class PersonDB:
    def __init__(self, db_path: str = "genealogy.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persons (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    second_name TEXT NOT NULL,
                    third_name TEXT,
                    gender TEXT CHECK(gender IN ('m', 'f')),
                    date_birth TEXT,
                    place_birth TEXT,
                    age INTEGER,
                    date_death TEXT,
                    place_death TEXT,
                    history TEXT,
                    education TEXT,
                    work TEXT,
                    mom_id INTEGER,
                    dad_id INTEGER,
                    x INTEGER DEFAULT 0,
                    y INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_person(self, person: PersonInfo) -> int:
        if not person.first_name or not person.second_name:
            raise ValueError("Имя и фамилия обязательны для добавления в БД")
        
        person_data = person_to_dict(person)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO persons 
                (first_name, second_name, third_name, gender, date_birth, place_birth, 
                 age, date_death, place_death, history, education, work, mom_id, dad_id, x, y)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                person_data['first_name'],
                person_data['second_name'],
                person_data['third_name'],
                person_data['gender'],
                person_data['date_birth'],
                person_data['place_birth'],
                person_data['age'],
                person_data['date_death'],
                person_data['place_death'],
                person_data['history'],
                person_data['education'],
                person_data['work'],
                person_data['mom_id'],
                person_data['dad_id'],
                person_data['x'],
                person_data['y']

            ))
            conn.commit()
            return cursor.lastrowid
    
    def delete_person(self, person_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM persons WHERE id = ?', (person_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_person(self, person_id: int) -> Optional[PersonInfo]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM persons WHERE id = ?', (person_id,))
            row = cursor.fetchone()
            
            if row:
                return dict_to_person(dict(row))
            return None
    
    def get_all_persons(self) -> List[PersonInfo]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM persons ORDER BY second_name, first_name')
            rows = cursor.fetchall()
            
            return [dict_to_person(dict(row)) for row in rows]
    
    def update_person(self, person_id: int, person: PersonInfo) -> bool:
        person_data = person_to_dict(person)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE persons 
                SET first_name = ?, second_name = ?, third_name = ?, gender = ?,
                    date_birth = ?, place_birth = ?, age = ?, 
                    date_death = ?, place_death = ?, history = ?, 
                    education = ?, work = ?, mom_id = ?, dad_id = ?, x = ?, y = ?
                WHERE id = ?
            ''', (
                person_data['first_name'],
                person_data['second_name'],
                person_data['third_name'],
                person_data['gender'],
                person_data['date_birth'],
                person_data['place_birth'],
                person_data['age'],
                person_data['date_death'],
                person_data['place_death'],
                person_data['history'],
                person_data['education'],
                person_data['work'],
                person_data['mom_id'],
                person_data['dad_id'],
                person_data['x'],
                person_data['y'],
                person_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def search_persons(self, first_name: str = None, second_name: str = None) -> List[PersonInfo]:
        query = 'SELECT * FROM persons WHERE 1=1'
        params = []
        
        if first_name:
            query += ' AND first_name LIKE ?'
            params.append(f'%{first_name}%')
        
        if second_name:
            query += ' AND second_name LIKE ?'
            params.append(f'%{second_name}%')
        
        query += ' ORDER BY second_name, first_name'
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            return [dict_to_person(dict(row)) for row in rows]

    def update_person_position(self, person_id: int, x: int, y: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE persons 
                SET x = ?, y = ?
                WHERE id = ?
            ''', (x, y, person_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_all_relation(self):
        persons = self.get_all_persons()

        edges = []

        for p in persons:
            if p.mom_id is not None:
                edges.append({"from_id": p.id, "to_id": p.mom_id})
            if p.dad_id is not None:
                edges.append({"from_id": p.id, "to_id": p.dad_id})

        return edges
