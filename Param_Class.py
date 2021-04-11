import copy


class Parameter:
    """Constructs a parameter to be used for creating combinatorial patterns"""
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables  
        self.size = len(variables) 
        self.current_var = 0 

    def add(self, val : int) -> int:
        """Adds given value to the parameter and returns how much it carries over"""
        self.current_var += val
        if self.current_var >= self.size: 
            carry_over = self.current_var // self.size
            self.current_var %= self.size
            return carry_over
        else:
            return 0 

    def currentVal(self):
        return self.variables[self.current_var]


class Combination:
    """"Expresses combination of variables"""
    def __init__ (self, params):
        self.params = params
        self.size = len(params)
   
    def increment(self):
        """Increments the combination. Returns True when overflows. """
        original = self.params
        inc_index = self.size - 1
        carry_over = self.params[inc_index].add(1)
        
        if carry_over == 0:
            return False
        
        while carry_over != 0:
            inc_index -= 1
            if inc_index < 0: # overflow
                self.params = original
                return True
            else:
                carry_over = self.params[inc_index].add(carry_over)
        
        return False

    def print(self):
        result = ""
        for param in self.params:
            result += param.currentVal()

        print(result)
        



# counts max combinatorial number of passed parameter list 
def count_all_comb(param_list)-> int:
    '''counts max combinatorial number of passed parameter list'''
    comb_num = 1
    for param in param_list.params:
        comb_num *= param.size
    return comb_num


def all_combination(comb : Combination) ->list:
    """Pass in the parameter list class and get all combinations"""
    result = []
    overflow = False
    while not overflow:
        to_append = copy.deepcopy(comb)
        result.append(to_append)
        overflow = comb.increment()


    return result

