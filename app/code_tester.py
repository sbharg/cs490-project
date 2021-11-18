from app.models import Testcase, Question

class CodeTester():

    def __init__(self, func: str, correct_func_name: str):
        self.func = func
        self.correct_func_name = correct_func_name
        self.func_name = func.partition('(')[0][4:]

    def check_func_name(self):
        return self.correct_func_name == self.func_name

    def check_for_loop(self):
        return "for" in self.func.partition('\r')[2]
    
    def check_while_loop(self):
        return "while" in self.func.partition('\r')[2]

    def check_recursion(self):
        return self.func_name in self.func.partition('\n')[2]
            
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
        if (self.func.replace(' ', '') == ""):
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


        if not self.check_recursion():
            try:
                out = eval(self.func_name + '(%s)' % test_input, global_params, local_params)
            except NameError:
                return [0, None]
        else:
            func_body = self.func
            func_body = func_body.strip() + "\nret_val = %s(%s)" % (self.func_name, test_input)
            exec(func_body, globals(), globals())
            out = ret_val

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

    code = """def fibo(n):
        if n==1:
            return 1
        elif n==2:
            return 1
        else:
            return fibo(n-1) + fibo(n-2)
    """
    tester = CodeTester(code, 'fibo')

    case1 = Testcase(1, "1", "1")
    case2 = Testcase(1, "2", "1")
    case3 = Testcase(1, "3", "2")
    case4 = Testcase(1, "5", "5")

    percent = tester.auto_grade([case3, case4], 'recursion')
    print(percent)