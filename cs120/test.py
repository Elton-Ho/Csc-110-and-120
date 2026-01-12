def find_mode(list, first_time, curr_count, highest_count, answer):
    if first_time:
        list.sort()
        first_time = False
    if len(list) == 1:
        # need to account for curr_count + 1 when the last number is the answer
        if curr_count + 1> highest_count: 
            answer = list[0]
        return answer
    if list[0] == list[1]: 
        return find_mode(list[1:], first_time, curr_count + 1, highest_count, answer)
    
    # curr_count + 1 needs to be accounted for because the if statment above 
    # doesn't look between two different numbers 
    if curr_count + 1> highest_count: 
        return find_mode(list[1:], first_time, 0, curr_count + 1, list[0])
    
    return find_mode(list[1:], first_time, 0, highest_count, answer)

# example test case
list = [1,4, 2,4,3,2,3,3] # should equal 3
print(find_mode(list, True, 0, 0, None))