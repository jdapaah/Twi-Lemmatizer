#!python3
import sys
import vowels
correction = {
    chr(596): vowels.VOWEL_SMALL_O,
    chr(8580):vowels.VOWEL_SMALL_O,#

    chr(603): vowels.VOWEL_SMALL_E,
    chr(949): vowels.VOWEL_SMALL_E,#
    chr(1297):vowels.VOWEL_SMALL_E,#

    chr(390): vowels.VOWEL_CAPITAL_O,
    chr(8579):vowels.VOWEL_CAPITAL_O,#

    chr(400): vowels.VOWEL_CAPITAL_E,
    chr(1296):vowels.VOWEL_CAPITAL_E,#

    chr(39):   chr(39),
    chr(8216): chr(39),#
    chr(8217): chr(39),#
}
collection = {}
with open(sys.argv[1]) as read, open(sys.argv[1]+'x', 'w') as write:
    for line in read:
        for char in line:
            if char in correction:
                write.write(correction[char])
            else:
                write.write(char)
            if char not in collection:
                collection[char] = ord(char)
collection  = sorted(collection.items(), key=lambda item: item[1])
with open('collection', 'w') as f:
    for p in collection:
        print(p, file=f)