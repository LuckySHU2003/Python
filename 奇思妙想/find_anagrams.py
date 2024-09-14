# 定义函数，返回给定列表中与目标字符串是字母重排的项
def find_anagrams(string_list, target_string):
    # 将目标字符串进行排序
    sorted_target = sorted(target_string)
    
    # 创建一个空的结果列表
    result = []
    
    # 遍历字符串列表
    for string in string_list:
        # 如果当前字符串的排序结果与目标字符串相同，且它不是目标字符串本身
        if sorted(string) == sorted_target and string != target_string:
            # 将该字符串加入结果列表
            result.append(string)
    
    return result

# 示例用法
string_list = ["abd", "ac", "bad"]
target_string = "abd"

# 调用函数
result = find_anagrams(string_list, target_string)
print(result)
