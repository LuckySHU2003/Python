def word_pattern(pattern: str, words: list[str]) -> bool:

    If len(pattern) != len(words): #前提条件：两个内容长度一致
        return False

    word_dict = {}
    y = ''

   for k, x in enumerate(pattern): #把pattern的每一个元素 当作字典的value
        word_dict[words[k]] = x #words对应相同第n个作为dict的key

    for i in words:
        y += word_dict[i] #获取key对应内容，添加出结果
    
    return  y == pattern #比较结果是否相同，相同则pattern相同
