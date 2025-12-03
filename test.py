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

matrix = [[i * 4 + j for j in range(4)] for i in range(5)]
# выводим массив построчно с отступами
for row in matrix:
   print(' '.join(map(str, row)))