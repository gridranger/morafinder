# -*- coding: utf-8 -*-
from sys import argv

__author__ = 'Bárdos Dávid'
l = "l"  # LONG
s = "s"  # SHORT
dactyl = "lss"
spondee = "ll"
trochee = "ls"
iamb = "sl"
# add new feet above this line
hexameter = [[dactyl, spondee], [dactyl, spondee], [dactyl, spondee], [dactyl, spondee], [dactyl],
             [spondee, trochee]]
pentameter = [[dactyl, spondee], [dactyl, spondee], [l, s], [dactyl], [dactyl], [l, s]]
pentameter_closure = [[dactyl], [dactyl], [l, s]]
# add new line structure before this line
known_formats = {"hexameter": hexameter, "pentameter": pentameter, "pentameter closure": pentameter_closure}


class WrongFeet(RuntimeError):
    pass


class NotEnoughFeet(RuntimeError):
    pass


class MoraFinder(object):
    long_vowels = ["Á", "É", "Í", "Ó", "Ő", "Ú", "Ű"]
    vowels = ["A", "Á", "E", "É", "I", "Í", "O", "Ó", "Ö", "Ő", "U", "Ú", "Ü", "Ű"]
    single_letter_consonants = ["B", "C", "D", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "V", "W", "X", "Y", "Z"]
    multi_character_consonants = ["DZS", "CS", "DZ", "GY", "LY", "NY", "SZ", "TY", "ZS"]
    consonants = single_letter_consonants + multi_character_consonants

    def is_vowel(self, letter):
        return True if letter in self.vowels else False

    def is_consonant(self, letter):
        return True if letter in self.consonants else False

    def check_line(self, line):
        pseudosyllabes = self.split_to_pseudosyllabes(line)
        feet = ""
        for pseudosyllabe in pseudosyllabes:
            feet += self.get_length(pseudosyllabe)
        return self.recognize_forms(feet)

    def split_to_pseudosyllabes(self, line):
        line = line.upper()
        result = []
        current_pseudosyllabe = ""
        for character in line:
            if self.is_vowel(character) and current_pseudosyllabe == "":
                current_pseudosyllabe += character
            elif self.is_vowel(character):
                result.append(str(current_pseudosyllabe))
                current_pseudosyllabe = ""
                current_pseudosyllabe += character
            elif self.is_consonant(character) and current_pseudosyllabe == "":
                continue
            elif self.is_consonant(character):
                current_pseudosyllabe += character
        if current_pseudosyllabe:
            result.append(current_pseudosyllabe)
        return result

    def get_length(self, pseudosyllabe):
        current_vowel = pseudosyllabe[0]
        current_consonants = pseudosyllabe[1:]
        if current_vowel in self.long_vowels:
            return l
        for multi_caracter_consonant in self.multi_character_consonants:
            current_consonants = current_consonants.replace(multi_caracter_consonant, "0")
        for consonant in self.consonants:
            current_consonants = current_consonants.replace(consonant, "0")
        if len(current_consonants) in [0, 1]:
            return s
        else:
            return l

    def recognize_forms(self, feet):
        log = []
        for name, current_format in known_formats.items():
            log.append("Checking as {}...".format(name))
            try:
                self.recognize_form(current_format, feet)
            except (NotEnoughFeet, WrongFeet) as e:
                log.append("    {}".format(e))
            else:
                print("Line identified as {}".format(name))
                return current_format
        print("\n".join(log))

    @staticmethod
    def recognize_form(expected_form, raw_feet):
        final_form = []
        for feet_alternatives in expected_form:
            if any(raw_feet.startswith(feet_alternative) for feet_alternative in feet_alternatives):
                for feet_alternative in feet_alternatives:
                    if raw_feet.startswith(feet_alternative):
                        final_form.append(feet_alternative)
                        raw_feet = raw_feet.replace(feet_alternative, "", 1)
                        break
            elif len(raw_feet) < min([len(feet_alternative) for feet_alternative in feet_alternatives]):
                raise NotEnoughFeet("Remaining feet ({}) are not enough for {}.".format(raw_feet, " or ".join(feet_alternatives)))
            else:
                raise WrongFeet("None of the expected feet ({}) was found in: {}.\n    Parsed so far: {}".format(feet_alternatives, raw_feet, final_form))
        if raw_feet != "":
            raise WrongFeet("Feet processed {} but more left {}".format(final_form, raw_feet))


if __name__ == "__main__":
    h = MoraFinder()
    try:
        line = argv[1]
        print(line, end=" - ")
        h.check_line(line)
    except IndexError:
        print("Type exit to quit.")
        line = ""
        while line != "exit":
            if line:
                print(line, end=" - ")
                h.check_line(line)
            line = input(">>> ")
