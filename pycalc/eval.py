from pycalc.object_types import *
from pycalc.parse_functions import FunctionParser
from pycalc.lexer import Lexer, Error
from copy import copy
from pycalc.constants import Constants
import re


def calculate(exp):

    def shunting_yard(exp):
        ''' Method that returns postfix polish notation of math expression.
            :param exp: String with math expression.
            :return : Postfix polish notation of math expression.
        '''
        lexer = Lexer()
        parsed_formula = lexer.get_lexem_array(exp)
        stack = []
        indices = lexer.find_unary_minus(parsed_formula)
        parsed_formula = enumerate(parsed_formula)
        for index,token in parsed_formula:
            if token in operators_dict or token in FunctionParser.functions_dict:

                if token in operators_dict:

                    if index in indices:
                        token_obj = operators_dict['unary_minus'] if token == '-' else operators_dict['unary_plus']
                    else:
                        token_obj = operators_dict[token]

                else:
                    token_obj = copy(operators_dict['func'])
                    token_obj.name = token

                while stack and stack[-1] != "(" and token_obj.priority <= stack[-1].priority and token_obj.is_binary \
                        and token_obj.associativity == 1:
                    yield stack.pop()

                stack.append(token_obj)

            elif token in FunctionParser.constants_dict:
                token_obj = copy(operators_dict['const'])
                token_obj.const = FunctionParser.constants_dict[token]
                yield token_obj

            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x

            elif token == "(":
                stack.append(token)

            elif re.match(Constants.tpl, token):
                yield token

            else:
                raise Error(f'name {token} is not defined')

        while stack:
            yield stack.pop()

    def calc(polish):
        ''' Method that calculate value of given expression.
            :param polish: List with tokens of expression in polish notation.
            :return : Value of math expression.
        '''
        polish = list(polish)
        stack = []
        if all(isinstance(term, Operator) for term in polish):
            raise Error('not valid input')
        for token in polish:
            if isinstance(token, Operator):
                if token.name:
                    x = stack.pop()
                    stack.append(token.func(FunctionParser.functions_dict[token.name], x))
                elif token.const:
                    stack.append(float(token.const))
                elif not token.is_binary:
                    x = stack.pop()
                    stack.append(token.func(x))
                else:
                    try:
                        y, x = stack.pop(), stack.pop()
                        stack.append(token.func(x, y))
                    except Exception as e:
                        raise Error(f' binary operation must have two operands')
                    
            else:
                stack.append(float(token))
        return stack[0]

    return calc(shunting_yard(exp))


if __name__ == '__main__':
    lexer = Lexer()
    lex_arr = lexer.get_lexem_array('(3+(4*5)/10)-sin(3)+pow(3,2)')
    parser = FunctionParser()
    result = calculate('(3+(4*5)/10)-sin(3)+pow(3,2)')
    print(f'result = {result}')