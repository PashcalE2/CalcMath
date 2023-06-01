
def str_to_float(s: str):
    try:
        return float(s.replace(",", "."))
    except ValueError:
        raise Exception("неверный формат числа с плавающей точкой")


def str_to_float_list(s: str, sep=" "):
    try:
        ans = []
        for num in s.replace(",", ".").split(sep):
            ans.append(float(num))
        return ans
    except ValueError:
        raise Exception("неверный формат числа с плавающей точкой")


def str_to_int(s: str):
    try:
        n = int(s)
        return n
    except ValueError:
        raise Exception("неверный формат целого числа")
