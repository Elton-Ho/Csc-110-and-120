def all_mappings(dic):
    list =[]
    if len(dic) > 0:
        for x in dic:
            for y in dic[x]:
                tuple1 = (x,y)
                list.append(tuple1)
    return list 

