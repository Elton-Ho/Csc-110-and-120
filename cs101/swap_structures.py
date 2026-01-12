def swap(dict,set1):
    for x in set(dict):
        if x in set1:
            dict[dict[x]] = x
            dict.pop(x)
    return dict
