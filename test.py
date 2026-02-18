import xml.etree.ElementTree as ET
import random


class Section:
    def __init__(self, elem: ET.Element):
        a = elem.attrib
        self.n = a.get("n")
        # Собираем все i-атрибуты в словарь
        self.i_values = {}
        for key, value in a.items():
            if key.startswith('i'):
                self.i_values[key] = value
        self.bits = [0] * 8  # 8 бит для каждой секции
        
    def set_bit(self, bit_index: int, value: int):
        """Установить значение бита (0 или 1)"""
        if 0 <= bit_index < 8:
            self.bits[bit_index] = value if value in (0, 1) else 0
        else:
            raise IndexError(f"Битный индекс должен быть от 0 до 7, получено: {bit_index}")
    
    def get_bit(self, bit_index: int) -> int:
        """Получить значение бита"""
        if 0 <= bit_index < 8:
            return self.bits[bit_index]
        raise IndexError(f"Битный индекс должен быть от 0 до 7, получено: {bit_index}")
    
    def get_binary_string(self) -> str:
        """Получить бинарное представление"""
        return ''.join(str(bit) for bit in self.bits)
    
    def get_decimal_value(self) -> int:
        """Получить десятичное значение битов"""
        return int(self.get_binary_string(), 2)
    
    def get_i_value(self, i_number: int):
        """Получить значение i по номеру (1-8)"""
        i_key = f"i{i_number}"
        return self.i_values.get(i_key, "Не найдено")
    
    def __repr__(self):
        bits_str = ''.join(str(b) for b in self.bits)
        active_count = sum(self.bits)
        return f"<Section n={self.n!r} bits={bits_str} active={active_count}>"


class BitGenerator:
    """Класс для генерации и управления битовыми состояниями секций"""
    
    def __init__(self, sections, seed=None):
        self.sections = sections
        self.total_bits = len(sections) * 8
        self.generated_numbers = []
        
        # Инициализируем генератор случайных чисел
        if seed is not None:
            random.seed(seed)
        
    def generate_random_numbers(self):
        """Генерировать случайную последовательность чисел 0/1 для всех битов"""
        self.generated_numbers = [random.randint(0, 1) for _ in range(self.total_bits)]
        return self.generated_numbers
    
    def apply_numbers_to_sections(self):
        """Применить сгенерированные числа к секциям"""
        if not self.generated_numbers:
            self.generate_random_numbers()
            
        for i, section in enumerate(self.sections):
            start_idx = i * 8
            for j in range(8):
                if start_idx + j < len(self.generated_numbers):
                    section.set_bit(j, self.generated_numbers[start_idx + j])
    
    def set_section_bit(self, section_n, bit_index, value):
        """Установить конкретный бит для секции"""
        section = self._find_section_by_n(section_n)
        if section:
            section.set_bit(bit_index, value)
            # Обновляем generated_numbers
            section_index = self._get_section_index(section_n)
            if section_index is not None:
                idx = section_index * 8 + bit_index
                if idx < len(self.generated_numbers):
                    self.generated_numbers[idx] = value
    
    def display_section_state(self, section_n):
        """Показать состояние конкретной секции с выводом активных i-значений"""
        section = self._find_section_by_n(section_n)
        if section:
            print(f"\nСекция {section_n}")
            print(f"Бинарное представление: {section.get_binary_string()}")
            print(f"\nБиты и соответствующие значения:")
            
            active_found = False
            for i in range(8):
                bit_value = section.get_bit(i)
                i_key = f"i{i+1}"
                i_value = section.get_i_value(i+1)
                
                if bit_value == 1:
                    active_found = True
                    print(f"  Бит {i}: 1 → {i_key} = {i_value}")
                else:
                    print(f"  Бит {i}: 0 → {i_key} = {i_value}")
            
            print(f"\nВключены следующие состояния (где бит = 1):")
            
            if not active_found:
                print("  Нет активных состояний")
            else:
                for i in range(8):
                    if section.get_bit(i) == 1:
                        i_key = f"i{i+1}"
                        i_value = section.get_i_value(i+1)
                        print(f"  {i_key}: {i_value}")
            
            return section
        else:
            print(f"Секция с номером {section_n} не найдена!")
            return None
    
    def display_all_sections(self):
        """Показать состояния всех секций"""
        print(f"\nВсего секций: {len(self.sections)}")
        print(f"Всего битов: {self.total_bits}")
        print("\nСостояния секций:")
        for section in self.sections:
            active_count = sum(section.bits)
            print(f"  Секция {section.n}: {section.get_binary_string()} (активных: {active_count})")
    
    def _find_section_by_n(self, n):
        """Найти секцию по номеру n"""
        for section in self.sections:
            if section.n == str(n):
                return section
        return None
    
    def _get_section_index(self, n):
        """Получить индекс секции в списке"""
        for i, section in enumerate(self.sections):
            if section.n == str(n):
                return i
        return None


def parse_tzk_file(filename: str = "tzk.xml"):
    """Специальная функция для парсинга файла tzk.xml"""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        
        sections = []
        # Ищем все элементы <g> внутри <section>
        for section_elem in root.findall(".//section/g"):
            section = Section(section_elem)
            sections.append(section)
        
        return sections
    except FileNotFoundError:
        print(f"Файл {filename} не найден!")
        return []
    except ET.ParseError as e:
        print(f"Ошибка парсинга XML: {e}")
        return []


def interactive_menu(generator):
    """Интерактивное меню для управления секциями"""
    while True:
        print("\nУПРАВЛЕНИЕ СЕКЦИЯМИ И БИТАМИ")
        print("1. Показать состояние всех секций")
        print("2. Показать состояние конкретной секции")
        print("3. Изменить конкретный бит секции")
        print("0. Выйти")
        
        choice = input("\nВыберите действие (0-3): ").strip()
        
        if choice == "1":
            generator.display_all_sections()
            
        elif choice == "2":
            section_n = input("Введите номер секции: ").strip()
            generator.display_section_state(section_n)
            
        elif choice == "3":
            section_n = input("Введите номер секции: ").strip()
            section = generator.display_section_state(section_n)
            if section:
                try:
                    bit_index = int(input("Введите номер бита (0-7): ").strip())
                    if 0 <= bit_index <= 7:
                        value = int(input("Введите значение (0 или 1): ").strip())
                        if value in (0, 1):
                            generator.set_section_bit(section_n, bit_index, value)
                            print(f"\nБит {bit_index} секции {section_n} установлен в {value}!")
                            generator.display_section_state(section_n)
                        else:
                            print("Ошибка: значение должно быть 0 или 1!")
                    else:
                        print("Ошибка: номер бита должен быть от 0 до 7!")
                except ValueError:
                    print("Ошибка: вводите числа!")
            
        elif choice == "0":
            print("Выход из программы.")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")


def main():
    # Парсим XML файл
    sections = parse_tzk_file("tzk.xml")
    
    if not sections:
        print("Не удалось загрузить секции. Убедитесь, что файл tzk.xml существует.")
        return
    
    # Создаем генератор битов со случайной инициализацией
    generator = BitGenerator(sections)
    
    # Генерируем случайные значения для всех битов
    generator.generate_random_numbers()
    generator.apply_numbers_to_sections()
    
    # Запускаем интерактивное меню
    interactive_menu(generator)


if __name__ == "__main__":
    main()

