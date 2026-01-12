def celsius_to_fahrenheit(celsius):
    result = (celsius * 1.8) + 32
    rounded_result = round(result, 2)
    return rounded_result

def fahrenheit_to_celsius(fahrenheit):
    result = (fahrenheit-32) * 5/9 
    rounded_result = round(result, 2)
    return rounded_result
