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
        self.trie_province = self.build_trie_with_abbreviations('list_province.txt', type="province")
        self.trie_district = self.build_trie('list_district.txt')
        self.trie_ward = self.build_trie('list_ward.txt')
        pass

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
    normal_map_2 = {
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
    telex_map = {
        'ă': 'aw', 'ắ': 'aws', 'ằ': 'awf', 'ẳ': 'awr', 'ẵ': 'awx', 'ặ': 'awj',
        'â': 'aa', 'ấ': 'aas', 'ầ': 'aaf', 'ẩ': 'aar', 'ẫ': 'aax', 'ậ': 'aaj',
        'á': 'as','á': 'as', 'à': 'af', 'ả': 'ar', 'ã': 'ax', 'ạ': 'aj',
        'é': 'es', 'è': 'ef', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej',
        'ê': 'ee', 'ế': 'ees', 'ề': 'eef', 'ể': 'eer', 'ễ': 'eex', 'ệ': 'eej',
        'í': 'is', 'ì': 'if', 'ỉ': 'ir', 'ĩ': 'ix', 'ị': 'ij',
        'ó': 'os', 'ò': 'of', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj',
        'ô': 'oo', 'ố': 'oos', 'ồ': 'oof', 'ổ': 'oor', 'ỗ': 'oox', 'ộ': 'ooj',
        'ơ': 'ow', 'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
        'ú': 'us', 'ù': 'uf', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj',
        'ư': 'uw', 'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
        'ý': 'ys', 'ỳ': 'yf', 'ỷ': 'yr', 'ỹ': 'yx', 'ỵ': 'yj',
        'đ': 'dd'
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

        def insert(self, word, full_name):
            node = self.root
            for char in word:
                if char not in node.children:
                    node.children[char] = Solution.TrieNode()  # Access TrieNode through Solution
                node = node.children[char]
            node.is_end_of_word = True
            node.full_name = full_name

        def search(self, word):
            node = self.root
            for char in word:
                if char in node.children:
                    node = node.children[char]
                else:
                    return ""  # Không tìm thấy
            if node.is_end_of_word:
                return node.full_name
            else:
                return ""  # Không tìm thấy

    def build_trie(self, file_path, type="ward"):
        trie = self.Trie(self)  # Pass 'self' as the outer_instance
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = []
            for line in file:
                full_name = line.strip()
                # Replace special characters with spaces and remove duplicate spaces
                full_name_one_space = re.sub(r'[.,-]', ' ', full_name)
                full_name_one_space = re.sub(r'\s+', ' ', full_name_one_space).strip()
                normalized_name = self.reverse_string(self.convert_to_vni(full_name_one_space.lower()))
                lines.append((normalized_name, full_name))
            for line in lines:
                trie.insert(line[0], line[1])  # Store the original full_name
                if type == "province":
                    trie.insert(line[0]+"t", line[1])
                if len(normalized_name) > 3:
                    # Generate and insert similar words differing by one to 2 characters
                    similar_words = self.generate_similar_words(normalized_name, max_distance=1)
                    for word in similar_words: 
                        if word not in lines:
                            trie.insert(word, line[1])
            for line in lines:
                trie.insert(line[0].replace(" ", ""), line[1])
        return trie

    def build_trie_with_abbreviations(self, file_path, type = "ward"):
        trie = self.build_trie(file_path, type=type)
        # Adding common abbreviations
        abbreviations = {
            "hcm": "Hồ Chí Minh",
            "tphcm": "Hồ Chí Minh",
            "hn": "Hà Nội",
        }
        for abbr, full_name in abbreviations.items():
            normalized_abbr = self.reverse_string(self.convert_to_vni(abbr))
            trie.insert(normalized_abbr, full_name)

            if len(normalized_abbr) > 3:
                # Generate and insert similar words differing by one to 2 characters
                similar_words = self.generate_similar_words(normalized_abbr, max_distance=1)
                for word in similar_words:
                    trie.insert(word, full_name)
        return trie

    def generate_similar_words(self, word, max_distance=1):
        """Generate words that differ by 1 to max_distance characters."""
        similar_words = set()
        for dist in range(1, max_distance + 1):
            self._generate_similar_words_helper(word, dist, similar_words)
        return list(similar_words)

    def _generate_similar_words_helper(self, word, distance, similar_words):
        """Helper function to generate words with a specific edit distance."""
        if distance == 0:
            similar_words.add(word)
            return

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz0123456789':  # Including digits for more flexibility
                if c != word[i]:
                    similar_word = word[:i] + c + word[i+1:]
                    self._generate_similar_words_helper(similar_word, distance - 1, similar_words)

    def normalize_input(self, address):
        """Normalize the address by removing special characters and unwanted keywords, then convert to VNI format."""
        # Convert the string to lowercase
        address = address.lower()

        # Remove specific keywords, including those with diacritics
        keywords = ["x", "tx", "tt", "h", "tp", "q", "p",
                    "xa", "xã", "thi xa", "thị xã", "thi tran", "thị trấn",
                    "huyen", "huyện", "tinh", "tỉnh", "thanh pho", "thành phố",
                     "quận", "phuong", "phường", "t"]
        pattern = r'\b(?:' + '|'.join(keywords) + r')\b'
        address = re.sub(pattern, ' ', address).strip()

        force_remove = ["thị xã", "thi tran", "thị trấn",
                    "huyện", "tỉnh", "thanh pho", "thành phố",
                    "quận", "phường"]
        for word in force_remove:
            address = address.replace(word, ' ')

        # Remove only "p" and "q" when followed by one or two digits, leave the digits alone
        pattern_pq_digit = r'\b([pq])(\d{1,2})\b'
        address = re.sub(pattern_pq_digit, r'\2', address).strip()
        
        # Replace special characters with spaces
        address = re.sub(r'[.,-]', ' ', address)
        # Remove duplicate spaces
        address = re.sub(r'\s+', ' ', address).strip()

         

        # Convert to VNI format
        normalized = self.convert_to_vni(address).strip()
        # Reverse the normalized string
        reversed_normalized = self.reverse_string(normalized)
        return reversed_normalized

    def search_and_update(self, trie, words, search_type):
        """
        Search for the best match in the trie for a concatenation of up to 4 words.
        If a match is found, return the match and the remaining words after the match.
        """
        max_words = 4
        for i in range(len(words)):
            for j in range(i + 1, min(i + 1 + max_words, len(words) + 1)):
                search_string = ' '.join(words[i:j])  # Join words with spaces
                match = trie.search(search_string)
                if match:
                    return match, words[:i] + words[j:]
        return "", words

    def search_ward(self, trie, words):
        """
        Search for the best match for the ward in the trie by gradually increasing the number of words joined.
        """
        longest_match = ""
        for i in range(len(words)):
            search_string = ' '.join(words[:i + 1])  # Join words with spaces
            ward_match = trie.search(search_string)
            #print(f"*** search_ward: {search_string}")
            if ward_match:
                longest_match = ward_match
        return longest_match

    def split_address(self, trie_province, trie_district, trie_ward, address):
        normalized_address = self.normalize_input(address)
        print(f"= normalized_address: {normalized_address}")
        province, district, ward = None, None, None
        # Split the reversed normalized input into words
        words = normalized_address.split()
        # Search for province
        province, remaining_words = self.search_and_update(trie_province, words, "province")
        if province:
            words = remaining_words
        # Search for district
        district, remaining_words = self.search_and_update(trie_district, words, "district")
        if district:
            words = remaining_words
        # Search for ward
        ward = self.search_ward(trie_ward, words)
        print(f"= address: {address}")
        print(f"= province: {province}")
        print(f"= district: {district}")
        print(f"= ward: {ward}")
        print(f"=============================")
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
