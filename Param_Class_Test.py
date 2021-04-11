
""""Unit Test for Parameter Class"""

import pytest
import call_generator as gen
import Param_Class as param
import ast


def test_add():
    p = param.Parameter("Weather", ["Sunny", "Cloudy","Rainy"])
    assert(p.current_var == 0)
    assert(p.size == 3)
    assert(p.name == "Weather")

    assert(p.add(1) == 0)
    assert(p.current_var == 1 and p.currentVal() == "Cloudy")
    assert(p.add(3) == 1)
    assert(p.current_var == 1 and p.currentVal() == "Cloudy")
    assert(p.add(2) == 1)
    assert(p.current_var == 0 and p.currentVal() == "Sunny")
    assert(p.add(11) == 3)
    assert(p.current_var == 2 and p.currentVal() == "Rainy")

def test_combination_increment():
    p1 = param.Parameter(1, ["0","1", "2", "3","4","5","6","7","8","9"])
    p2 = param.Parameter(2, ["0","1", "2", "3","4","5","6","7","8","9"])
    p3 = param.Parameter(3, ["0","1", "2", "3","4","5","6","7","8","9"])

    combination = param.Combination([p1,p2,p3])
    overflow = False
    while not overflow:
        combination.print()
        overflow = combination.increment()

def test_all_combination():
    p1 = param.Parameter(0, ["0","1"])
    p2 = param.Parameter(1, ["0","1"])
    p3 = param.Parameter(2, ["0","1"])
    p4 = param.Parameter(3, ["0","1"])
        
    combination = param.Combination([p1,p2,p3,p4])
    combination = param.all_combination(combination)

    for comb in combination:
        args= gen.form_arguments(comb)
        for arg in args:
            print(ast.dump(arg))
    

test_all_combination()