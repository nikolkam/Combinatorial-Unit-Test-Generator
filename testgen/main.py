import call_generator as gen
import copy
import ast
import param

def parse_vals(string):
    string.replace(" ","")
    string.split(",")
    return string

def print_func_sig(func_def, with_num = True):
    to_str = ""
    num = 1
    if isinstance(func_def, ast.FunctionDef):
        if with_num:
            num = 1
            to_str += "[" + str(num) + "] "

        temp = copy.deepcopy(func_def)
        temp.body = []
        print(to_str,ast.unparse(temp))
    elif isinstance(func_def, list):
        for func in func_def:
            if with_num:
                to_str = "[" + str(num) + "] "
            temp = copy.deepcopy(func)
            temp.body = []
            print(to_str,ast.unparse(temp))
            num += 1
    else:
        print("none")

if __name__ == "__main__":
    # get the test file
    while True:
        file_name = input("Input the file path to test (absolute/relative): ")
        print(file_name)
        if not file_name.endswith(".py"):
            print("You must specify a python file (.py)")
            continue
        
        try:
            file = open(file_name).read()
        except FileNotFoundError:
            print("File path ",file_name," not found. Input a valid path.")
            continue
        
        break
       
    file = ast.parse(file)
    func_defs = gen.get_func_def(file)
    print_func_sig(func_defs)
    range = "[1-"+str(len(func_defs))+"]"
    print(range)
    while True:
        try:
            func_to_parse = int(input("Choose function to construct test on "+range+": "))
        except ValueError:
            print("You must enter integer.")
            continue
        if not (1<=func_to_parse and func_to_parse<= func_defs.__len__()):
            print("You must enter integer between "+range)
            continue
        break

    func_def = func_defs[func_to_parse-1]
    print("Constructing tests on...")
    print_func_sig(func_def, False)
    
   
    print("Choose arguments to perform combinatorial input pertitioning.")

    params = []
    consts = []
    print("Input y to include set them as combinatorial params (any input except y will set them to constants)")


    print("Set parameter's possible values seperated by comma.")
    print('Eg. degree: float(150), float(250.0), animal: "cat", "dog", "mouse" locations: list("sea","mountain","city") ')
    parameters = []
    for a in func_def.args.args:
        val = input(a.arg+": ")
        val = parse_vals(val)
        vals = val.split(",")
        print(vals)
        parameter = param.Parameter(a.arg, vals)
        #parameter
        parameters.append(parameter)

    while True:
        t = int(input("Enter the strength of the test T="))
        if t > parameters.__len__():
            print("T must be in between 1-",parameters.__len__())
            continue
        break
    combination = param.Combination(parameters)
    if t == parameters.__len__():
        combination = param.all_combination(combination)
    else:
        T = param.TwiseConstructor(parameters, t)
        print(T.param_vecs)
        print(T.value_vec)
        combination = T.t_wise

    
    func_ast = []
    resulting_ast = []
    for c in combination:
        c.print()
        result = copy.deepcopy(gen.create_func_def(func_def, c))
        func_ast.append(result)
        file.body.append(result)
        func_defs.append(func_ast)



    print(ast.unparse(file))