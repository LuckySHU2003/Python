# 第一种
def to_title_case(text):
    # 使用 split() 将字符串分割成单词列表
    words = text.split()
    
    # 创建一个空列表，用来存储每个处理过的单词
    capitalized_words = []
    
    # 使用 for 循环遍历每个单词，并将首字母大写，其他字母小写
    for word in words:
        capitalized_word = word.capitalize()  # 首字母大写
        capitalized_words.append(capitalized_word)  # 添加到列表中
    
    # 使用 join() 将单词重新组合成一个字符串
    return ' '.join(capitalized_words)

# 第二种
def title(chars:str) -> str:
    ans = ''
    characters = chars.split() #直接返回为list!所有单词都在里面 ['drake', 'is', 'mid']
    for x in characters:
        ans = ans + ' ' + x.capitalize() #string才有capitalize!要中间加上空格
    return ans.strip() #删掉左右空格
