from models import Testcase

class CodeTester():

    def __init__(self, func_name: str, func: str):
        self.func_name = func_name
        self.func = func

    def __type_mapping(self, v: str, v_type: str):
        '''
        Private method to return correct type for a variable

        Inputs:
        v       --  value as a string
        v_type  --  value type as a string

        Output:
        v as its correct type, else None if type is not str, int, or float
        '''
        if v_type == "str" or v_type == "string" or v_type == "String":
            return str(v)
        elif v_type == "int" or v_type == "Int":
            return int(v)
        elif v_type == "float" or v_type == "Float":
            return float(v)
        else:
            return None
    
    def test_single_case(self, test_input: str, input_type: str, test_output: str, output_type: str):
        '''
        Method to test a single testcase

        Input:
        test_input  --  testcase input
        input_type  --  testcase input type (str, int, or float)
        test_output --  testcase output
        output_type --  testcase output type (str, int, or float)

        Output:
        returns 1 if the testcase is passed, 0 otherwise
        '''

        # Edge Case: func is empty string
        if(self.func.replace(' ', '') == ""):
            return 0

        exec(self.func)                             # Executes the user defined function and makes it callable

        global_params = {}                          # Allows execution of only __builtins__ functions      

        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(self.func_name)
        local_params = {self.func_name: method}     # Allows execution of user defined method 

        func_input = self.__type_mapping(test_input, input_type)
        desired_ouput = self.__type_mapping(test_output, output_type)

        out = eval(self.func_name, global_params, local_params)(func_input)
        if out != desired_ouput:
            return 0
        else:
            return 1

    def test_on_cases(self, test_cases: list[Testcase]):
        '''
        Method to test multiple testcases passed as a list

        Input:
        test_cases  --  A list with elements of the type Testcase 

        Output:
        returns the proportion of test cases passed
        '''
        cases_passed = 0
        for case in test_cases:
            cases_passed += self.test_single_case(case.case_input, case.input_type, case.case_output, case.output_type)
        prop_passed = cases_passed / len(test_cases)
        return prop_passed


if __name__ == "__main__":

    code = """def test(a):
            return a+5
    """
    tester = CodeTester("test", code)

    case1 = Testcase(1, "1", "int", "6", "int")
    case2 = Testcase(1, "2", "int", "7", "int")
    case3 = Testcase(1, "3", "int", "9", "int")

    percent = tester.test_on_cases([case1, case2, case3])
    print(percent)