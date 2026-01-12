'''
Author: Adriana Picoral
Course: CSC 110

This python script tests the solution for programming problem 3.
No need to make any changes to this code. Just have this .py in the same
folder/directory as your temperatures.py and run this file.
'''

# from the solution file, import all functions
from temperatures import *

def pass_or_fail(result, assert_value):
  '''
  This function tests whether a value returned by a function matches
  the expected value -- it's used to test functions
  Args:
    result: any type returned by a function
    assert_value: any type that is expected
  Returns:
    nothing, it prints messages
  '''
  # try to assert value returned by function is equal to expected value
  try:
    assert result == assert_value
    print("Test passed.")
  except AssertionError: # try failed, values are different
    print("Test failed. " + str(result) + " != " + str(assert_value))

def main():
  '''
  This function calls pass_or_fail to assert the accuracy of the
  functions in this programming problem solution
  '''
  pass_or_fail( celsius_to_fahrenheit(15), 59.0 )
  pass_or_fail( celsius_to_fahrenheit(25), 77.0 )
  pass_or_fail( celsius_to_fahrenheit(38), 100.4 )
  pass_or_fail( fahrenheit_to_celsius(100), 37.78 )
  pass_or_fail( fahrenheit_to_celsius(115), 46.11 )
  pass_or_fail( fahrenheit_to_celsius(75), 23.89 )

main()