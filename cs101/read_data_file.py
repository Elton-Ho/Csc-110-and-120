def read_csv(file_name):
    file = open(file_name)
    dictionary = {}
    for line in file:
        x = line.strip("\n").split(',')
        for i in range(len(x)):
            if x[1][0] in "12345567890.":
                if i > 1:
                    dictionary[x[0]].append(float(x[i]))
                else:
                    dictionary[x[0]] = [float(x[1])]
            else:
                if i > 1:
                    dictionary[x[0]].append(x[i])
                else:
                    dictionary[x[0]] = [x[1]]
              
    return dictionary 
