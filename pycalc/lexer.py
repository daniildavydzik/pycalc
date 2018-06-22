import re
from pycalc.object_types import *
from pycalc.constants import Constants


class Error(Exception):
    pass


class Lexer:

    def get_lexem_array(self, str):
        ''' Method that returns list of lexems.
            :param str: String with math expression.
            :return : List of lexems/tokens.
        '''
        new_str = self.pre_tokinaze(str)
        if new_str is None:
            return '0'
        n = len(new_str)
        j = 0
        ar_lec = []
        if len(new_str) > 0:
            accum = new_str[0]
        else:
            return new_str

        for i in range(1, n + 1):
            if i == n:
                ar_lec.insert(j, accum)
                break

            if (accum == '-' or accum == '+') and i == 1:
                ar_lec.append(accum)
                j += 2
                accum = new_str[i]
                continue

            if accum in Constants.sign_arr and new_str[i] == '=':
                accum += new_str[i]
                continue

            if (re.match(Constants.tpl, accum[0]) or accum[0] == '.')and (re.match(Constants.tpl, new_str[i]) or new_str[i] == '.'):
                accum += new_str[i]
                continue

            if (new_str[i].isalpha() or re.match(Constants.tpl, new_str[i])) and re.match(Constants.letter_reg, accum):
                accum += new_str[i]
            else:
                ar_lec.insert(j, accum)
                j += 1
                accum = new_str[i]
        ar_lec = self.remove_unary_minus(ar_lec)
        lexem_array = self.add_multiply_sign(ar_lec)
        return lexem_array

    def par_check(self, expression):
        ''' Method that check for validity of brackets.
            :param expression: String with math expression.
            :return : True or False, depends on validity of brackets of a given expression.
        '''
        mapping = dict(zip('({[', ')}]'))
        queue = []
        for letter in expression:
            if letter in mapping:
                queue.append(mapping[letter])
            elif letter not in mapping.values():
                continue
            elif not (queue and letter == queue.pop()):
                return False
        return not queue

    def pre_tokinaze(self, str):
        ''' Method that do a number of operations before tokenization.
            :param str: String with a math expression.
            :return : Amended string with a math expression.
        '''
        str.lower()
        if self.par_check(str):
            normalize_str = self.normalize_string(str)
            valid_string = self.validate_string(normalize_str).replace(" ", "")
            return valid_string
        else:
            raise Error('Brackets not balanced')

    def normalize_string(self, str):
        ''' Method that normalize string with expression. If we have more than one space between symbol,
            it change multiply spaces with one space.
            :param str: String with a math expression.
            :return : Normalized string with a math expression.
        '''
        return re.sub(Constants.spaces_reg, ' ', str).strip()

    def validate_string(self, str):
        ''' Method that raise error if string with a math expression is not valid.
            :param str: String with a math expression.
            :return : string with a math expression if it is valid.
        '''
        indices = enumerate(str)
        for i, char in indices:
            if char in Constants.sign_arr:
                if str[i + 1] == ' ' and str[i + 2] == '=':
                    raise Error('invalid syntax')
            elif char.isdigit() and i != len(str) - 1:
                if str[i + 1] == ' ' and str[i + 2].isdigit():
                    raise Error('invalid syntax')

        return str

    def remove_unary_minus(self, ar_lec):
        ''' Method that delete redundant unary symbols.
            :param ar_lec: list of tokens.
            :return : Amended list without redundant unary symbols.
        '''
        sign_arr = []
        i = len(ar_lec) - 1
        start_index = None
        while i != -1:
            if ar_lec[i] != '-' and ar_lec[i] != '+':
                start_index = i
                i -= 1
                continue

            if ar_lec[i] == '-' or ar_lec[i] == '+':
                sign_arr.append(ar_lec[i])
                i -= 1

            if ar_lec[i] != '-' and ar_lec[i] != '+' and ar_lec[i] != '(' and len(sign_arr) >= 0:
                end_index = i
                sign_arr = list(filter(lambda a: a == '-', sign_arr))

                if start_index is None:
                    raise Error('not valid')

                if len(sign_arr) % 2 == 0:
                    ar_lec[end_index + 1:start_index] = ['+']
                    sign_arr.clear()
                else:
                    ar_lec[end_index + 1:start_index] = ['-']
                    sign_arr.clear()

            if ar_lec[i] == '(' and len(sign_arr) >= 0:
                end_index = i
                sign_arr = list(filter(lambda a: a == '-', sign_arr))

                if len(sign_arr) % 2 != 0:
                    ar_lec[end_index + 1:start_index] = ['-']
                    sign_arr.clear()
                else:
                    ar_lec[end_index + 1:start_index] = ['+']
                    sign_arr.clear()

        return ar_lec

    def add_multiply_sign(self, arr_lex):
        ''' Method that add multiply sign in list of tokens.
            :param ar_lex: list of tokens.
            :return : Amended list of tokens.
        '''
        i = 0
        while i != len(arr_lex) - 1:
            if re.match(Constants.tpl, arr_lex[i]) and arr_lex[i + 1] == '(':
                arr_lex.insert(i + 1, '*')
            elif re.match(Constants.tpl, arr_lex[i]) and re.match(Constants.letter_reg, arr_lex[i + 1]):
                arr_lex.insert(i + 1, '*')
            elif arr_lex[i] == ')' and re.match(Constants.tpl, arr_lex[i + 1]):
                arr_lex.insert(i + 1, '*')
            elif re.match(Constants.letter_reg, arr_lex[i]) and re.match(Constants.tpl, arr_lex[i + 1]):
                arr_lex.insert(i + 1, '*')
            elif arr_lex[i] == ')' and arr_lex[i + 1] == '(':
                arr_lex.insert(i + 1, '*')
            i += 1

        return arr_lex

    def find_unary_minus(self, lexem_array):
        ''' Method that find unary symbols.
            :param lexem_array: list of tokens.
            :return : List of indices of unary operators.
        '''
        find_unary = enumerate(lexem_array)
        unary_indecies = []
        if len(lexem_array) <= 1:
            return []
        for index, lexem in find_unary:
            if index == 0 and lexem_array[index] in ['+', '-']:
                unary_indecies.append(index)

            if index != len(lexem_array) - 1 and lexem in operators_dict and lexem_array[index+1] in ['+','-'] :
                unary_indecies.append(index+1)
            elif lexem == '(' and lexem_array[index+1] in ['+','-']:
                unary_indecies.append(index+1)

        return unary_indecies

