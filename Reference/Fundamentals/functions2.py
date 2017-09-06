# More fun with functions!
# Here we have to different functions. One replaces a's with b's, and another replaces b's with c's
def replaceA(str):
    return str.replace('a','b')

def replaceB(str):
    return str.replace('b','c')
# Returning a variable just means that we don't print it right away. Instead,
# we return it, so that it can be manipulated however we want later.

# Here we call our functions, labeling them. We set the variable A equal to the result of
# replacing all the 'a's in apple with b's.
a = replaceA("apple")
# We set the varibale b equal to the result of replacing all the b's in 'banana' with c's
b = replaceB("banana")

# Here, we set c equal to the result of replacing all the b's with c's after all the
# a's are replaced with b's. The below function is really:
# c = replaceB(replaceA("apple"))

c = replaceB(a)
# Print all variables to the console
print "apple",a,c

