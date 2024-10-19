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

#####################################################################
################## This section contains Parameters #################
#####################################################################

preprocess_string_dialect = "telex"
"""
ways to embed dialects\n
possible values: "telex", "vni", "none"
"""

search_algorithm = "edit_distance"
"""
The search algorithm to use\n
possible values: "levenshtein", "edit_distance"
"""

input_separate_algorithm = "brute_force"
"""
The algorithm to separate the input\n
possible values: "brute_force"
"""

province_edit_distance_threshold = 5
"""
The maximum edit distance to search for provinces\n
"""
district_edit_distance_threshold = 5
"""
The maximum edit distance to search for districts\n
"""
ward_edit_distance_threshold = 5
"""
The maximum edit distance to search forwards\n
"""

debug = "VERBOSE"
"""
debug options\n 
possible values: "VERBOSE", "NORMAL", "QUIET"
"""

#####################################################################
######## This section contains fucntions for processing Data ########
#####################################################################

def get_all_parameters() -> str:
    return{
        "preprocess_string_dialect": preprocess_string_dialect,
        "search_algorithm": search_algorithm,
        "input_separate_algorithm": input_separate_algorithm,
        "province_edit_distance_threshold": province_edit_distance_threshold,
        "district_edit_distance_threshold": district_edit_distance_threshold,
        "ward_edit_distance_threshold": ward_edit_distance_threshold
    }
def measure_runtime(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

#####################################################################
######## This section contains fucntions for processing Data ########
#####################################################################

def vietnamese_normalize_dialect(text: str) -> str:
    """
    Function to convert Vietnamese characters to normal characters\n
    Input:    text : str - The text to convert\n
    Output:          str - The converted text\n
    Can be manipulated by changing the preprocess_string_dialect parameter 
    """
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
    
    # Convert the text
    if preprocess_string_dialect == "telex":
        # Using Telex embedding 
        converted_text = ''.join(telex_map.get(char, char) for char in text)
    elif preprocess_string_dialect == "vni":
        # Using VNI embedding 
        converted_text = ''.join(vni_map.get(char, char) for char in text)
    else:
        converted_text = text
        # MISRA shenanigans ~~~
    return converted_text

def preprocess_string(text: str) -> str:
    # Remove special characters and convert to lowercase
    normalized = re.sub(r'[^\w\s]', '', text).lower().strip()
    return vietnamese_normalize_dialect(normalized)


#####################################################################
############# This section contains Trie implementation #############
#####################################################################

class TrieNode:
    def __init__(self):
        """
        Trie Node class\n
        Full name of the word is stored in the end of node\n
        """
        self.children = {}
        self.is_end_of_word = False
        self.full_name = None

class Trie:
    """
    Trie implementation in Python with insert and search functions
    """
    def __init__(self)-> None:
        self.root = TrieNode()
        self.max_edit_distance = province_edit_distance_threshold

    def insert(self, word, full_name)-> bool:
        """
        Insert a word into the Trie\n
        Input:    word : str - The word to insert\n
                  full_name : str - The full name of the word\n
        Output:   bool - True if the word is inserted successfully\n
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.full_name = full_name
        return True

    def search(self, word: str)-> str:
        if search_algorithm == "levenshtein":
            return self.search_laveshtein_distance(word)
        elif search_algorithm == "edit_distance":
            return self.search_with_edit_distance(word, self.max_edit_distance, 5)
        return self.search_laveshtein_distance(word)

    def search_with_edit_distance(self, word: str, max_distance: int, max_results: int = 5)->list[tuple]:
        """
        Search for a word in the Trie with edit distance\n
        Input:    word : str - The word to search\n
                  max_distance : int - The maximum edit distance\n
                  max_results : int - The maximum number of results to return\n
        Output:   list[tuple] - The list of results with the format (full_name, distance)\n
        """
        results = []
        self._search_recursive(self.root, '', word, results, max_distance, max_results)
        return min(results, key=lambda x: x[1])[0] if results else ""

    def _search_recursive(self, node, current_word, target_word, results, max_distance, max_results):
        if node.is_end_of_word:
            distance = edit_distance(current_word, target_word)
            if distance <= max_distance:
                results.append((node.full_name, distance))
                if len(results) >= max_results:
                    return

        if len(results) >= max_results:
            return

        for char in node.children:
            self._search_recursive(node.children[char], current_word + char, target_word, results, max_distance, max_results)

    def search_laveshtein_distance(self, word):
        return self._search_recursive_laveshtein_distance(self.root, word, "", float('inf'), "")
    
    def _search_recursive_laveshtein_distance(self, node, word, current, min_distance, best_match):
        if node.is_end_of_word:
            distance = levenshtein_distance(word, current)
            if distance < min_distance:
                min_distance = distance
                best_match = node.full_name
        for char, next_node in node.children.items():
            result = self._search_recursive_laveshtein_distance(next_node, word, current + char, min_distance, best_match)
            if result[1] < min_distance:
                min_distance = result[1]
                best_match = result[0]
        return best_match, min_distance


def edit_distance(str1: str, str2: str) -> int:
    """
    Function to calculate the edit distance between two strings
    Input:    str1 : str - The first string
              str2 : str - The second string
    Output:          int - The edit distance between the two strings

    function use dynamic programming to possibly reduce the time complexity
    TODO: test if time complexity is reduced
    TODO: Add option to modify the costs of insertion, deletion, substitution
    """
    memo = {}
    def dp(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        if i == 0:
            return j
        if j == 0:
            return i
        if str1[i - 1] == str2[j - 1]:
            cost = 0
        else:
            cost = 1
        res = min(dp(i - 1, j) + 1,      
                  dp(i, j - 1) + 1,      
                  dp(i - 1, j - 1) + cost)  

        memo[(i, j)] = res
        return res
    return dp(len(str1), len(str2))

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

def load_data_to_Trie(file_name: str) -> Trie:
    """
    Load data from a file to a Trie\n
    Input:    file_name : str - The name of the file\n
    Output:          Trie - The Trie containing the data\n

    Each line in the file is a word to insert into the Trie\n
    Preprocess the word before inserting with the preprocess_string function
    """
    trie = Trie()
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in  file.readlines():
            line = line.strip()
            trie.insert(preprocess_string(line), line)
    return trie

#####################################################################
########################### Main pipeline ###########################
#####################################################################

def load_data():
    """
    Load data from database\n
    """
    list_province = load_data_to_Trie('list_province.txt')
    list_district = load_data_to_Trie('list_district.txt')
    list_ward = load_data_to_Trie('list_ward.txt')
    list_province.max_edit_distance = province_edit_distance_threshold 
    list_district.max_edit_distance = district_edit_distance_threshold
    list_ward.max_edit_distance = ward_edit_distance_threshold 
    return list_province, list_district, list_ward

def find_province(list_province, input):
    """
    Find province from the input\n
    Input:    list_province : Trie - The Trie containing the provinces\n
              input : str - The input to search\n
    Output:            str - The likely province\n
    """
    return list_province.search(preprocess_string(input))

def find_district(list_district, input):
    """
    Find district from the input\n
    Input:    list_district : Trie - The Trie containing the districts\n
              input : str - The input to search\n
    Output:            str - The likely district\n
    """
    return list_district.search(preprocess_string(input))


def find_ward(list_ward, input):
    """
    Find ward from the input\n
    Input:    list_ward : Trie - The Trie containing the wards\n
              input : str - The input to search\n
    Output:            str - The likely ward\n
    """
    return list_ward.search(preprocess_string(input))
   

def find_address_components_brute_force(input, list_province, list_district, list_ward):
    #process input
    process_input = preprocess_string(input).split(" ")
    len_input = len(process_input)
    # load data from database
    

    province, district, ward = "", "", ""
    province_found, ward_found = "", ""

    for i in range(len_input):
        # find province
        if province == "":
            province = find_province(list_province, " ".join(process_input[i:len_input]))
            province_found = process_input[i-1:len_input]
        # find ward
        if ward == "":
            ward = find_ward(list_ward, " ".join(process_input[:len_input - i]))
            ward_found = process_input[0:len_input - i   ]
    process_input = [item for item in process_input if item not in province_found]
    process_input = [item for item in process_input if item not in ward_found]
    len_input = len(process_input)
    for i in range(len_input):
        # find district
        if district == "":
            district = find_province(list_district, " ".join(process_input[i:len_input]))

    return {
        "province": province,
        "district": district,
        "ward": ward
    }

def main(input):
    list_province, list_district, list_ward = load_data()
    if input_separate_algorithm == "brute_force": 
        return measure_runtime(find_address_components_brute_force, input, list_province, list_district, list_ward)
    

if __name__ == '__main__':

    input = "Xã Bình Phan, huyện Chợ Gạo, tỉnh Tiền Giang"
    
    search_algorithm = "edit_distance"
    result, runtime = main(input)   

    if debug == "VERBOSE":
        print(get_all_parameters())
        print(f"Result: {result}")
        print(f"Runtime: {runtime} seconds")

    search_algorithm = "lavenshtein"
    result, runtime = main(input)   

    if debug == "VERBOSE":
        print(get_all_parameters())
        print(f"Result: {result}")
        print(f"Runtime: {runtime} seconds")