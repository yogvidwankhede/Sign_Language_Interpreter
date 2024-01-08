from collections import Counter
def tl(res):
    res_counter = Counter(res)
    a = list(res_counter)
    a = a[1:]
    return a