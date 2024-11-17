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



# NOTE: you CAN change this cell
# import your library here
import re
import time
import unicodedata

# NOTE: you MUST change this cell
# New methods / functions must be written under class Solution.
class Solution:
    
    def __init__(self):
        # list provice, district, ward for private test, do not change for any reason

        self.province_path = 'list_province.txt'
        self.district_path = 'list_district.txt'
        self.ward_path = 'list_ward.txt'

        # write your preprocess here, add more method if needed
        self.trie_province = self.build_trie('list_province_db.txt')
        self.trie_district = self.build_trie('list_district_db.txt')
        self.trie_ward = self.build_trie('list_ward_db.txt')

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

    normal_map = {
        'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'đ': 'd'
    }

    def convert_to_vni(self, text):
        """Convert Vietnamese characters to VNI encoding."""
        return ''.join(self.normal_map.get(c, c) for c in text)

    def reverse_string(self, s):
        return s[::-1]

    

    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end_of_word = False
            self.full_name = None

    class Trie:
        def __init__(self, outer_instance):  # Pass outer_instance during initialization
            self.root = Solution.TrieNode()  # Access TrieNode through Solution
            self.outer_instance = outer_instance  # Store outer_instance
            self.translate_with_dialect = {}

        def insert(self, word, full_name):
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = Solution.TrieNode()  # Access TrieNode through Solution
                node = node.children[char]
            node.is_end_of_word = True
            if node.full_name is None:
                node.full_name = full_name
            else:
                if node.full_name in self.translate_with_dialect.keys():
                    self.translate_with_dialect[node.full_name].append(full_name)
                else:
                    self.translate_with_dialect[node.full_name] = [node.full_name, full_name]
        def search(self, word):
            node = self.root
            best_match = ""
            for char in word:
                if char in node.children:
                    node = node.children[char]
                else:
                    break  # Dừng duyệt nếu không tìm thấy ký tự
                if node.is_end_of_word:
                    best_match = node.full_name
            return best_match

    def build_trie(self, file_path):
        trie = self.Trie(self)  # Pass 'self' as the outer_instance
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                full_name = line.strip()
                #trie.insert(full_name, full_name)
                normalized_name = self.normalize_input(full_name)
                normalized_name = re.sub(r'\s+', '', normalized_name).strip()
                trie.insert(normalized_name, full_name)  # Store the original full_name

        # Adding common abbreviations
        if file_path == 'list_province_db.txt':
            abbreviations = {
                "hcm": "Hồ Chí Minh",
                "tphcm": "Hồ Chí Minh",
                "H.C.Minh": "Hồ Chí Minh",
                "hn": "Hà Nội",
                "hnoi": "Hà Nội",  
                "Thanh Hoá": "Thanh Hóa",
                "Quảyg Nm" : "Quảng Nam",
                "TGiang" : "Tiền Giang",
                "Thừa.t.Huế": "Thừa Thiên Huế",
                "T.T.H": "Thừa Thiên Huế",
            }
            for abbr, full_name in abbreviations.items():
                normalized_abbr = self.normalize_input(abbr)
                normalized_abbr = re.sub(r'\s+', '', normalized_abbr).strip()
                trie.insert(normalized_abbr, full_name)
        if file_path == 'list_district_db.txt':
            abbreviations = {
                "TB": "Tân Bình",
                "BT": "Bình Thạnh",
                "C/Giấy": "Cầu Giấy",
                "GV": "Gò Vấp",
                "BC": "Bình Chánh"
            }
            for abbr, full_name in abbreviations.items():
                normalized_abbr = self.normalize_input(abbr)
                normalized_abbr = re.sub(r'\s+', '', normalized_abbr).strip()
                trie.insert(normalized_abbr, full_name)
        if file_path == 'list_ward_db.txt':
            abbreviations = {
                "PP": "Phong Phú",
            }
            for abbr, full_name in abbreviations.items():
                normalized_abbr = self.normalize_input(abbr)
                normalized_abbr = re.sub(r'\s+', '', normalized_abbr).strip()
                trie.insert(normalized_abbr, full_name)
        # print(trie.translate_with_dialect)
        return trie



    def normalize_input(self, address):
        """Normalize the address by removing special characters and unwanted keywords, then convert to VNI format."""
        # Convert the string to lowercase
        address = address.lower()
        # Replace special characters with spaces
        address = re.sub(r'[.,-]', ' ', address)
        not_vn_chars = ["w", "z", "j"]
        for char in not_vn_chars:
            # Escape special characters using re.escape
            address = re.sub(re.escape(char), '', address)
        # Add spaces around the address to handle edge cases
        address = " " + address + " "

        # Remove specific keywords, including those with diacritics
        keywords = ["x", "tx", "tt", "h", "t", "tp", "q", "p",
                    "xa", "xã", "thi xa", "thị xã", "thixa", "thi tran", "thitran", "thị trấn",
                    "huyen", "huyện", "tỉnh", "thanh pho", "thanhpho", "thành phố",
                    "quận", "phuong", "phường"]
        pattern = r'\b(?:' + '|'.join(keywords) + r')\b'
        address = re.sub(pattern, ' ', address)

        # Remove adjacent keyword combinations
        adjacent_keywords = ["tx", "tp", "xa", "xã", "thi xa", "thị xã", "thixa", "thi tran", "thitran", "thị trấn",
                    "huyen", "huyện", "tỉnh", "thanhpho", "thành phố", "quận", "phường", "thà6nh phố", "phố"]
        for word in adjacent_keywords:
            address = re.sub(word, ' ', address)
        # Remove duplicate spaces
        address = re.sub(r'\s+', ' ', address).strip()
        # Convert to VNI format
        normalized = self.convert_to_vni(address).strip()
        replacements = {
            "aa": "a", "bb": "b", "cc": "c", "dd": "d", "ee": "e", "gg": "g", "hh": "h",
            "ii": "i", "kk": "k", "ll": "l", "mm": "m", "nn": "n", "oo": "o", "pp": "p",
            "qq": "q", "rr": "r", "ss": "s", "tt": "t", "uu": "u", "vv": "v", "xx": "x", "yy": "y",
            "kh": "h"
        }
        for old, new in replacements.items():
            normalized = re.sub(old, new, normalized)

        # Reverse the normalized string
        reversed_normalized = self.reverse_string(normalized)
        return reversed_normalized

    def levenshtein_distance(self, node, word, prev_row, min_cost, max_cost=3):
        current_row = [prev_row[0] + 1]
        for i in range(1, len(prev_row)):
            insert_cost = current_row[i - 1] + 1
            delete_cost = prev_row[i] + 1
            replace_cost = prev_row[i - 1] + (word[i - 1] != node)
            current_row.append(min(insert_cost, delete_cost, replace_cost))
            if min(insert_cost, delete_cost, replace_cost) > max_cost:
                return  # Dừng tính toán nếu chi phí vượt quá max_cost
        if current_row[-1] < min_cost[0]:
            min_cost[0] = current_row[-1]
        if min_cost[0] <= max_cost:
            for char in node.children:
                self.levenshtein_distance(node.children[char], word, current_row, min_cost, max_cost)



    def search_and_update(self, trie, words, search_type, raw = ""):
        """
        Search for the best match in the trie for a concatenation of up to 4 words.
        If a match is found, return the match and the remaining words after the match.
        """
        max_words = 4
        for i in range(len(words)):
            for j in range(i + 1, min(i + 1 + max_words, len(words) + 1)):
                search_string = ' '.join(words[i:j])  # Join words with spaces
                search_string = re.sub(r'\s+', '', search_string).strip()
                match = trie.search(search_string)
                if match:
                    if match in trie.translate_with_dialect.keys():
                            for matching in trie.translate_with_dialect[match]:
                                if matching.lower() in raw.lower():
                                    return matching, words[j:]
                            match = trie.translate_with_dialect[match][0]
                    return match, words[j:]

        # If not found, use Levenshtein distance to search (limited to 3 character differences for strings longer than 5 characters)
        min_cost = [float('inf')]
        best_match = ""
        for i in range(len(words)):
            for j in range(i + 1, min(i + 1 + max_words, len(words) + 1)):
                search_string = ' '.join(words[i:j])
                search_string = re.sub(r'\s+', '', search_string).strip()
                if len(search_string) > 3:
                    prev_row = list(range(len(search_string) + 1))
                    max_cost = min(len(search_string) // 2, 5)
                    self.levenshtein_distance(trie.root, search_string, prev_row, min_cost, max_cost)
                    if min_cost[0] <= 3:
                        best_match = search_string
                        if best_match in trie.translate_with_dialect.keys():
                            for matching in trie.translate_with_dialect[best_match]:
                                if matching.lower() in raw.lower():
                                    return matching, words[j:]
                            best_match = trie.translate_with_dialect[best_match][0]
                        
                        return best_match, words[j:]
        return "", words

    def search_ward(self, trie, words, raw = ""):
        """
        Search for the best match for the ward in the trie by gradually increasing the number of words joined.
        """
        longest_match = ""
        for i in range(len(words)):
            search_string = ' '.join(words[:i + 1])  # Join words with spaces
            search_string = re.sub(r'\s+', '', search_string).strip()
            ward_match = trie.search(search_string)
            if ward_match:
                longest_match = ward_match

        # If not found, use Levenshtein distance to search (limited to 3 character differences for strings longer than 3 characters)
        if not longest_match:
            min_cost = [float('inf')]
            best_match = ""
            for i in range(len(words)):
                search_string = ' '.join(words[:i + 1])
                search_string = re.sub(r'\s+', '', search_string).strip()
                if len(search_string) > 3:
                    prev_row = list(range(len(search_string) + 1))
                    max_cost = min(len(search_string) // 2, 10)
                    self.levenshtein_distance(trie.root, search_string, prev_row, min_cost, max_cost)
                    if min_cost[0] <= 3:
                        best_match = search_string
                        longest_match = best_match
        if longest_match in trie.translate_with_dialect.keys():
            for matching in trie.translate_with_dialect[longest_match]:
                if matching.lower() in raw.lower():
                    return matching
            longest_match = trie.translate_with_dialect[longest_match][0]
    
        return longest_match

    def split_address(self, trie_province, trie_district, trie_ward, address):
        normalized_address = self.normalize_input(address)
        print(f"== normalized_address: {normalized_address}")
        province, district, ward = "", "", ""
        # Split the reversed normalized input into words
        words = normalized_address.split()
        # Search for province
        province, remaining_words = self.search_and_update(trie_province, words, "province", address)
        if province:
            words = remaining_words
        # Search for district
        district, remaining_words = self.search_and_update(trie_district, words, "district", address)
        if district:
            words = remaining_words
        # Search for ward
        #ward, remaining_words = self.search_and_update(trie_ward, words, "ward")
        ward = self.search_ward(trie_ward, words, address)
        print(f"  {{")
        print(f"    \"text\": \"{address}\",")
        print(f"    \"result\": {{")
        print(f"      \"province\": \"{province}\",")
        print(f"      \"district\": \"{district}\",")
        print(f"      \"ward\": \"{ward}\"")
        print(f"    }}")
        print(f"  }},")

        return ward, district, province


    def process(self, s: str):
        # write your process string here
        ward, district, province = self.split_address(self.trie_province, self.trie_district, self.trie_ward, s)
        return {
            "province": province,
            "district": district,
            "ward": ward,
        }
    
# NOTE: DO NOT change this cell
# This cell is for scoring
import datetime
TEAM_NAME = 'DEFAULT_NAME'  # This should be your team name
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
EXCEL_FILE = f'{TEAM_NAME}_{current_time}.xlsx'

import json
import time
with open('test.json') as f:
    data = json.load(f)

summary_only = True
df = []
solution = Solution()
timer = []
correct = 0
for test_idx, data_point in enumerate(data):
    address = data_point["text"]

    ok = 0
    try:
        start = time.perf_counter_ns()
        result = solution.process(address)
        answer = data_point["result"]
        finish = time.perf_counter_ns()
        timer.append(finish - start)
        ok += int(answer["province"] == result["province"])
        ok += int(answer["district"] == result["district"])
        ok += int(answer["ward"] == result["ward"])
        df.append([
            test_idx,
            address,
            answer["province"],
            result["province"],
            int(answer["province"] == result["province"]),
            answer["district"],
            result["district"],
            int(answer["district"] == result["district"]),
            answer["ward"],
            result["ward"],
            int(answer["ward"] == result["ward"]),
            ok,
            timer[-1] / 1_000_000_000,
        ])
    except Exception as e:
        df.append([
            test_idx,
            address,
            answer["province"],
            "EXCEPTION",
            0,
            answer["district"],
            "EXCEPTION",
            0,
            answer["ward"],
            "EXCEPTION",
            0,
            0,
            0,
        ])
        # any failure count as a zero correct
        pass
    correct += ok


    if not summary_only:
        # responsive stuff
        print(f"Test {test_idx:5d}/{len(data):5d}")
        print(f"Correct: {ok}/3")
        print(f"Time Executed: {timer[-1] / 1_000_000_000:.4f}")


print(f"-"*30)
total = len(data) * 3
score_scale_10 = round(correct / total * 10, 2)
if len(timer) == 0:
    timer = [0]
max_time_sec = round(max(timer) / 1_000_000_000, 4)
avg_time_sec = round((sum(timer) / len(timer)) / 1_000_000_000, 4)

import pandas as pd

df2 = pd.DataFrame(
    [[correct, total, score_scale_10, max_time_sec, avg_time_sec]],
    columns=['correct', 'total', 'score / 10', 'max_time_sec', 'avg_time_sec',],
)

columns = [
    'ID',
    'text',
    'province',
    'province_student',
    'province_correct',
    'district',
    'district_student',
    'district_correct',
    'ward',
    'ward_student',
    'ward_correct',
    'total_correct',
    'time_sec',
]

df = pd.DataFrame(df)
df.columns = columns

print(f'{TEAM_NAME = }')
print(f'{EXCEL_FILE = }')
print(df2)

writer = pd.ExcelWriter(EXCEL_FILE, engine='xlsxwriter')
df2.to_excel(writer, index=False, sheet_name='summary')
df.to_excel(writer, index=False, sheet_name='details')
writer.close()
