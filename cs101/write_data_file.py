
def write_csv(dictionary, file_name):
    list = []
    string = ""
    file = open(file_name, "w")
    for x,y in dictionary.items():
        file.write(x)
        for i in range(len(y)):
            file.write("," + str(y[i]))
        file.write("\n")
    file.close
