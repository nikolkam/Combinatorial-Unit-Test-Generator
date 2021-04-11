import ast
import Param_Class as param
import codegen


# function to test
def foo(a,b,c):
    return a*b-c



class FunctionCallVisitor(ast.NodeVisitor):
    def __init__(self, name):
        self.name = name
        self.func = ast.FunctionDef()
        
    
    def visit_FunctionDef(self,node : ast.FunctionDef) -> bool:
        if(node.name == self.name):
            print(ast.dump(node))
            self.func = node
        return True

    def visit_Call(self,node : ast.Call):
        #if(node.name == self.name):
        print(ast.dump(node))




def get_func_def(tree, name):
    '''Look for a function definition with the specific name'''    
    func_calls = []
    func_visitor = FunctionCallVisitor(name)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
        # if isinstance(node, ast.Call):
            if func_visitor.visit(node):
                break

    return func_visitor.func


def form_arguments(arg : param.Combination):
    """Takes combinationand forms argument list for AST"""
    arguments = []
    for a in arg.params:
        arguments.append(ast.Constant(value=a.currentVal(), kind=None))
    return arguments


def create_func_call(func_name : str, arg : param.Combination):
    """Takes in function name and Parameter and forms AST function calls"""
    arguments = form_arguments(arg)
    
    call = ast.Call(
        func = ast.Name(
            id = func_name,
            ctx = ast.Load()
        ),
        args = arguments,
        keywords = []
    )

    return call

def main():
    to_parse = 'foo.py'
    code = ast.parse(open(to_parse).read())
    test_func = get_func_def(code, 'foo')

    p1 = param.Parameter('a', [1,2,3])
    p2 = param.Parameter('b', [4,5,6])
    p3 = param.Parameter('c', [7,8,9])
    comb = param.Combination([p1,p2,p3])   
    comb = param.all_combination(comb)

    func_calls = []
    for c in comb:
        call = create_func_call(test_func.name,c)
        codegen.to_source(call)
        func_calls.append(call)



   


    foo(1,2,3)
    # foos = find_foo()
    # func_calls.
    #FunctionCallVisitor().visit(code)




if __name__ == "__main__":
    main()