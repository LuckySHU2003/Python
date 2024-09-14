# 定义一个函数，计算字符串中每个字符的频率
def get_char_count(string):
    char_count = {}
    for char in string:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
    return char_count

# 定义函数，返回给定列表中与目标字符串是字母重排的项
def find_anagrams(string_list, target_string):
    # 获取目标字符串的字符频率
    target_count = get_char_count(target_string)
    
    # 创建一个空的结果列表
    result = []
    
    # 遍历字符串列表
    for string in string_list:
        # 如果当前字符串的字符频率与目标字符串相同，且它不是目标字符串本身
        if get_char_count(string) == target_count and string != target_string:
            # 将该字符串加入结果列表
            result.append(string)
    
    return result

# 示例用法
string_list = ["abd", "ac", "bad"]
target_string = "abd"

# 调用函数
result = find_anagrams(string_list, target_string)
print(result)
