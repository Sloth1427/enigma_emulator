"""
Main file for enigma machine emulator.

This programme is intended to emulator the M3 enigma machine.

References:
    http://www.cryptomuseum.com/crypto/enigma/wiring.htm
    https://en.wikipedia.org/wiki/Enigma_machine#Rotors

"""

import enigma_classes


#### create wheel and UKW instances ####

wI = enigma_classes.Wheel('EKMFLGDQVZNTOWYHXUSPAIBRCJ', 'Q')
wII = enigma_classes.Wheel('AJDKSIRUXBLHWTMCQGZNPYFVOE', 'E')
wIII = enigma_classes.Wheel('BDFHJLCPRTXVZNYEIWGAKMUSQO', 'V')
wIV = enigma_classes.Wheel('ESOVPZJAYQUIRHXLNFTGKDCMWB', 'J')
wV = enigma_classes.Wheel('VZBRGITYUPSDNHLXAWMJQOFECK', 'Z')
wVI = enigma_classes.Wheel('JPGVOUMFYQBENHZRDKASXLICTW', 'ZM')
wVII = enigma_classes.Wheel('NZJHGRCXMYSWBOUFAIVLPEKQDT', 'ZM')
wVIII = enigma_classes.Wheel('FKQHTLXOCBJSPDZRAMEWNIUYGV', 'ZM')

# UKWs do not have turnover notches. Provide empty string.
UKW_B = enigma_classes.Wheel('YRUHQSLDPXNGOKMIEBFZCWVJAT', '')
UKW_C = enigma_classes.Wheel('FVPJIAOYEDRZXWGCTKUQSBNMHL', '')

#### set ringstellung for desired wheels using wheel class method ####

wI.set_ringstellung('A')
wII.set_ringstellung('U')
wIII.set_ringstellung('E')

#### create enigma machine instance and set up ####

wheels = [UKW_B, wI, wII, wIII]  # wheels in the order that they are in the machine
stekkerbrett = ['AG', 'TF']  # stekkerbrett pairs
wheel_positions = ['C', 'G', 'S']  # which outer letters are showing in window

M3 = enigma_classes.M3(wheels, stekkerbrett)  # create machine instance

M3.set_wheel_positions(wheel_positions)  # rotate wheels to wheel positions

#### encipher or decipher message ####

allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
input_message = ''
raw_input = input('ENTER MESSAGE: ')
raw_input = raw_input.upper()
for char in raw_input:
    if char in allowed_chars:
        input_message = input_message + char
    else:
        print(char + ' - stripped from message')

output_message = ''

for char in input_message:
    output_message = output_message + M3.encipher(char)

print('OUTPUT: ' + output_message)








