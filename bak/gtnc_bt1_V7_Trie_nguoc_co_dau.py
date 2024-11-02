from fuzzywuzzy import fuzz
import re
import time
import unicodedata

vni_map = {
    'ă': 'a8', 'ắ': 'a81', 'ằ': 'a82', 'ẳ': 'a83', 'ẵ': 'a84', 'ặ': 'a85',
    'â': 'a6', 'ấ': 'a61', 'ầ': 'a62', 'ẩ': 'a63', 'ẫ': 'a64', 'ậ': 'a65',
    'á': 'a1', 'à': 'a2', 'ả': 'a3', 'ã': 'a4', 'ạ': 'a5',
    'é': 'e1', 'è': 'e2', 'ẻ': 'e3', 'ẽ': 'e4', 'ẹ': 'e5',
    'ê': 'e6', 'ế': 'e61', 'ề': 'e62', 'ể': 'e63', 'ễ': 'e64', 'ệ': 'e65',
    'í': 'i1', 'ì': 'i2', 'ỉ': 'i3', 'ĩ': 'i4', 'ị': 'i5',
    'ó': 'o1', 'ò': 'o2', 'ỏ': 'o3', 'õ': 'o4', 'ọ': 'o5',
    'ô': 'o6', 'ố': 'o61', 'ồ': 'o62', 'ổ': 'o63', 'ỗ': 'o64', 'ộ': 'o65',
    'ơ': 'o7', 'ớ': 'o71', 'ờ': 'o72', 'ở': 'o73', 'ỡ': 'o74', 'ợ': 'o75',
    'ú': 'u1', 'ù': 'u2', 'ủ': 'u3', 'ũ': 'u4', 'ụ': 'u5',
    'ư': 'u7', 'ứ': 'u71', 'ừ': 'u72', 'ử': 'u73', 'ữ': 'u74', 'ự': 'u75',
    'ý': 'y1', 'ỳ': 'y2', 'ỷ': 'y3', 'ỹ': 'y4', 'ỵ': 'y5',
    'đ': 'd9'
}

def convert_to_vni(text):
    """Convert Vietnamese characters to VNI encoding."""
    return ''.join(vni_map.get(c, c) for c in text)

def normalize_input(address):
    """Normalize the address by removing special characters and unwanted keywords, then convert to VNI format."""
    # Convert the string to lowercase
    address = address.lower()
    
    # Remove specific keywords, including those with diacritics
    keywords = ["x", "tx", "tt", "h", "t", "tp", "q", "p", 
                "xa", "xã", "thi xa", "thị xã", "thi tran", "thị trấn", 
                "huyen", "huyện", "tinh", "tỉnh", "thanh pho", "thành phố", 
                "quan", "quận", "phuong", "phường"]
    pattern = r'\b(?:' + '|'.join(keywords) + r')\b'
    address = re.sub(pattern, '', address).strip()
    # Replace special characters with spaces
    address = re.sub(r'[.,-]', ' ', address)
    # Remove duplicate spaces
    address = re.sub(r'\s+', ' ', address).strip()
    # Convert to VNI format
    normalized = convert_to_vni(address).strip()
    # Reverse the normalized string
    reversed_normalized = reverse_string(normalized)
    return reversed_normalized

def fuzzy_edit_distance(s1, s2):
    """Calculate the edit distance between two strings."""
    m, n = len(s1), len(s2)
    if abs(m - n) > 1:  # Quick check for early exit
        return max(m, n)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

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

    def _search_recursive(self, node, word, index, min_distance, best_match):
        if node.is_end_of_word:
            if len(word) <= 2:
                if word == index:  # Exact match for short words
                    best_match = node.full_name
                    min_distance = 0
            else:
                distance = fuzzy_edit_distance(word, index)
                if distance <= 1 and distance < min_distance:  # Accepting a difference of up to 1 character
                    min_distance = distance
                    best_match = node.full_name
        for char, next_node in node.children.items():
            new_best_match, new_min_distance = self._search_recursive(next_node, word, index + char, min_distance, best_match)
            if new_min_distance < min_distance:
                min_distance = new_min_distance
                best_match = new_best_match
        return best_match, min_distance

    def search(self, word):
        return self._search_recursive(self.root, word, "", float('inf'), "")

def reverse_string(s):
    return s[::-1]

def build_trie(file_path):
    trie = Trie()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            full_name = line.strip()
            # Replace special characters with spaces and remove duplicate spaces
            full_name_one_space = re.sub(r'[.,-]', ' ', full_name)
            full_name_one_space = re.sub(r'\s+', ' ', full_name_one_space).strip()
            normalized_name = reverse_string(convert_to_vni(full_name_one_space.lower()))
            trie.insert(normalized_name, full_name)  # Store the original full_name
    return trie

def build_trie_with_abbreviations(file_path):
    trie = build_trie(file_path)
    # Adding common abbreviations
    trie.insert(reverse_string(convert_to_vni("hcm")), "Hồ Chí Minh")
    trie.insert(reverse_string(convert_to_vni("tphcm")), "Hồ Chí Minh")
    trie.insert(reverse_string(convert_to_vni("hn")), "Hà Nội")
    return trie

def search_and_update(trie, words, search_type):
    """
    Search for the best match in the trie for a concatenation of up to 4 words.
    If a match is found, return the match and the remaining words after the match.
    """
    max_words = 4
    for i in range(len(words)):
        for j in range(i + 1, min(i + 1 + max_words, len(words) + 1)):
            search_string = ' '.join(words[i:j])  # Join words with spaces
            match, _ = trie.search(search_string)
            if match:
                return match, words[:i] + words[j:]
    return None, words

def search_ward(trie, words):
    """
    Search for the best match for the ward in the trie by gradually increasing the number of words joined.
    """
    longest_match = ""
    for i in range(len(words)):
        search_string = ' '.join(words[:i + 1])  # Join words with spaces
        ward_match, _ = trie.search(search_string)
        print(f"*** search_ward: {search_string}")
        if ward_match:
            longest_match = ward_match
    return longest_match

def split_address(trie_province, trie_district, trie_ward, address):
    """
    Split the address into province, district, and ward by searching in the respective tries.
    """
    start_time = time.time()
    normalized_address = normalize_input(address)
    print(f"*** normalized_address: {normalized_address}")
    province, district, ward = None, None, None

    # Split the reversed normalized input into words
    words = normalized_address.split()
    print(f"reversed normalized splited input  : {words}")

    # Search for province
    province, remaining_words = search_and_update(trie_province, words, "province")
    if province:
        words = remaining_words

    # Search for district
    district, remaining_words = search_and_update(trie_district, words, "district")
    if district:
        words = remaining_words

    # Search for ward
    ward = search_ward(trie_ward, words)
    print(f"search_ward: {ward}")

    elapsed_time = time.time() - start_time
    return ward, district, province, elapsed_time

# Update your trie initialization to use the new function
trie_province = build_trie_with_abbreviations('list_province_db.txt')
trie_district = build_trie('list_district_db.txt')
trie_ward = build_trie('list_ward_db.txt')

requests = [
    "X. Thuận Thành, H. Cần Giuộc, T. Long An",
    "P. Bến Nghé, Q. 1, TPHCM",
    "X. Bình Mỹ, H. Củ Chi, TPHCM",
    "X. An Bình, H. Cao Lãnh, T. Đồng Tháp",
    "Phú Lợi, Tp. Thủ Dầu Một, Bình Dương",
    "P. 7, Q. Gò Vấp, TPHCM",
    "X. Tân Phú Trung, H. Củ Chi, TPHCM",
    "P. 14, Q. Phú Nhuận, TPHCM",
    "Ngãi Giao, Châu Đức, Tỉnh Bà Rịa - Vũng Tàu"
]



total_time = 0
for req in requests:
    start_time = time.time()
    ward, district, province, elapsed_time = split_address(trie_province, trie_district, trie_ward, req)
    total_time += elapsed_time
    print(f"Address: {req}")
    print(f"Xã/Phường: {ward}")
    print(f"Huyện/Quận: {district}")
    print(f"Tỉnh/Thành phố: {province}")
    print(f"Thời gian xử lý: {elapsed_time:.6f} giây")
    print(f"=================================================")
average_time = total_time / len(requests)
print(f"Thời gian trung bình cho mỗi yêu cầu: {average_time:.6f} giây")
