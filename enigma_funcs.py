# enigma functions


# rotate string to the right by n chars

def rotateString(string, n):
    return string[-n:] + string[:-n]


# create num2letter two-way dict
num2letter = {}
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(0, len(alphabet)):
    num2letter[alphabet[i]] = i
    num2letter[i] = alphabet[i]

