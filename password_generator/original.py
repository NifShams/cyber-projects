from string import ascii_letters , digits , punctuation 
import random

def password(n):#will return a password with the length of n
    v=[ascii_letters , digits , punctuation ]
    password=''
    for j in range (n):
            password +=random.choice(random.choice(v))
    
    return password
