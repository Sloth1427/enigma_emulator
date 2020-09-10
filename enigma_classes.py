# contains classes for enigma M3 emulator

import enigma_funcs

# wheel class for the creation of each wheel and UKW.

class Wheel:

    def __init__(self, wiring, turnoverNotch):

        self.wiring = wiring  # string of the inner wheel wiring

        # letter/number visible in window when wheel turns over. Not the same as
        # the actual position of the turnover notch on the outer wheel. I.e. the two
        # are offset. The first position in a wheel list will be considered the 'window'.
        # See 'Turnover' column in http://www.cryptomuseum.com/crypto/enigma/wiring.htm.

        self.turnoverNotch = turnoverNotch  # string containing turnover notch positions relative to outer letters

        self.outer = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # outer wheel markings

    # instance method to set the ringstellung, i.e. rotation
    # of inner ring relative to outer. Not exactly sure how the usual notation
    # translates to an offset, so the below is a first guess. Puts the letter
    # specified (ringstellung) of outer to first position, without rotating
    # wiring.

    def set_ringstellung(self, ringstellung):

        while self.outer[0] != ringstellung:  # while ringstellung not at first position. Might need to change index.
            self.outer = enigma_funcs.rotateString(self.outer, 1)  # rotate outer by 1
        return self.outer





# enigma M3 machine class

class M3:

    def __init__(self, wheels, stekkerbrett):

        # list of wheels in desired order, where element 0 is the UKW
        self.wheels = wheels

        # create stekkerbrett two-way dict from stekkerbrett pairs, e.g. ['AE', 'FY']

        stekker_dict = {}  # create initial empty dictionary

        # create initial unstekkered dict
        for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            stekker_dict[char] = char

        # modify dict with stekkers
        for pair in stekkerbrett:
            stekker_dict[pair[0]] = pair[1]
            stekker_dict[pair[1]] = pair[0]

        self.stekkerbrett = stekker_dict




    # method to rotate the wheels to the starting position. As far as I know,
    # the UKW in M3 could only be inserted in one position. Model C could be
    # inserted in two positions, and model D in 26.
    # wheel_positions should be list e.g. ['D', 'H', 'Z']

    def set_wheel_positions(self, wheel_positions):

        # Error checking
        if len(self.wheels)-1 != len(wheel_positions):
            print('Error: number of movable wheels, and number of wheel position settings does not match')
            return

        # rotate each wheel to correct position, so that outer letter specified is at index [0]
        # Might need to change index.
        for i in range(0, len(wheel_positions)):  # for each wheel
            while self.wheels[i + 1].outer[0] != wheel_positions[i]:  # while wheel position not set correctly
                self.wheels[i + 1].outer = enigma_funcs.rotateString(self.wheels[i + 1].outer, 1)  # rotate outer
                self.wheels[i + 1].wiring = enigma_funcs.rotateString(self.wheels[i + 1].wiring, 1)  # rotate wiring

        return self.wheels



    # method to rotate right-most wheel, and any other wheels as dictated
    # by turnover notches on the wheel to the left. Will be run before each
    # character is enciphered.

    def move_wheels(self):

        w2_move_flag = 0  # flag variable, which gets set to 1 if w2 (wheels[2]) moves

        # the rightmost wheels always rotates one position
        self.wheels[3].outer = enigma_funcs.rotateString(self.wheels[3].outer, 1)
        self.wheels[3].wiring = enigma_funcs.rotateString(self.wheels[3].wiring, 1)
        #print('rightmost wheel click')

        # move middle wheel one position if turnover notch was in first position of rightmost wheel
        # before move.
        # This is working on the assumption that the turnover notch turns over the wheel to its
        # left if it goes from being at index 0 to index 1
        if self.wheels[3].outer[1] in self.wheels[3].turnoverNotch:  # if turnover notch was in position 0 before move
            self.wheels[2].outer = enigma_funcs.rotateString(self.wheels[2].outer, 1)
            self.wheels[2].wiring = enigma_funcs.rotateString(self.wheels[2].wiring, 1)

            w2_move_flag = 1  # set flag to 1, to show middle wheel moved
            #print('middle wheel click')

        # move leftmost wheel one click if middle wheel moved, and if middle wheel
        # turnover notch was as index 0 before move (i.e. index 1 now).
        if w2_move_flag == 1 and self.wheels[2].outer[1] in self.wheels[2].turnoverNotch:
            self.wheels[1].outer = enigma_funcs.rotateString(self.wheels[1].outer, 1)
            self.wheels[1].wiring = enigma_funcs.rotateString(self.wheels[1].wiring, 1)
            #print('leftmost wheel click')

        return self.wheels




    # encipher/decipher a character

    def encipher(self, char):

        #print('input char: ' + char)
        self.move_wheels()  # wheels move before enciphering a character

        # run the char through the stekkerbrett on the way to wheels
        char = self.stekkerbrett[char]
        #print('char out of stekkerbrett: ' + char)

        # run char through righmost wheel towards UKW
        char = self.wheels[3].wiring[enigma_funcs.num2letter[char]]
        #print('char out of rightmost wheel: ' + char)

        # run car through middle wheel towards UKW
        char = self.wheels[2].wiring[enigma_funcs.num2letter[char]]
        #print('char out of middle wheel: ' + char)

        # run car through leftmost wheel towards UKW
        char = self.wheels[1].wiring[enigma_funcs.num2letter[char]]
        #print('char out of leftmost wheel: ' + char)

        # run car through UKW
        char = self.wheels[0].wiring[enigma_funcs.num2letter[char]]
        #print('char out of UKW: ' + char)

        # run car through leftmost wheel towards ETW
        char = enigma_funcs.num2letter[self.wheels[1].wiring.index(char)]
        #print('char out of leftmost wheel: ' + char)

        # run car through middle wheel towards ETW
        char = enigma_funcs.num2letter[self.wheels[2].wiring.index(char)]
        #print('char out of middle wheel: ' + char)

        # run car through rightmost wheel towards ETW
        char = enigma_funcs.num2letter[self.wheels[3].wiring.index(char)]
        #print('char out of rightmost wheel: ' + char)

        # run the char through the stekkerbrett on the way out from wheels
        char = self.stekkerbrett[char]
        #print('char out of stekkerbrett: ' + char)

        return char