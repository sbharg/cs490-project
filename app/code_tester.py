from app.models import Testcase, Question

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

    def check_for_loop(self):
        return "for" in self.func.partition('\r')[2]
    
    def check_while_loop(self):
        return "while" in self.func.partition('\r')[2]

    def check_recursion(self):
        return self.func_name in self.func.partition('\r')[2]
            
    def test_single_case(self, case: Testcase):
        '''
        Method to test a single testcase

        Input: case  --  Testcase object
        Output: returns an array containing and integer and a string
                If the function passes the testcase, the int is a one and zero otherwise.
                The string returned is the user's output to the input, or None if there is a failure somewhere
        '''

        test_input = case.case_input
        test_output = case.case_output
        if test_output[0] == "\"" or test_output[0] == "\'":
            test_output = test_output[1:-1]

        # Edge Case: func is empty string
        if(self.func.replace(' ', '') == ""):
            return [0, None]

        try:
            exec(self.func)                         # Executes the user defined function and makes it callable
        except SyntaxError:
            return [0, None]                       

        global_params = {}                          # Allows execution of only __builtins__ functions      

        possibles = globals().copy()
        possibles.update(locals())
        method = possibles.get(self.func_name)
        local_params = {self.func_name: method}     # Allows execution of user defined method 

        try:
            out = eval(self.func_name + '(%s)' % test_input, global_params, local_params)
        except NameError:
            return [0, None]
        
        if str(out) != test_output:
            return [0, out]
        else:
            return [1, out]

    def auto_grade(self, test_cases: list[Testcase], constraint = None):
        '''
        Method to test multiple testcases and passed as a list and a constraint

        Input:  test_cases  --  A list with elements of the type Testcase 
                constraint  --  A string detailing a type of constraint
        Output: returns the proportion of test cases passed and a mask of constraints/testcases passed
        '''
        cases = len(test_cases)
        cases_passed = 0
        constraints = 1
        constraints_passed = 0
        mask = []

        if self.check_func_name():
            constraints_passed += 1
            mask.append(1)
        else:
            mask.append(0)

        if constraint != None:
            if constraint == "for":
                if self.check_for_loop():
                    constraints_passed += 1 
                    mask.append(1)
                else:
                    mask.append(0)
                constraints += 1
            elif constraint == "while":
                if self.check_while_loop():
                    constraints_passed += 1 
                    mask.append(1)
                else:
                    mask.append(0)
                constraints += 1
            elif constraint == "recursion":
                if self.check_recursion():
                    constraints_passed += 1 
                    mask.append(1)
                else:
                    mask.append(0)
                constraints += 1
        
        for case in test_cases:
            if self.test_single_case(case)[0] == 1:
                cases_passed += 1
                mask.append(1)
            elif self.test_single_case(case)[0] == 0:
                mask.append(0)
        
        prop = (cases_passed + constraints_passed) / (cases + constraints)
        return [prop, mask]

    def get_total_items(self, q: Question):
        cases = len(q.testcases)
        constraints = 1
        if q.for_flag:
            constraints += 1
        elif q.while_flag:
            constraints += 1
        elif q.rec_flag:
            constraints += 1

        cases += constraints
        return cases

if __name__ == "__main__":

    code = """def test(a):
            return a+5
    """
    tester = CodeTester(code, 'test')

    case1 = Testcase(1, "1", "int", "6", "int")
    case2 = Testcase(1, "2", "int", "7", "int")
    case3 = Testcase(1, "3", "int", "9", "int")

    percent = tester.test_on_cases([case1, case2, case3])
    print(percent)