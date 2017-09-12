# Python script to demonstrate the power of lists.

# Lists are a java data type that can store multiple pieces of information.

# To declare a list, we use [].
import time
import sys
import random

a = [1,2,3,4,5] # A list of 5 integers

# To select an item from the list, we can call the list with the number's index.
# An index is a number's postion in the array. For example, 1 has the index "0"
# because it is the first element.

print a[2] # Print's 3, because we are calling the third number in the list.

# To add an element to a list, we can call a.append()

a.append(6)
print a