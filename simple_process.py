def simple_go(text):
    result = text[::-1].upper() + " 42"
    print(f"{text=} {result=}")
    return result
