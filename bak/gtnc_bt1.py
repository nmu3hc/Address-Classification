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
        # Nếu đây là từ đầy đủ, tính khoảng cách và cập nhật kết quả tốt nhất
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

    # trường hợp cơ sở
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

def build_trie(dictionary):
    trie = Trie()
    for word, full_name in dictionary.items():
        trie.insert(word, full_name)
    return trie

def normalize_input(address):
    import re
    # Loại bỏ các ký tự không cần thiết và chuyển thành chữ thường
    normalized = re.sub(r'[^\w\s]', '', address).lower().strip()
    return normalized

def split_address(trie_province, trie_district, trie_ward, address):
    normalized_address = normalize_input(address)
    words = normalized_address.split()

    province, district, ward = None, None, None
    
    # Tìm kiếm tỉnh
    province_match, _ = trie_province.search(' '.join(words))
    if province_match:
        province = province_match
        province_words = province.lower().split()
        words = [word for word in words if word not in province_words]
    
    # Tìm kiếm huyện
    district_match, _ = trie_district.search(' '.join(words))
    if district_match:
        district = district_match
        district_words = district.lower().split()
        words = [word for word in words if word not in district_words]

    # Tìm kiếm xã
    ward_match, _ = trie_ward.search(' '.join(words))
    if ward_match:
        ward = ward_match

    return ward, district, province

# Xây dựng từ điển trie không dấu và ánh xạ tới tên đầy đủ có dấu
province_dict = {
    "tinh long an": "Tỉnh Long An",
    "thanh pho ho chi minh": "Thành phố Hồ Chí Minh"
}

district_dict = {
    "huyen can giuoc": "Huyện Cần Giuộc",
    "quan 1": "Quận 1"
}

ward_dict = {
    "xa thuan thanh": "Xã Thuận Thành",
    "phuong ben nghe": "Phường Bến Nghé"
}

trie_province = build_trie(province_dict)
trie_district = build_trie(district_dict)
trie_ward = build_trie(ward_dict)

# Chuỗi địa chỉ ví dụ
address = "X. Thuận Thành, H. Cần Giuộc, T. Long An"

# Phân tách địa chỉ
ward, district, province = split_address(trie_province, trie_district, trie_ward, address)
print(f"Xã/Phường: {ward}")
print(f"Huyện/Quận: {district}")
print(f"Tỉnh/Thành phố: {province}")
