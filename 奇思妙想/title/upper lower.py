# 第一种
def title(chars: str) -> str:
    ans = ''
    last = ' '  # ⚠️初始值为空格，表示第一个字符为新单词的首字母
    for char in chars:
        if last == ' ':  # 如果前一个字符是空格，则大写当前字符
            ans += char.upper()
        else:  # 前一个不是空格，则小写当前字符
            ans += char.lower()
        last = char  # 更新 last 为当前字符
    return ans

# 第二种
def title(xs: str) -> str:
  ans = ''
  for x in xs:
    if ans[-1] == '': #把内容放到结果里，看结果里上一次循环后最后一位是不是空格，默认最开始也是空格
      ans += x.upper()
    else: 
      ans += x.lower()

  return ans[1:]
