def concatenate(words):
    index = 0
    result = "" 
    while index < len(words):
        result += words[index]
        if index < len(words) -1:
            result += " "
        index += 1
    return result