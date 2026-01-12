def zip_lists(list_1, list_2, list_3):
    list =[]
    if len(list_1) > 0:
        for x in range(len(list_1)):
            tuple1 = (list_1[x],list_2[x], list_3[x])
            list.append(tuple1)
    return list 
