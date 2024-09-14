def word_pattern(pattern: str, words: list[str]) -> bool:
    if len(pattern) != len(words):
        return False

    pattern_to_word = {}
    word_to_pattern = {}

    for i in range(len(pattern)):
        p = pattern[i]
        w = words[i]

        if p in pattern_to_word: #如果单独这个元素 已经在字典里了
            if pattern_to_word[p] != w:  #对应的alue不对 -> False
                return False
        else:
            pattern_to_word[p] = w 
            #如果不在字典里，则添加相同index位置的word内容

        if w in word_to_pattern:
            if word_to_pattern[w] != p:
                return False
        else:
            word_to_pattern[w] = p

    return True

# 示例用法
print(word_pattern('aaaa', ['cat', 'cat', 'cat', 'cat']))  # 输出: True
print(word_pattern('xoox', ['dog', 'cat', 'cat', 'dog']))  # 输出: True
print(word_pattern('xy', ['cat', 'cat']))  # 输出: False
print(word_pattern('xooy', ['dog', 'cat', 'cat', 'fish']))  # 输出: True
