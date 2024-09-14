# 写一个Count函数
def count(y, ys: str) -> int:
    ans = 0
    for x in ys:
        if y == x:
            ans += 1
    return ans

# 使用Count计数
def foo(xs: str) -> str:
    cur_ans, cur_freq = '', -1 #因为最低频次是0，所以初始设定一个比0小的

    for x in xs: 
        if count(x, xs) > cur_freq: #数目前这个字母的频率 如果结果大于现有最大值
            cur_freq = count(x, xs) #则更新该值为现有最高频率
            cur_ans = x #同步更新对应字母

    return cur_ans
