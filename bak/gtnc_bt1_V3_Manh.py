#                    _oo0oo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                   0\  =  /0
#                 ___/`---'\___
#               .' \\|     |// '.
#              / \\|||  :  |||// \
#             / _||||| -:- |||||- \
#            |   | \\\  -  /// |   |
#            | \_|  ''\---/''  |_/ |
#            \  .-\__  '-'  ___/-. /
#          ___'. .'  /--.--\  `. .'___
#       ."" '<  `.___\_<|>_/___.' >' "".
#      | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#      \  \ `_.   \_ __\ /__ _/   .-` /  /
#  =====`-.____`.___ \_____/___.-`___.-'=====
#                    `=---='

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     Buddha blesses   No More BUG below
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


import re
import time

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.full_name = None

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, full_name):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.full_name = full_name
    
    def search(self, word):
        return self._search_recursive(self.root, word, "", float('inf'), "")
    
    def _search_recursive(self, node, word, current, min_distance, best_match):
        if node.is_end_of_word:
            distance = levenshtein_distance(word, current)
            if distance < min_distance:
                min_distance = distance
                best_match = node.full_name
        for char, next_node in node.children.items():
            result = self._search_recursive(next_node, word, current + char, min_distance, best_match)
            if result[1] < min_distance:
                min_distance = result[1]
                best_match = result[0]
        return best_match, min_distance

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s1) == 0:
        return len(s2)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def build_trie(file_path):
    trie = Trie()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            full_name = line.strip()
            normalized_name = re.sub(r'[^\w\s]', '', full_name).lower().strip()
            trie.insert(normalized_name, full_name)
    return trie

def normalize_input(address):
    normalized = re.sub(r'[^\w\s]', '', address).lower().strip()
    return normalized

def split_address(trie_province, trie_district, trie_ward, address):
    start_time = time.time()
    
    normalized_address = normalize_input(address)
    words = normalized_address.split()
    province, district, ward = None, None, None
    
    province_match, _ = trie_province.search(' '.join(words))
    if province_match:
        province = province_match
        province_words = province.lower().split()
        words = [word for word in words if word not in province_words]
        
    district_match, _ = trie_district.search(' '.join(words))
    if district_match:
        district = district_match
        district_words = district.lower().split()
        words = [word for word in words if word not in district_words]
    
    ward_match, _ = trie_ward.search(' '.join(words))
    if ward_match:
        ward = ward_match
    
    elapsed_time = time.time() - start_time
    return ward, district, province, elapsed_time

trie_province = build_trie('list_province.txt')
trie_district = build_trie('list_district.txt')
trie_ward = build_trie('list_ward.txt')

address = "X. Thuận Thành, H. Cần Giuộc, T. Long An"

# Example of making multiple requests
requests = [address] * 10  # replace with actual list of requests
total_time = 0

for req in requests:
    ward, district, province, elapsed_time = split_address(trie_province, trie_district, trie_ward, req)
    total_time += elapsed_time
    print(f"Xã/Phường: {ward}")
    print(f"Huyện/Quận: {district}")
    print(f"Tỉnh/Thành phố: {province}")
    print(f"Thời gian xử lý: {elapsed_time:.6f} giây")

average_time = total_time / len(requests)
print(f"Thời gian trung bình cho mỗi yêu cầu: {average_time:.6f} giây")
