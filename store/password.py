# Python3 code to demonstrate
# generating random strings
# using random.choices()
import string
import random


def PasswordSet():
    # initializing size of string
    N = 10

    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))

    # print result
    print("The generated random string : " + str(res))
    return str(res)


PasswordSet()
