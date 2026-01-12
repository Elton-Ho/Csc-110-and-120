'''
Elton Ho 
CSC110
1 p.m. Class
Programming Project 1
This program has four separate functions that find the area of a
rectangle, triangle, trapezoid, and circle.
'''

def rectangle_area(base, height):
    '''
    It returns the area of the rectangle using a given base and height.
    Args:
        base: the given base of the rectangle.
        height: the given height of the rectangle.
    Returns:
        The area of the rectangle using a given base and height.
    '''

    # using the formula for the area of a rectangle 
    return base * height

def triangle_area(a, b ,c):
    '''
    It returns the area of the triangle using three given side lengths
    by use of Heron’s formula.
    Args:
        a: one of the three given side lengths of the triangle
        b: a different given side length of the triangle
        c: a different given side length of the triangle
    Returns:
        The area of the triangle using three given side lengths.
    '''

    # assigns the semiperimeter to s
    s = (a + b + c) / 2

    # using Heron's formula where s is the semiperimeter
    return (s * (s - a) * (s - b) * (s-c)) ** (.5)

def trapezoid_area(base_1, base_2, height):
    '''
    It returns the area of the trapezoid using two given bases and a 
    given height.
    Args:
        base_1: one of the two given bases of the trapezoid
        base_2: the other given base of the trapezoid
        height: the given height of the trapezoid
    Returns:
        The area of the trapezoid using two given bases and a given height.
    '''

    # using the formula for the area of a trapezoid 
    return .5 * (base_1 + base_2) * height 

def circle_area(radius):
    '''
    It returns the area of the circle rounded to two decimal places
    using a given radius.
    Args:
        radius: the given radius of the circle
    Returns:
        The area of the circle rounded to two decimal places using
        a given radius.
    '''

    # assigns the area of the circle to result
    result = 3.1415 * radius ** 2 

    # assigns rounded_result to the result rounded to two decimal places
    rounded_result = round(result, 2)

    # returns the result rounded to two decimal places
    return rounded_result