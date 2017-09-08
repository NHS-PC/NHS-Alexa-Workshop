# Python program that extends another script

# We import the python script addTwoNumbers that is also in this folder,
# that returns the sum of two numbers.
import addTwoNumbers

# We declare the variable 'sum' to be equal to the result of addTwoNumbers of 3 and 4.
sum = addTwoNumbers.addTwoNumbers(3,4)

# Print the sum
print sum

# Inheritence is a great tool to abstract your project, and to organize your code.