import importlib


class FunctionParser:
    functions_dict = {}
    constants_dict = {}

    def __init__(self):
        self.parse_modules(['math'])
        self.functions_dict['pow'] = pow
        self.functions_dict['abs'] = abs
        self.functions_dict['round'] = round

    def parse_modules(self, modules):
        ''' Method that parse module names array and add to dictionary their name as a key and
            callable object as a value.
            :param modules: Array of modules names.
        '''
        for module in modules:
            modul = importlib.import_module(module)
            for object in vars(modul):
                if object[0:2] != '__':
                    if isinstance(vars(modul)[object], (int, float, complex)):
                        self.constants_dict[object] = vars(modul)[object]
                    else:
                        self.functions_dict[object] = vars(modul)[object]


