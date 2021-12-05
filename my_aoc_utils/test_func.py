import sys
import textwrap
from typing import List

class FunctionTester:
    def __init__(self, func):
        self.test_num = 0
        self.func = func 

    def test(self, **kwargs):  
        """
        Test 'self.func' with the given keyword arguments. Keyword args are required for all args.
        This is beacuse the answer is parsed using keywords.

        If a test is succesful, the answer will be returned.
        """
        try: 
            self.test_num += 1
            ans = kwargs['ans']
            inputs = [v for k,v in kwargs.items() if k != 'ans']
            # CALL FUNCTION TO BE TESTED 
            res = self.func(*inputs)
            if res != ans:  
                print("---------------------")      
                print(f"TEST {self.test_num}")
                str_res = textwrap.shorten(str(res), width=500)
                str_inputs = textwrap.shorten(str(inputs), width=500)
                print(f"Got: \n{str_res}\nExpected:\n{ans}\nFor input:\n{str_inputs}")
            return res
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            while exception_traceback.tb_next != None:
                exception_traceback = exception_traceback.tb_next 
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno

            print(f"Exception in test number: {self.test_num} on line {line_number} in file {filename}")
            print(e)

