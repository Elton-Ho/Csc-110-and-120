def stop_ascending(list):
    index = 0
    if len(list) > 0: 
        while index < len(list) -1:
            if list[index] >= list[index + 1]:
                return index + 1
            index += 1
        return len(list)
    return None

