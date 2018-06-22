import unittest
from pycalc.lexer import Lexer, Error
from pycalc.eval import calculate
from pycalc.parse_functions import FunctionParser


class TestLexerMethods(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.function_parser = FunctionParser()

    def test_normalize_string(self):
        self.assertEqual(self.lexer.normalize_string('2+   3 >   =   8'), '2+ 3 > = 8')
        self.assertNotEqual(self.lexer.normalize_string('2+3 >        =9'), '2+3 >=9')

    def test_find_unary_minus(self):
        self.assertEqual(self.lexer.find_unary_minus('2+3*-9/(-3)'), [4, 8])
        self.assertEqual(self.lexer.find_unary_minus('2+3*-9/(---+-3)'), [4, 8, 9, 10, 11, 12])
        self.assertEqual(self.lexer.find_unary_minus('2+3*-+9/(-3)'), [4, 5, 9])
        self.assertEqual(self.lexer.find_unary_minus('2+3*+-9/(+3)'), [4, 5, 9])
        self.assertNotEqual(self.lexer.find_unary_minus('3+-9/(3)'), [1, 2])
        self.assertEqual(self.lexer.find_unary_minus('2+3*+-sin(2)/(2+3)'), [4, 5])

    def test_get_lexem_array(self):
        self.assertEqual(self.lexer.get_lexem_array('3*---2+5*(-----1)'), ['3', '*', '-', '2', '+', '5', '*', '(', '-', '1', ')'])
        self.assertEqual(self.lexer.get_lexem_array('log10(10)'), ['log10', '(', '10', ')'])
        self.assertEqual(self.lexer.get_lexem_array('log10(.10)'), ['log10', '(', '.10', ')'])
        self.assertEqual(self.lexer.get_lexem_array('log10(1.0)'), ['log10', '(', '1.0', ')'])
        self.assertEqual(self.lexer.get_lexem_array('log10(1.0)*e'), ['log10', '(', '1.0', ')', '*', 'e'])
        self.assertEqual(self.lexer.get_lexem_array('log10(1.0)>=e'), ['log10', '(', '1.0', ')', '>=', 'e'])

    def test_add_multiply_sign(self):
        self.assertEqual(self.lexer.add_multiply_sign(['log10', '(', '1.0', ')', '(', 'e', ')']), ['log10', '(', '1.0', ')', '*', '(', 'e', ')'])
        self.assertEqual(self.lexer.add_multiply_sign(['log10', '(', '1.0', ')', '4']), ['log10', '(', '1.0', ')', '*', '4'])
        self.assertEqual(self.lexer.add_multiply_sign(['(', '1.0', ')', '(', '4', ')']), ['(', '1.0', ')', '*', '(', '4', ')'])
        self.assertEqual(self.lexer.add_multiply_sign(['2', 'log10', '(', '1.0', ')', '4']),['2', '*', 'log10', '(', '1.0', ')', '*', '4'])
        self.assertEqual(self.lexer.add_multiply_sign(['4', '(', '1.0', ')', '4']), ['4', '*', '(', '1.0', ')', '*', '4'])

    def test_validation(self):
        expressions = ["2 >= 4 5", "2 > = 45", "2 ! = 45", "2 < = 45", "2 = = 4 5"]
        for expression in expressions:
            with self.assertRaises(Error) as context_manager:
                self.lexer.validate_string(expression)
            self.assertIn("invalid syntax", str(context_manager.exception))
        self.assertEqual(self.lexer.validate_string("2 >= 45"), "2 >= 45")

    def test_par_checker(self):
        self.assertFalse(self.lexer.par_check('(()'))
        self.assertFalse(self.lexer.par_check('(()))'))
        self.assertFalse(self.lexer.par_check('(()}'))
        self.assertTrue(self.lexer.par_check('((((()))))'))
        self.assertTrue(self.lexer.par_check('3'))
        self.assertTrue(self.lexer.par_check('((3 + 5))'))

    def test_remove_unary_minus(self):
        tokenized_exp = ['-', '+', '-', '3', '-', '+', '-', '5', '-', '(', '-', '-', '-', '+', '-', '-', '5', ')']
        result_exp = ['+', '3', '+', '5', '-', '(', '-', '5', ')']
        self.assertEqual(self.lexer.remove_unary_minus(tokenized_exp), result_exp)


class TestCalculateMethod(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.function_parser = FunctionParser()

    def test_calculate(self):
        str_exp = 'sin(-cos(-sin(3.0)-cos(-sin(-3.0*5.0)-sin(cos(log10(43.0))))+cos(sin(sin(34.0-2.0^2.0))))--cos(1.0)--cos(0.0)^3.0)'
        self.assertEqual(calculate(str_exp), 0.5361064001012784)
        self.assertEqual(calculate('(3+(4*5)/10)+pow(3,2)'), 14.0)


if __name__ == '__main__':
    unittest.main()
