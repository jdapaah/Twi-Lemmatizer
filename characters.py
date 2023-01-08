APOSTROPHE      = "'" # chr(39)
VOWEL_SMALL_E   = "ɛ" # chr(400)
VOWEL_SMALL_O   = "ɔ" # chr(596)
VOWEL_CAPITAL_E = "Ɛ" # chr(603)
VOWEL_CAPITAL_O = "Ɔ" # chr(390)

correction = {
    chr(39):   APOSTROPHE,
    chr(8216): APOSTROPHE,#
    chr(8217): APOSTROPHE,#
    
    chr(400): VOWEL_CAPITAL_E,
    chr(1296):VOWEL_CAPITAL_E,#
    
    chr(596): VOWEL_SMALL_O,
    chr(8580):VOWEL_SMALL_O,#

    chr(603): VOWEL_SMALL_E,
    chr(949): VOWEL_SMALL_E,#
    chr(1297):VOWEL_SMALL_E,#

    chr(390): VOWEL_CAPITAL_O,
    chr(8579):VOWEL_CAPITAL_O,#

}