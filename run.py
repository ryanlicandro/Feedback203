
from nnf import Var
from lib204 import Encoding

givenBoardCondition = ["Wo_11 >> (Wh_21 || Sh_22)", "Wh_21 >> Br_31"]

def create_variables(givenBoardCondition):
    #creating dictionaries for each resource to hold their resources
    whVariables = {}
    brVariables = {}
    woVariables = {}
    shVariables = {}
    variableDictionary = {}

    #Running through each list value in the given board condition and splitting them based on the operators to just leave variable names ie. W_31
    #Then creating a dictionary key value pair where the key is the variable name and the value is a Var with the variable name used as the 
    # constructor value
    for node in givenBoardCondition:
        parts=node.replace(">>"," ").replace("&"," ").replace("|"," ").replace("("," ").replace(")"," ").split()
        for variable in parts:
            variable.strip()
            if "wh" in variable.lower():
                whVariables[parts[variable]] = Var(parts[variable]) 
            if "wo" in variable.lower():
                woVariables[parts[variable]] = Var(parts[variable])
            if "br" in variable.lower():
                brVariables[parts[variable]] = Var(parts[variable])
            if "sh" in variable.lower():
                shVariables[parts[variable]] = Var(parts[variable])
    
    #Merging variable dictionaries into 1 master dictionary containing all variables 
    variableDictionary = merge_dictionaries(merge_dictionaries,whVariables)
    variableDictionary = merge_dictionaries(merge_dictionaries,whVariables)
    variableDictionary = merge_dictionaries(merge_dictionaries,whVariables)
    variableDictionary = merge_dictionaries(merge_dictionaries,whVariables)

    return variableDictionary
    
#method used to merge two dictionaries together, dict1 will be appended onto dict2
def merge_dictionaries(dict1,dict2):
    return(dict2.update(dict1))

def board_Condition_To_Constraints(givenBoardCondition):
    for node in givenBoardCondition:
        parts=node.replace(">>"," ").replace("&"," ").replace("|"," ").replace("("," ").replace(")"," ").split()
        parts[0]=parts[0].strip()
        newConstraint = "~"+parts[0]+"|"
        if len(parts) < 2:
            parts[1] = parts[1].strip()
            newConstraint = newConstraint + parts[1]
        else:
            newConstraint = newConstraint + "("
            for variable in parts:
                variable.strip()
                newConstraint = newConstraint + variable + "|"
            newConstraint=newConstraint.strip("|")
            newConstraint = newConstraint + ")"
        E.add_constraint(newConstraint)
         


# Call your variables whatever you want
variables=create_variables(givenBoardCondition)





#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    #Making Constraints based on board condition
    board_Condition_To_Constraints(givenBoardCondition)
    E.add_constraint(a | b)
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
