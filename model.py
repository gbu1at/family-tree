from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union

class PersonInfo:
    def __init__(self):
        self.id: Optional[int] = None
        self.first_name: Optional[str] = None
        self.second_name: Optional[str] = None
        self.third_name: Optional[str] = None
        self.gender: Optional[str] = None

        self.date_birth: Optional[date] = None
        self.place_birth: Optional[str] = None
        self.age: Optional[int] = None
        self.date_death: Optional[date] = None
        self.place_death: Optional[str] = None
        self.history: Optional[str] = None
        self.education: Optional[str] = None
        self.work: Optional[str] = None
        
        self.mom_id: Optional[int] = None
        self.dad_id: Optional[int] = None

        self.x: int = 0
        self.y: int = 0


    def set_id(self, id: int) -> None:
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID должен быть положительным целым числом")
        self.id = id
    
    def set_first_name(self, first_name: str) -> None:
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("Имя должно быть непустой строкой")
        self.first_name = first_name.strip()
    
    def set_second_name(self, second_name: str) -> None:
        if not isinstance(second_name, str) or not second_name.strip():
            raise ValueError("Фамилия должна быть непустой строкой")
        self.second_name = second_name.strip()
    
    def set_third_name(self, third_name: Optional[str]) -> None:
        if third_name is not None and not isinstance(third_name, str):
            raise ValueError("Отчество должно быть строкой или None")
        self.third_name = third_name.strip() if third_name else None


    def set_gender(self, gender: str) -> None:
        if not isinstance(gender, str):
            raise ValueError("gender должен быть строкой")
        
        gender = gender.lower()

        if gender not in ["f", "m"]:
            raise ValueError("gender должен быть строкой равной f или m")

        self.gender = gender
    
    def set_date_birth(self, date_birth: Optional[Union[date, str]]) -> None:
        if date_birth is not None:
            if isinstance(date_birth, str):
                if not date_birth.strip():
                    self.date_birth = None
                    return
                try:
                    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y.%m.%d'):
                        try:
                            date_birth = datetime.strptime(date_birth, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        raise ValueError(f"Неверный формат даты: {date_birth}")
                except Exception as e:
                    raise ValueError(f"Ошибка преобразования даты: {e}")
            
            if not isinstance(date_birth, date):
                raise ValueError("Дата должна быть объектом date, строкой или None")
            
            if date_birth > datetime.now().date():
                raise ValueError("Дата не может быть в будущем")
        
        self.date_birth = date_birth
    
    def set_place_birth(self, place_birth: Optional[str]) -> None:
        if place_birth is not None and not isinstance(place_birth, str):
            raise ValueError("Место рождения должно быть строкой или None")
        self.place_birth = place_birth.strip() if place_birth else None
    
    def set_date_death(self, date_death: Optional[date]) -> None:
        if date_death is not None:
            if isinstance(date_death, str):
                if not date_death.strip():
                    self.date_death = None
                    return
                try:
                    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y.%m.%d'):
                        try:
                            date_death = datetime.strptime(date_death, fmt).date()
                            break
                        except ValueError:
                            continue
                    else:
                        raise ValueError(f"Неверный формат даты: {date_death}")
                except Exception as e:
                    raise ValueError(f"Ошибка преобразования даты: {e}")
            
            if not isinstance(date_death, date):
                raise ValueError("Дата должна быть объектом date, строкой или None")
            
            if date_death > datetime.now().date():
                raise ValueError("Дата не может быть в будущем")
        
        self.date_death = date_death
        
        if self.date_birth:
            self._calculate_age()
    
    def set_place_death(self, place_death: Optional[str]) -> None:
        if place_death is not None and not isinstance(place_death, str):
            raise ValueError("Место смерти должно быть строкой или None")
        self.place_death = place_death.strip() if place_death else None
    
    def set_history(self, history: Optional[str]) -> None:
        if history is not None and not isinstance(history, str):
            raise ValueError("История должна быть строкой или None")
        self.history = history
    
    def set_education(self, education: Optional[str]) -> None:
        if education is not None and not isinstance(education, str):
            raise ValueError("Образование должно быть строкой или None")
        self.education = education
    
    def set_work(self, work: Optional[str]) -> None:
        if work is not None and not isinstance(work, str):
            raise ValueError("Работа должно быть строкой или None")
        self.work = work

    def set_x(self, x) -> None:
        self.x = x

    def set_y(self, y) -> None:
        self.y = y

    def _calculate_age(self) -> None:
        if not self.date_birth:
            self.age = None
            return
        
        end_date = self.date_death if self.date_death else datetime.now().date()
        
        age = end_date.year - self.date_birth.year
        
        if (end_date.month, end_date.day) < (self.date_birth.month, self.date_birth.day):
            age -= 1
        
        self.age = age
    
    def get_full_name(self) -> str:
        parts = []
        if self.second_name:
            parts.append(self.second_name)
        if self.first_name:
            parts.append(self.first_name)
        if self.third_name:
            parts.append(self.third_name)
        return " ".join(parts) if parts else "Неизвестно"
    
    def __str__(self) -> str:
        return f"PersonInfo({self.get_full_name()}, возраст: {self.age})"

    def set(self, **info) -> None:
        for key, value in info.items():
            if hasattr(self, key):
                setter_method = f"set_{key}"
                if hasattr(self, setter_method):
                    getattr(self, setter_method)(value)
                else:
                    setattr(self, key, value)
            else:
                raise AttributeError(f"PersonInfo не имеет атрибута '{key}'")
            
    def set_kwargs(self, info) -> None:
        for key, value in info.items():
            if hasattr(self, key):
                setter_method = f"set_{key}"
                if hasattr(self, setter_method):
                    getattr(self, setter_method)(value)
                else:
                    setattr(self, key, value)
            else:
                raise AttributeError(f"PersonInfo не имеет атрибута '{key}'")


def person_to_dict(person: PersonInfo) -> Dict[str, Any]:
    return {
        'first_name': person.first_name,
        'second_name': person.second_name,
        'third_name': person.third_name,
        'gender': person.gender,
        'date_birth': person.date_birth.isoformat() if person.date_birth else None,
        'place_birth': person.place_birth,
        'age': person.age,
        'date_death': person.date_death.isoformat() if person.date_death else None,
        'place_death': person.place_death,
        'history': person.history,
        'education': person.education,
        'work': person.work,
        'mom_id': person.mom_id,
        'dad_id': person.dad_id,
        'x': person.x,
        'y': person.y,
    }


def dict_to_person(row: Dict[str, Any]) -> PersonInfo:
    person = PersonInfo()
    person.set(
        id=row['id'],
        first_name=row['first_name'],
        second_name=row['second_name'],
        third_name=row['third_name'],
        gender=row["gender"],
        date_birth=date.fromisoformat(row['date_birth']) if row['date_birth'] else None,
        place_birth=row['place_birth'],
        age=row['age'],
        date_death=date.fromisoformat(row['date_death']) if row['date_death'] else None,
        place_death=row['place_death'],
        history=row['history'],
        education=row['education'],
        work=row['work'],
        mom_id=row['mom_id'],
        dad_id=row['dad_id'],
        x=row['x'],
        y=row['y']
    )
    return person
