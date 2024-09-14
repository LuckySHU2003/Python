def foo(xs: str) -> str:
    acc = ''

    for char in xs:
        if char in 'aeiouAEIOU':
            acc += char

    new_string = ''
    for char in xs:
        if char in 'aeiouAEIOU':
            new_string += acc[-1]
            acc = acc[:-1]
        else: 
            new_string += char
    
    return new_string

print(foo('aAeEiIoOuU'))
