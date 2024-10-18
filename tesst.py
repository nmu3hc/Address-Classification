"""
Can python print encoded Vietnamese characters?
Yes
"""
# print("ắ")


"""
Can python compare encoded Vietnamese characters?
Yes
"""
# a = "ắ"
# if a == "ắ":
#     print("aws")


"""
Function to convert Vietnamese characters to Telex characters
Input:    text : str - The text to convert
Output:          str - The converted text
"""
# def vietnamese_to_telex(text: str) -> str:
#     # Mapping of special Vietnamese characters to their Telex form
#     telex_map = {
#         'ắ': 'aws', 'ằ': 'awf', 'ẳ': 'awr', 'ẵ': 'awx', 'ặ': 'awj',
#         'ấ': 'aas', 'ầ': 'aaf', 'ẩ': 'aar', 'ẫ': 'aax', 'ậ': 'aaj',
#         'á': 'as', 'à': 'af', 'ả': 'ar', 'ã': 'ax', 'ạ': 'aj',
#         'é': 'es', 'è': 'ef', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej',
#         'ế': 'ees', 'ề': 'eef', 'ể': 'eer', 'ễ': 'eex', 'ệ': 'eej',
#         'í': 'is', 'ì': 'if', 'ỉ': 'ir', 'ĩ': 'ix', 'ị': 'ij',
#         'ó': 'os', 'ò': 'of', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj',
#         'ố': 'oos', 'ồ': 'oof', 'ổ': 'oor', 'ỗ': 'oox', 'ộ': 'ooj',
#         'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
#         'ú': 'us', 'ù': 'uf', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj',
#         'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
#         'ý': 'ys', 'ỳ': 'yf', 'ỷ': 'yr', 'ỹ': 'yx', 'ỵ': 'yj'
#     }
    
#     # Convert the text
#     converted_text = ''.join(telex_map.get(char, char) for char in text)
#     return converted_text

# # Example usage
# text = "Quán Thánh"
# converted_text = vietnamese_to_telex(text)
# print(converted_text)  # Output: aw as as es is os us ys

"""
Trie implementation in Python with insert and search functions
"""
# class TrieNode:
#     def __init__(self):
#         self.children = {}
#         self.is_end_of_word = False

# class Trie:
#     def __init__(self):
#         self.root = TrieNode()

#     def insert(self, word: str) -> None:
#         node = self.root
#         for char in word:
#             if char not in node.children:
#                 node.children[char] = TrieNode()
#             node = node.children[char]
#         node.is_end_of_word = True

#     def search(self, word: str) -> bool:
#         node = self.root
#         for char in word:
#             if char not in node.children:
#                 return False
#             node = node.children[char]
#         return node.is_end_of_word

# # Example usage
# trie = Trie()
# trie.insert("apple")
# print(trie.search("apple"))   # Returns True
# print(trie.search("app"))     # Returns False
# trie.insert("app")
# print(trie.search("app"))     # Returns True


"""
UT for province search
"""
# input = "Hà Ni"
# print('Input: {}'.format(preprocess_string(input)))
# for i in range(20):
#     results = list_province.search_with_edit_distance(preprocess_string(input),i)
#     print('Search with edit distance {}, likely result: {}. all results: {}'.format(i, min(results, key=lambda x: x[1])[0] if results else "", results))