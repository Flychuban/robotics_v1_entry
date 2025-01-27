
from timeit import default_timer as timer

class FunctionTracer:
    def __init__(self, func_name: str, message_postfix: str):
        self.start = timer()
        self.func_name = func_name #compute_solution
        self.message_postfix = message_postfix #seconds
 
    def __del__(self):
        end = timer()
        print(f"{self.func_name} took {end - self.start} {self.message_postfix}")