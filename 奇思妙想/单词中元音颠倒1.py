# 思路： 先判断字母是不是元音，不是不改，是的放一个list里→反向reverse()→再依次获取
def foo(xs: str) -> str:
    vowels = 'aeiouAEIOU'  # 定义所有元音字母
    vowel_list = []  # 存储字符串中的所有元音字母

    # 取所有xs里的元音字母并存储在 vowel_list 中
    for char in xs:
        if char in vowels:
            vowel_list.append(char)
    
    # 反转元音字母的顺序
    vowel_list.reverse()
    
    result = []  # 用一个新的空列表 存储最终结果的列表

    # 遍历原始字符串
    for char in xs: #从头开始创建颠倒结果
    # 每次输入一个字母，添加一个对应字母到list
        if char in vowels: #如果该字母是元音字母，则result添加一个反过来的
            # 从反转的元音字母列表中取出一个元音字母，添加到result
            result.append(vowel_list.pop(0)) 
        else:
            # 不是元音字母，则直接添加到结果中
            result.append(char)
    
    # 将结果列表中的字符拼接成一个字符串并返回
    return ''.join(result) #把list里的每一个string拼起来

print(foo("drake"))  # 输出 "dreka"
print(foo("aAeEiIoOuU"))  # 输出 "UuOoIiEeAa"
print(foo("xAyEz"))  # 输出 "xEyAz"
print(foo("SaTeXiY"))  # 输出 "SiTeXaY"
