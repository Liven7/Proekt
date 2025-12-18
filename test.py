'''
import xml.etree.ElementTree as ET

tree = ET.parse('test.xml')
root = tree.getroot()

sost = [[i * 4 + j for j in range(3)] for i in range(2)]

for section in root.findall('section'):
    section_list = []
    section_id = section.get('id')
    section_list.append(Way(section))
    sost.append(section_id)

class Connect:
    def __init__():
        n_array, n_group, n_imp = ....

class NetConnect:
    def __init__(name):
        self.name = name
        .... # Найти импульс в ТЗК

    def check_state():
        # Проверяет сотояние из сети

class Way:
    def __init__(attrs):
        self.name = attrs["name"]
        self.id = attrs["id"]
        self.nb_left = attrs["left"]
        self.nb_rigth = attrs["rigth"]
        self.pIn_state = NetConnect(attrs["pIn"]) # 1 1 1



print(sost)

'''

''' 
    section_left = section.find('section_left').text
    section_right = section.find('section_right').text
    print(f"ID: {section_id}, {section_left} - {section_right}")

'''

'''

numbers = []
for i in range(2):
    for r in range(2):
        numbers.append(r+1)
    numbers.append(1212)
    numbers.append(i+1)

print("\n", numbers)

'''
'''
matrix = [[i * 4 + j for j in range(4)] for i in range(5)]
# выводим массив построчно с отступами
for row in matrix:
   print(' '.join(map(str, row)))



'''


''' 

import random

def generate_and_edit_random_numbers(count):
    random_numbers = [random.randint(0, 1) for _ in range(count)]
    print("Сгенерированные числа:", random_numbers)
    
    Нужно ли нам выводить промежуточное значение в массиве?
    print("\nНомера чисел для редактирования (от 1 до {}):".format(count))
    for i in range(len(random_numbers)):
        print("{}: {}".format(i + 1, random_numbers[i]))
    
    
    while True:
        try:
            choice = input("\nВведите порядковый номер в массиве для редактирования (или 'q' для выхода): ")
            
            if choice.lower() == 'q':
                break
            
            index = int(choice) - 1
            if 0 <= index < count:
                print("Текущий элемент в массиве [{}]: состояние: {}".format(index + 1, random_numbers[index]))
                
                while True:
                    try:
                        new_value = int(input("Введите новое значение (от 0 до 1): "))
                        if 0 <= new_value <= 1:
                            random_numbers[index] = new_value
                            print("Число изменено на:", new_value)
                            break
                        else:
                            print("Ошибка: значение должно быть 0 или 1")
                    except ValueError:
                        print("Ошибка: введите 0 или 1")
            else:
                print("Ошибка: номер числа выходит за массив")
                
        except ValueError:
            print("Ошибка: номер числа выходит за массив или 'q' для выхода")
    
    print("\nФинальный список чисел:", random_numbers)
    return random_numbers

def split_into_chunks(arr, chunk_size=8):
    """Разбивает массив на части по chunk_size """
    chunks = []
    for i in range(0, len(arr), chunk_size):
        chunk = arr[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

def print_chunks(chunks):
    print(f"\nМассив разбит на группы по 8 элементов:")
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Группа {idx}: {chunk}")

def main():
    try:
        num_count = int(input("кол-во чисел в массиве "))
        if num_count <= 0:
            print("введите положительное число")
            return
        
        #Генерация и редактирование массива
        final_array = generate_and_edit_random_numbers(num_count)
        
        #Разбиение на группы по 8 элементов
        chunks = split_into_chunks(final_array, 8)
        
        #Вывод результата
        print_chunks(chunks)
        print(f"\nИтоговый массив: {final_array}")
        
    except ValueError:
        print("Ошибка: введите целое число")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()


'''

import xml.etree.ElementTree as ET


class Section:
    def __init__(self, elem: ET.Element):
        a = elem.attrib
        self.id = a.get("id")
        self.pIn = a.get("pIn")
        self.zIn = a.get("zIn")

    def __repr__(self):
        return f"<Section id={self.id!r} pIn={self.pIn!r} zIn={self.zIn!r}>"


class Way:
    def __init__(self, elem: ET.Element):
        a = elem.attrib
        self.id = a.get("id")
        self.pIn = a.get("pIn")
        self.zIn = a.get("zIn")

    def __repr__(self):
        return f"<Way id={self.id!r} pIn={self.pIn!r} zIn={self.zIn!r}>"


class Switch:
    def __init__(self, elem: ET.Element):
        a = elem.attrib
        self.id = a.get("id")
        self.pkIn = a.get("pkIn")
        self.mkIn = a.get("mkIn")

    def __repr__(self):
        return f"<Switch id={self.id!r} pkIn={self.pkIn!r} mkIn={self.mkIn!r}>"


class Signal:
    def __init__(self, elem: ET.Element):
        a = elem.attrib
        self.id = a.get("id")
        self.redIn = a.get("redIn")
        self.greenIn = a.get("greenIn")
        self.yellowIn = a.get("yellowIn")
        self.blueIn = a.get("blueIn")

    def __repr__(self):
        return (
            f"<Signal id={self.id!r} r={self.redIn!r} g={self.greenIn!r} "
            f"y={self.yellowIn!r} b={self.blueIn!r}>"
        )


class ObjectFactory:
    def __init__(self):
        self.sections = []
        self.ways = []
        self.switches = []
        self.signals = []
        self._all = []

        self._registry = {
            "section": (Section, self.sections),
            "way": (Way, self.ways),
            "switch": (Switch, self.switches),
            "signal": (Signal, self.signals),
        }

    @property
    def all_objects(self):
        return self._all

    def load_from_file(self, filename: str):
        tree = ET.parse(filename)
        root = tree.getroot()
        self._create_objects(root)

    def load_from_string(self, xml_text: str):
        root = ET.fromstring(xml_text)
        self._create_objects(root)

    def _create_objects(self, root: ET.Element):
        for elem in root.iter():
            reg = self._registry.get(elem.tag)
            if reg is None:
                continue
            cls, lst = reg
            obj = cls(elem)
            lst.append(obj)
            self._all.append(obj)


if __name__ == "__main__":
    xml_example = """
    <root>
        <section id="1" pIn="1П" zIn="1з" />
        <way id="411" pIn="411П" zIn="411з" />
        <switch id="1" pkIn="1ПК" mkIn="1МК" />
        <signal id="411пЛ" redIn="411КО" greenIn="411РО" yellowIn="411ЖО" blueIn="411БО" />
    </root>
    """

    factory = ObjectFactory()
    factory.load_from_string(xml_example)

    print("Sections:", factory.sections)
    print("Ways:", factory.ways)
    print("Switches:", factory.switches)
    print("Signals:", factory.signals)
    print("All:", factory.all_objects)

