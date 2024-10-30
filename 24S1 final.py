##import tkinter as tk
##root = tk.Tk()
##root.geometry("200x400")
##root.mainloop()

##x = input("Prompt: ")
##y = input("Prompt: ")
##print(f"x - y = {x - y}")

# Q10
##import tkinter as tk 
##root = tk.Tk()
##(s1, s2, s3, s4) = (tk.BOTTOM, tk.LEFT, tk.RIGHT, tk.TOP)
##
##tk.Label(text="alice").pack(side=s1)
##tk.Label(text="bob").pack(side=s2)
##tk.Label(text="carol").pack(side=s3)
##tk.Label(text="dilbert").pack(side=s4)
##
##root.mainloop()

# Q11
##x = 0
##for y,z in enumerate([[1],[2]]):
##    x += 2 * y + z

# Q14
##z = lambda v, w:v+w
##xs = [1,2,3,4]
##ys = [3,4,5,6]
##y = [z(v,w) for v in xs if v<2 for w in ys]

# Q17
##if [] and y:
##    y=0
##else:
##    y=1

# Q18
##def foo(xs: list[int], ys: dict) -> bool:
##    """ Precondition: len(xs) > 0 """
##    for x in xs:
##        if not x in ys:
##            return True
##    return False

# Q20
##xss = ['basket', 'bird', 'balloon']
##ys = ['ball']
##z=[ys[0] in xs and ys[1] in xs for xs in xss]
##print(z)

# Q22
##def foo(xs: str) -> None:
##    for x in xs:
##        with open('file.txt', 'w') as f:
##            f.write(x)
##    return

# Q23
##def lcs(xs: str, ys: str) -> str:
##    """
##    Return the longest substring
##    that both and xs and ys have in
##    common.
##    >>> lcs("", "potato")
##    ''
##    >>> lcs("tomato", "potato")
##    'ato'
##    >>> lcs("ababa", "cbaba")
##    'baba'
##    """
##    i = 0
##    ans = ''
##    if len(xs)!= 0:
##        while i < len(ys):
##            if ys[i] == xs[i]:
##                ans += ys[i]
##                i += 1
##    return ans

##def lcs(xs: str, ys: str) -> str:
##    """
##    Return the longest substring
##    that both xs and ys have in
##    common.
##    >>> lcs("", "potato")
##    ''
##    >>> lcs("tomato", "potato")
##    'ato'
##    >>> lcs("ababa", "cbaba")
##    'baba'
##    """
##    # 初始化二维列表，用于记录公共子串的长度
##    dp = [[0] * (len(ys) + 1) for _ in range(len(xs) + 1)]
##    longest = 0
##    end_index = 0  # 用于记录最长公共子串的结束位置
##
##    # 填充dp表格，找到最长的公共子串
##    for i in range(1, len(xs) + 1):
##        for j in range(1, len(ys) + 1):
##            if xs[i - 1] == ys[j - 1]:
##                dp[i][j] = dp[i - 1][j - 1] + 1
##                if dp[i][j] > longest:
##                    longest = dp[i][j]
##                    end_index = i  # 更新最长子串的结束位置
##
##    # 截取最长公共子串
##    return xs[end_index - longest:end_index]

# Q24
##def foo(x: int, xs: list[int]) -> bool:
##    return x in xs
##
##foo('', ' ')

#Q 25
##x = "goodbye".replace("ood","ello")

# Q27
##def r(x: int, y: int) -> int:
##    if x == 0:
##        return x * y
##    return r(x-5, y) + y

# Q31-35
##class A(object):
##    def __init__(self, x):
##        self._x = 2 * x
##
##    def f(self, x):
##        return self.g(x) + 2
##
##    def g(self, x):
##        return x-1
##
##class B(A):
##    def g(self, y):
##        return self._x + y
##
##class C(B):
##    def __init__(self, x, y):
##        super().__init__(x)
##        self._y = y+2
##
##    def f(self,x):
##        return self._x +self._y
##
##class D(B):
##
##    def __init__(self, x, y):
##        super().__init__(x)
##        self._x += y
##        self._y = y+2
##        
##    def f(self, y) :
##        return self._y + y
##    
##    def g(self, x):
##        return super().g(x) - x
##    
##a=A(1)
##b=B(2)
##c=C(3, 4)
##d=D(5, 6)

# Q36
def foo(xs:str, ys:str)->bool:
    char = ''
    for x in xs:
        if x!="!":
            char+=x
        else:
            char = char[:-1]
    return char == ys
