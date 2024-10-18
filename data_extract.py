import json

def read_json(file_path: str):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Example usage
file_path = 'raw.json'
data = read_json(file_path)
provinces = []
districts = []
wards = []
for province in data:
    provinces.append(province['Name'])
    for district in province['District']:
        districts.append(district['Name'])
        for ward in district['Ward']:
            wards.append(ward['Name'])
with open('list_province.txt', 'w') as file:
    for province in set(provinces):
        file.write(province + '\n')
    file.close()
with open('list_district.txt', 'w') as file:
    for district in set(districts):
        file.write(district + '\n')
    file.close()
with open('list_ward.txt', 'w') as file:    
    for ward in set(wards):
        file.write(ward + '\n')
    file.close()