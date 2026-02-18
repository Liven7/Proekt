import xml.etree.ElementTree as ET
import random
from typing import Dict, List, Union, Optional

# ==================== КЛАССЫ ДЛЯ ОБЪЕКТОВ ====================

class Section:
    """Класс для представления секции"""
    def __init__(self, section_id: str, zIn: str, pIn: str, 
                 n_l: str, n_r: str, n_t: Optional[str] = None):
        self.id = section_id
        self.zIn = zIn
        self.pIn = pIn
        self.n_l = n_l
        self.n_r = n_r
        self.n_t = n_t
        self.states = {'i1': 0, 'i2': 0, 'i3': 0}  # ЗН, СП, ЗМ
        self.status = "неизвестно"
        
    def update_status(self):
        """Обновляет статус секции на основе состояний датчиков"""
        bits = list(self.states.values())
        ones_count = sum(bits)
        
        if ones_count == 0:
            self.status = "неизвестно"
        elif ones_count == 1:
            if bits[0] == 1:
                self.status = "ЗН"  # Занято
            elif bits[1] == 1:
                self.status = "СП"  # Свободно
            elif bits[2] == 1:
                self.status = "ЗМ"  # Замкнуто
        else:  # больше 1 единицы - АВАРИЯ
            self.status = "АВАРИЯ"
            
    def set_states(self, states: List[int]):
        """Устанавливает состояния датчиков"""
        if len(states) != 3:
            raise ValueError("Должно быть 3 состояния")
        self.states = {'i1': states[0], 'i2': states[1], 'i3': states[2]}
        self.update_status()
        
    def get_available_states(self) -> Dict[str, List[int]]:
        """Возвращает доступные состояния для установки"""
        return {
            "ЗН (занято)": [1, 0, 0],
            "СП (свободно)": [0, 1, 0],
            "ЗМ (замкнуто)": [0, 0, 1]
        }


class Switch:
    """Класс для представления стрелки"""
    def __init__(self, switch_id: str):
        self.id = switch_id
        # Состояния: МК, ПК, -, +, З, ВЗ
        self.states = {'i1': 0, 'i2': 0, 'i3': 0, 'i4': 0, 'i5': 0, 'i6': 0}
        self.status = "неизвестно"
        
    def update_status(self):
        """Обновляет статус стрелки"""
        bits = list(self.states.values())
        ones_count = sum(bits)
        
        if ones_count == 0:
            self.status = "неизвестно"
        elif ones_count == 1:
            if bits[0] == 1:
                self.status = "Минусовой контроль"
            elif bits[1] == 1:
                self.status = "Плюсовой Контроль"
            elif bits[2] == 1:
                self.status = "Стрелка едет в Минус"
            elif bits[3] == 1:
                self.status = "Стрелка едет в Плюс"
            elif bits[4] == 1:
                self.status = "Замкнута"
            elif bits[5] == 1:
                self.status = "Вспомогательно замкнута"
        else:  # больше 1 единицы - потеря контроля
            self.status = "потеря контроля"
            
    def set_states(self, states: List[int]):
        """Устанавливает состояния стрелки"""
        if len(states) != 6:
            raise ValueError("Должно быть 6 состояний")
        self.states = {
            'i1': states[0], 'i2': states[1], 
            'i3': states[2], 'i4': states[3],
            'i5': states[4], 'i6': states[5]
        }
        self.update_status()
        
    def get_available_states(self) -> Dict[str, List[int]]:
        """Возвращает доступные состояния для установки"""
        return {
            "МК (минусовой контроль)": [1, 0, 0, 0, 0, 0],
            "ПК (плюсовой контроль)": [0, 1, 0, 0, 0, 0],
            "- (стрелка в минус)": [0, 0, 1, 0, 0, 0],
            "+ (стрелка в плюс)": [0, 0, 0, 1, 0, 0],
            "З (замкнуто)": [0, 0, 0, 0, 1, 0],
            "ВЗ (вспомогательно замкнуто)": [0, 0, 0, 0, 0, 1]
        }


# ==================== ФАБРИКА ОБЪЕКТОВ ====================

def create_objects_factory(test_xml_path: str, tzk_xml_path: str) -> Dict[str, Union[Section, Switch]]:
    """
    Фабрика для создания объектов из XML файлов
    Возвращает словарь объектов
    """
    objects = {}
    
    # Парсим test.xml для получения информации о секциях
    tree_test = ET.parse(test_xml_path)
    root_test = tree_test.getroot()
    
    # Создаем секцииcode 
    sections_elem = root_test.find('sections')
    for section_elem in sections_elem.findall('section'):
        section_id = section_elem.get('id')
        zIn = section_elem.get('zIn')
        pIn = section_elem.get('pIn')
        n_l = section_elem.get('n_l')
        n_r = section_elem.get('n_r')
        n_t = section_elem.get('n_t')
        
        section = Section(section_id, zIn, pIn, n_l, n_r, n_t)
        objects[f"section_{section_id}"] = section
    
    # Парсим tzk.xml для получения информации о входах
    tree_tzk = ET.parse(tzk_xml_path)
    root_tzk = tree_tzk.getroot()
    
    # Создаем стрелки из раздела switch
    switch_elem = root_tzk.find('switch')
    for g_elem in switch_elem.findall('g'):
        switch_id = g_elem.get('n')
        switch = Switch(switch_id)
        objects[f"switch_{switch_id}"] = switch
    
    return objects


# ==================== ГЕНЕРАТОР БИТОВ ====================

def generate_8_bits() -> List[int]:
    """Генерирует последовательность из 8 битов"""
    return [random.randint(0, 1) for _ in range(8)]


def map_8bits_to_object(bits: List[int], is_section: bool) -> List[int]:
    """
    Преобразует 8 битов в состояния для объекта
    Для секции: используем первые 3 бита
    Для стрелки: используем первые 6 битов
    """
    if is_section:
        # Для секции берем первые 3 бита
        object_bits = bits[:3]
        
        # Проверяем аварию (больше 1 единицы) с вероятностью 1/25
        if sum(object_bits) > 1:
            # С вероятностью 1/25 оставляем аварию, иначе исправляем
            if random.randint(1, 25) == 1:  # 1 к 25
                return object_bits  # Оставляем аварию
            else:
                # Исправляем на случайное валидное состояние
                valid_states = [
                    [1, 0, 0],  # ЗН
                    [0, 1, 0],  # СП
                    [0, 0, 1]   # ЗМ
                ]
                return random.choice(valid_states)
        return object_bits
    else:
        # Для стрелки берем первые 6 битов
        object_bits = bits[:6]
        
        # Проверяем потерю контроля (больше 1 единицы)
        if sum(object_bits) > 1:
            # С вероятностью 1/25 оставляем потерю контроля, иначе исправляем
            if random.randint(1, 25) == 1:  # 1 к 25
                return object_bits  # Оставляем потерю контроля
            else:
                # Исправляем на случайное валидное состояние
                valid_states = [
                    [1, 0, 0, 0, 0, 0],  # МК
                    [0, 1, 0, 0, 0, 0],  # ПК
                    [0, 0, 1, 0, 0, 0],  # -
                    [0, 0, 0, 1, 0, 0],  # +
                    [0, 0, 0, 0, 1, 0],  # З
                    [0, 0, 0, 0, 0, 1]   # ВЗ
                ]
                return random.choice(valid_states)
        return object_bits


def generate_and_apply_bits(objects: Dict):
    """
    Генерирует биты для всех объектов и применяет их
    """
    print("\nГенерация состояний...")
    
    for obj_name, obj in objects.items():
        # Генерируем 8 битов
        bits_8 = generate_8_bits()
        
        # Определяем тип объекта и преобразуем биты
        if isinstance(obj, Section):
            is_section = True
            object_bits = map_8bits_to_object(bits_8, is_section)
            obj.set_states(object_bits)
            
            # Проверяем аварию
            '''if sum(object_bits) > 1:
                print(f"Секция {obj.id}: АВАРИЯ")'''
                
        elif isinstance(obj, Switch):
            is_section = False
            object_bits = map_8bits_to_object(bits_8, is_section)
            obj.set_states(object_bits)
            
            # Проверяем потерю контроля
            '''if sum(object_bits) > 1:
                print(f"Стрелка {obj.id}: потеря контроля")'''


# ==================== ОСНОВНОЕ МЕНЮ ====================

def show_object_status(objects: Dict):
    """Показывает состояние объекта (секции или стрелки)"""
    obj_id = input("Введите ID (например, 401 или 403): ").strip() #есть ошибка в ID секции
    
    # Проверяем, секция это или стрелка
    section_key = f"section_{obj_id}"
    switch_key = f"switch_{obj_id}"
    
    if section_key in objects:
        obj = objects[section_key]
        print(f"\nСекция {obj.id}: {obj.status}")
    elif switch_key in objects:
        obj = objects[switch_key]
        print(f"\nСтрелка {obj.id}: {obj.status}")
    else:
        print(f"ID {obj_id} не найден!")


def change_object_status(objects: Dict):
    """Изменяет состояние объекта (секции или стрелки)"""
    obj_id = input("Введите ID для изменения: ").strip()
    
    # Проверяем, секция это или стрелка
    section_key = f"section_{obj_id}"
    switch_key = f"switch_{obj_id}"
    
    if section_key in objects:
        obj = objects[section_key]
        print(f"\nТекущее состояние секции {obj.id}: {obj.status}")
        print("\nДоступные состояния:")
        
        available_states = obj.get_available_states()
        states_list = list(available_states.items())
        
        for i, (state_name, _) in enumerate(states_list, 1):
            print(f"{i}. {state_name}")
        
        try:
            choice = int(input("\nВыберите состояние: "))
            if 1 <= choice <= len(states_list):
                selected_state_name, selected_bits = states_list[choice - 1]
                obj.set_states(selected_bits)
                print(f"\nСекция {obj.id} установлена в состояние: {selected_state_name}")
            else:
                print("Неверный выбор!")
        except ValueError:
            print("Введите число!")
            
    elif switch_key in objects:
        obj = objects[switch_key]
        print(f"\nТекущее состояние стрелки {obj.id}: {obj.status}")
        print("\nДоступные состояния:")
        
        available_states = obj.get_available_states()
        states_list = list(available_states.items())
        
        for i, (state_name, _) in enumerate(states_list, 1):
            print(f"{i}. {state_name}")
        
        try:
            choice = int(input("\nВыберите состояние: "))
            if 1 <= choice <= len(states_list):
                selected_state_name, selected_bits = states_list[choice - 1]
                obj.set_states(selected_bits)
                print(f"\nСтрелка {obj.id} установлена в состояние: {selected_state_name}")
            else:
                print("Неверный выбор!")
        except ValueError:
            print("Введите число!")
    else:
        print(f"ID {obj_id} не найден!")


def show_all_objects(objects: Dict):
    """Выводит все секции и стрелки"""
    print("\n" + "="*50)
    print("СЕКЦИИ:")
    print("="*50)
    
    sections_found = False
    for obj_name, obj in objects.items():
        if isinstance(obj, Section):
            sections_found = True
            print(f"Секция {obj.id}: {obj.status}")
    
    if not sections_found:
        print("Секции не найдены")
    
    print("\n" + "="*50)
    print("СТРЕЛКИ:")
    print("="*50)
    
    switches_found = False
    for obj_name, obj in objects.items():
        if isinstance(obj, Switch):
            switches_found = True
            print(f"Стрелка {obj.id}: {obj.status}")
    
    if not switches_found:
        print("Стрелки не найдены")


def main_menu(objects: Dict):
    """Основное меню программы"""
    while True:
        print("")
        print("1. Показать состояние объекта")
        print("2. Изменить состояние объекта")
        print("3. Вывод всех объектов")
        print("4. Сгенерировать новые состояния (обновить данные)")
        print("5. Выход")
        
        choice = input("\nВыберите действие (1-5): ").strip()
        
        if choice == "1":
            show_object_status(objects)
        elif choice == "2":
            change_object_status(objects)
        elif choice == "3":
            show_all_objects(objects)
        elif choice == "4":
            generate_and_apply_bits(objects)
            print("\nДанные обновлены!")
        elif choice == "5":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


# ==================== ОСНОВНАЯ ПРОГРАММА ====================

def main():
    """Основная функция программы"""
    
    # Создаем объекты через фабрику
    try:
        objects = create_objects_factory("test.xml", "tzk.xml")
        
        # Генерируем начальные состояния
        generate_and_apply_bits(objects)
        
        # Запускаем главное меню
        main_menu(objects)
        
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()