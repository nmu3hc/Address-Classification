import re

#####################################################################
######## This section contains fucntions for processing Data ########
#####################################################################
"""
Function to convert Vietnamese characters to Telex characters
Input:    text : str - The text to convert
Output:          str - The converted text
"""
def vietnamese_to_telex(text: str) -> str:
    # Mapping of special Vietnamese characters to their Telex form
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
    
    # Convert the text
    converted_text = ''.join(telex_map.get(char, char) for char in text)
    return converted_text

def preprocess_string(text: str) -> str:
    # Remove special characters and convert to lowercase
    normalized = re.sub(r'[^\w\s]', '', text).lower().strip()
    return vietnamese_to_telex(normalized)
#####################################################################
############# This section contains Trie implementation #############
#####################################################################
"""
Trie implementation in Python with insert and search functions
"""

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

    def search_with_edit_distance(self, word: str, max_distance: int, max_results: int = 5):
        results = []
        self._search_recursive(self.root, '', word, results, max_distance, max_results)
        return results[:max_results]

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


def edit_distance(str1: str, str2: str) -> int:
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
        res = min(dp(i - 1, j) + 1,      # Deletion
                  dp(i, j - 1) + 1,      # Insertion
                  dp(i - 1, j - 1) + cost)  # Substitution

        memo[(i, j)] = res
        return res
    return dp(len(str1), len(str2))

def load_data_to_Trie(file_name: str) -> Trie:
    trie = Trie()
    with open(file_name, 'r') as file:
        for line in  file.readlines():
            line = line.strip()
            trie.insert(preprocess_string(line), line)
    return trie

#####################################################################
########################### Main pipeline ###########################
#####################################################################

if __name__ == '__main__':
    # load data from database
    list_province = load_data_to_Trie('list_province.txt')
    list_district = load_data_to_Trie('list_district.txt')
    list_ward = load_data_to_Trie('list_ward.txt')

    input = "Tiền Giang"
    print('Input: {}'.format(preprocess_string(input)))
    for i in range(20):
        results = list_province.search_with_edit_distance(preprocess_string(input),i)
        print('Search with edit distance {}, results: {}'.format(i, results))