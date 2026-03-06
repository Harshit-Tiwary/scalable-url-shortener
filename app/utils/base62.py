import string

BASE62 = string.digits + string.ascii_letters

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    arr = []
    base = len(BASE62)

    while num > 0:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])

    arr.reverse()
    return ''.join(arr)