def get_elements(dictionary, n):
    list = []
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWRXYZ"
    for x in dictionary:
        if x[0] in alphabet or x[-1] in alphabet or dictionary[x] >= n:
            list.append(dictionary[x])
    return list 


