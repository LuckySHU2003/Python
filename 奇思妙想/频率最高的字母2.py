def foo(xs: str) -> str:
    cur_ans, cur_freq = '', -1

    for x in xs:
        if xs.count(x) > cur_freq:
            cur_freq = xs.count(x)
            cur_ans = x

    return cur_ans
