import copy
from itertools import repeat

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

    def param_size(self):
        return len(self.params)

    def get_comb_num(self):
        '''Number of combinatorial this list of parameters can make'''
        result = 1
        for p in self.params:
            result *= p.size
        return result

    def get_params(self, param_vec:list):
        '''Takes bit param vector and returns corresponding parameters'''
        result = []
        for i,p in enumerate(param_vec):
            if p == 1:
                result.append(copy.copy(self.params[i]))
        return Combination(result)

    def get_value(self):
        '''Value represent by combination'''
        val = 0
        for i,p in enumerate(self.params):
            #print("var = ",p.current_var," i =",i,"p.size = ",p.size)
            val += p.current_var*(p.size**i)
        return val

    def get_combination(self,value):
        '''Updates combination to a specified value'''
        for p in reverse(self.params):
            p.size()

    def print(self):
        result = ""
        for param in self.params:
            result += param.currentVal() 

        print(result)
        
class ParamVector:
    '''Uses parameter vector represent t combination of parameters'''
    def __init__(self, p :int, t: int):
        '''@p: number of parameters
           @t: strength of test
        '''
        self.t = t
        self.p = p
        self.param_vec = [1]*t+[0]*(p-t) 
        self.vecs = [self.param_vec]
        
    def increment(self):
        '''Find next bigger param vector with t combinations'''
        self.param_vec = copy.copy(self.param_vec)
        
        # find least significant bit that is 0 followed by 1
        one = False # previous element is one
        for g,element in enumerate(self.param_vec):
            if element == 1:
                one = True
            elif one:
                break
            else:
                one = False
        #case 1
        if self.param_vec[0] == 1:
            self.param_vec[g] = 1
            self.param_vec[g-1] = 0
        
        #case 2
        else:
            #c: count number of 1's after g
            c = sum(i == 1 for i in self.param_vec[g+1:])
            self.param_vec[g] = 1
            set1 = self.t-c-1
            #set all index before g: index < set1 to 1, others to 0
            for i in range(0,g):
                if(set1 != 0):
                    self.param_vec[i] = 1
                    set1 -= 1
                else:
                    self.param_vec[i] = 0
        self.vecs.append(self.param_vec)

    def enumarated(self):
        '''Returns true if all values are enumarated'''
        if all(i == 1 for i in self.param_vec[-self.t:]):
            return True
        else:
            return False

    def all_comb(self):
        while not self.enumarated():
            self.increment()


    def print(self):
        print(self.param_vec)


class TwiseConstructor:
    def __init__(self, params:list, t:int):
        '''Constructs a T-wise testing combination'''
        self.t = t
        self.params = params
        self.param_size = params.__len__()
        self.param_vecs = self.construct_param_vec()
        self.value_vec = self.construct_val_vec()
        self.t_wise = []
        #print(self.param_vecs)
        #construct all combinatorial for T variables
        
        temp = copy.copy(self.params[0:t])
        temp = self.all_comb(temp)

        current_par = t # parameter index currently being added
        matching = self.matching_param_vecs(current_par)


        for _ in range(t,self.param_size):
            temp = self.horizontal_growth(temp)

            

        # print(self.param_vecs)
        # print(self.value_vec)
        temp = self.vertical_growth(temp)


        self.t_wise = temp

    

    def vertical_growth(self,current):
        combs = self.get_uncovered_combs()
        combs = self.get_valid_combs(combs)
        result = []
        for c in combs:
            result.append(self.complete_comb(c))

        for r in result:
            current.append(Combination(r))

        return current


    def complete_comb(self,comb:Combination):
        '''Gets incomplete combination and supplements it with regular vals'''
        result = []
        for p in self.params:
            try:
                match = next(x for x in comb.params if x.name == p.name)
            except StopIteration:
                result.append(copy.copy(p))
                continue
            
            result.append(copy.copy(match))

        return result


    def get_valid_combs(self,combs:Combination):
        '''Gets valid combs from passed combs'''
        valid_combs = []
        new = False

        
        while True:
            #
            for i,c1 in enumerate(combs):
                for j,c2 in enumerate(combs):
                    if i >= j:
                        continue
                    
                    if self.no_conflic(c1,c2):

                        new = True
                        c3 = self.combine_combs(c1,c2)
                        combs.append(c3)
                        del combs[i] 
                        del combs[j]


                    else:
                        new = False

            if not new or combs.__len__() == 1:
                break

        return combs

    def combine_combs(self,comb1:Combination,comb2:Combination):
        '''Takes two combinations and returns the combined combination'''
        combs = copy.copy(comb1.params) #combs = [Param1,Param2,Param3,....]

        for c2 in comb2.params: #c2 = [Param1,]
            for c in combs:

                if c.name != c2.name:
                    combs.append(c2)

        #print("combine_combs =",combs)
        return Combination(combs)

    def get_uncovered_combs(self):
        '''Get all uncovered combs'''
        def find_0(lst):
            found = []
            for i,x in enumerate(lst):
                if x == 0:
                    found.append(i)
            return found

        #get all uncovered combinations
        uncovered_p = self.is_all_covered()
        comb_to_add = []
        for u in uncovered_p:
            vvec  = self.value_vec[u]
            uncovered_v = find_0(vvec)
            comb = Combination(self.get_param(self.param_vecs[u]))
            for uv in uncovered_v:
                c = copy.deepcopy(comb)
                #print(list(range(uv)))
                for i in range(uv):
                    c.increment()
                comb_to_add.append(c)

        # for c in comb_to_add:
        #     print_param_list(c.params)

        return comb_to_add

                
    def no_conflic(self,comb1,comb2):
        '''Takes two combination and returns true if there's no conflict'''
        p1 = comb1.params
        p2 = comb2.params
        # print("p1=",end='')
        # print_param_list(p1)
        # print("p2=",end='')
        # print_param_list(p1)
        
        for c1 in p1:
            for c2 in p2:
                if c1.name == c2.name and c1.current_var != c2.current_var:
                    return False
        return True


    def is_all_covered(self):
        '''Checks for uncovered param vecs and returns all non covered index'''
        non_covered = []
        for i,vec in self.value_vec.items():
            if any(x == 0 for x in vec):
                non_covered.append(i)
        return non_covered

    def horizontal_growth(self,combs):
        '''Adds one variable that maximizes the covered combination'''
        curr_par_index = combs[0].param_size()
        #print("Size = ",curr_par_index)
        matching = self.matching_param_vecs(curr_par_index)
        result = []
        for c in combs:
            result.append(self.horizontal_iteration(c, matching, curr_par_index))
        return result
    
    def horizontal_iteration(self,comb:Combination, matching:list, index:int):
        '''Horizontal iteration '''
        par_to_add = copy.copy(self.params[index])
        par_to_add.current_var = 0

        possible_combs = []
        for i in range(par_to_add.size):
            cp = copy.deepcopy(comb)
            cp.params.append(copy.deepcopy(par_to_add))
            possible_combs.append(cp)
            par_to_add.add(1)
    
        scores = [0]*possible_combs.__len__()
        for i,pc in enumerate(possible_combs):

            #pc.print()
            for m in matching:
  
                c = pc.get_params(m[1])
                #print_param_list(c.params)
                if not self.is_covered(m,c):
                    scores[i] += 1


        result = scores.index(max(scores))

        #print("result =",end="")
        #possible_combs[result].print()
        self.value_vec
        self.update_val_vec(matching, possible_combs[result])
        return possible_combs[result]


        #comb.params.append(self.params[index])
        #print(matching)
        
    def is_covered(self,m,c):
        '''Takes matching param vec and combination, returns true if it's already covered'''
        val = c.get_value()
        to_increment = self.value_vec[m[0]]
        if to_increment[val] == 0:
            return False
        else:
            return True

    def update_val_vec(self,matching,comb):
        '''Takes matching param vecs and combination and updates vallue accordingly'''
        #print(matching)
        
        for m in matching:
            pc = comb.get_params(m[1])
            val = pc.get_value()
            #pc.print()
            #print(val)
            to_increment = self.value_vec[m[0]]
            to_increment[val] = 1  

    def matching_param_vecs(self,index):
        '''Returns all matching param vecs that are covered by index'''
        result = []
        for i,p in enumerate(self.param_vecs):
            if p[index] == 1:
                if all(later == 0 for later in p[index+1:]):
                    result.append((i,p[0:index+1]))
        return result


    def construct_param_vec(self):
        '''Constructs param vector which stores information about parameter combinatorials'''
        pv = ParamVector(self.param_size, self.t)
        pv.all_comb()
        return pv.vecs

    def construct_val_vec(self):
        '''Constructs value vectors which stores information about value combinatorials'''
        vv = dict()
        for i,vec in enumerate(self.param_vecs):
            pl = copy.copy(self.get_param(vec))
            comb_num = Combination(pl).get_comb_num()
            if i == 0:
                vv[i] = [1]*comb_num
            else:
                vv[i] = [0]*comb_num

        return vv

    def get_param(self,param_vec):
        '''Takes param vec and returns corresponding parameters'''
        result = []
        for i in range(param_vec.__len__()):
            if param_vec[i] == 1:
                result.append(copy.copy(self.params[i]))
        return result


    def all_comb(self, params: list):
        '''Takes list of params and constructs all combinatiosn'''
        c = Combination(params)
        c = all_combination(c)
        return c



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

def print_param_list(params):
    print("[", end='')
    for p in params:
        print(" ",p.name,"=",p.currentVal(), end='')
    print(" ]")


