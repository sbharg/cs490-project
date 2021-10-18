from models import Testcase

class CodeTester():

    def __init__(self, func: str, correct_func_name: str):
        self.func = func
        self.correct_func_name = correct_func_name
        self.func_name = func.partition('(')[0][4:]

    '''
    def __type_mapping(self, v: str, v_type: str):
        
        Private method to return correct type for a variable

        Inputs:
        v       --  value as a string
        v_type  --  value type as a string

        Output: v as its correct type, else None if type is not str, int, or float
        
        if v_type == "str" or v_type == "string" or v_type == "String":
            return str(v)
        elif v_type == "int" or v_type == "Int":
            return int(v)
        elif v_type == "float" or v_type == "Float":
            return float(v)
        else:
            return None
    '''

    def check_func_name(self):
        return self.correct_func_name == self.func_name
    
    def test_single_case(self, case: Testcase):
        '''
        Method to test a single testcase

        Input: case  --  Testcase object
        Output: returns 1 if the testcase is passed, 0 otherwise
        '''

        test_input = case.case_input
        test_output = case.case_output

        # Edge Case: func is empty string
        if(self.func.replace(' ', '') == ""):
            return 0

        try:
            exec(self.func)                         # Executes the user defined function and makes it callable
        except SyntaxError:
            return 0                       

        global_params = {}                          # Allows execution of only __builtins__ functions      

        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(self.func_name)
        local_params = {self.func_name: method}     # Allows execution of user defined method 

        try:
            out = eval(self.func_name + '(%s)' % test_input, global_params, local_params)
        except NameError:
            return 0
        
        if str(out) != test_output:
            return 0
        else:
            return 1

    def test_on_cases(self, test_cases: list[Testcase]):
        '''
        Method to test multiple testcases passed as a list

        Input: test_cases  --  A list with elements of the type Testcase 
        Output: returns the proportion of test cases passed
        '''
        cases_passed = 0
        for case in test_cases:
            cases_passed += self.test_single_case(case)
        prop_passed = cases_passed / len(test_cases)
        return prop_passed


if __name__ == "__main__":

    code = """def test(a):
            return a+5
    """
    tester = CodeTester(code)

    case1 = Testcase(1, "1", "int", "6", "int")
    case2 = Testcase(1, "2", "int", "7", "int")
    case3 = Testcase(1, "3", "int", "9", "int")

    percent = tester.test_on_cases([case1, case2, case3])
    print(percent)