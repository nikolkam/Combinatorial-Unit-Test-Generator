import ast
import param
import copy

# function to test
def foo(a,b,c):
    return a*b-c



class FunctionDefVisitor(ast.NodeVisitor):
    """Visitor implementation to extract certain function definition AST based on name"""
    def __init__(self, name):
        """@name : Name of function to extract"""
        self.name = name
        self.func = []
        
    
    def visit_FunctionDef(self,node : ast.FunctionDef) -> bool:
        if(self.name == None or node.name in self.name):
            self.func.append(node)
            return True
        else:
            return False


def get_func_def(tree, name = None)-> list:
    '''Look for a function definition with the specific name'''    
    func_visitor = FunctionDefVisitor(name)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_visitor.visit(node)
                
    if func_visitor.func == []:
        print("Function defitions not found.")
        exit()
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

def create_func_def(func_def: ast.FunctionDef, args: param.Combination)-> ast.FunctionDef:
    """Creates function definition with passed FunctionDef and args as defaults"""
    args = form_arguments(args)
    func_def.args.defaults = args

    return func_def

def printFuncDefAST(funcDef : ast.FunctionDef()):
    temp = copy.deepcopy(funcDef)
    temp.body = []
    print(ast.unparse(temp))

