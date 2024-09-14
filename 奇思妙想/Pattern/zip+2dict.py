def word_pattern(pattern: str, words: list[str]) -> bool:

    if len(pattern) != len(words): #第一个条件：两个的长度要相等
        return False

    pattern_to_word = {}
    word_to_pattern = {}

    for p, w in zip(pattern, words):
        if p in pattern_to_word:
            if pattern_to_word[p] != w:
                return False
        else:
            pattern_to_word[p] = w

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

 """
    Given a pattern and a word list, determine if the word list follows the same pattern.
    That is to say, ensure
        pattern[j] == pattern[k] only when words[j] == words[k]
    and
        pattern[j] != pattern[k] means words[j] != words[k]
    Precondition:
        Assume pattern is all lowercase letters.

    >>> word_pattern('aaaa', ['cat', 'cat', 'cat', 'cat'])
    True
    >>> word_pattern('xoox', ['dog', 'cat', 'cat', 'dog'])
    True
    >>> word_pattern('xy', ['cat', 'cat'])
    False
    >>> word_pattern('xooy', ['dog', 'cat', 'cat', 'fish'])
    True
    """
