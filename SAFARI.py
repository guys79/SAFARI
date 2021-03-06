from DiagnosisData import DiagnosisData
import pycosat as sat_solver
from Description import booleanModel
import random
from trie import TrieNode

def random_diagnosis(SD, a):
    """
    Returns a random diagnosis using SAT solver
    :param SD: The rules that defines the connection between the components
    :param a: The observation
    :return: A random diagnosis
    """
    cnf = SD.get_model_cnf()
    for observation in a:
        cnf.append([observation])

    solution = sat_solver.solve(cnf)
    rand = random.randrange(15)
    for i in range(rand):
        solution = sat_solver.solve(cnf)
        cnf.append([-x for x in solution])

    healthy,not_healthy = SD.get_diagnosis(solution)
    return healthy,not_healthy


def improved_diagnosis(w):
    """
    This function will return the diagnosis with one less negative literal
    :param w: The diagnosis
    :return: The diagnosis with one less negative literal
    """
    not_healthy = w[1]
    healthy = w[0]
    w_tag = [[],[]]

    for comp in healthy:
        w_tag[0].append(comp)

    for comp in not_healthy:
        w_tag[1].append(comp)

    if len(not_healthy) > 0:
        random.shuffle(w_tag[1])
        w_tag[0].append(w_tag[1][0])
        w_tag[1].remove(w_tag[1][0])

    return w_tag[0], w_tag[1]


def doesnt_entail_false(SD, a, w_tag):
    """
    SD ∧ a ∧ w′ 6|=⊥
    :param SD: The rules that defines the connection between the components
    :param a: The observation
    :param w_tag: The diagnosis
    :return: True IFF the above expression is satisfied
    """
    cnf_model = SD.get_model_cnf()
    healthy = w_tag[0]
    non_healthy = w_tag[1]

    for comp in healthy:
        cnf_model.append([comp.get_health().get_id()])

    for comp in non_healthy:
        cnf_model.append([-1*(comp.get_health().get_id())])

    for observation in a:
        cnf_model.append([observation])

    sol = sat_solver.solve(cnf_model)


    if sol == 'UNSAT':
        return False
    return True

#works for the 2 data structures
def is_subsumed(sub_sumed_indexes):
    """
    Ths function will check if there are diagnoses that are subsumed using the indexes
    :param sub_sumed_indexes: The list of indexes
    :return: True if there is a diagnosis that is subsumed
    """
    return len(sub_sumed_indexes) !=0

#works for the 2 data structures
def add_to_trie(R, w):
    """
    This function will add the diagnosis to the Trie
    :param R: The Data Structure
    :param w: The diagnosis
    """
    R.add_diagnosis(w)

#works for the 2 data structures
def remove_subsumed(R, diagnoses_to_delete):
    """
    Removes from R all the diagnoses that are subsumed in w
    :param R: Thr Data Structure
    :param diagnoses_to_delete: The diagnosis indexes to delete
    """
    for diagnosis in diagnoses_to_delete:
        R.delete_diagnosis(diagnosis)

#works for the 2 data structures
def convert_trie_to_set_of_components(R):
    """
    This function will convert the Trie of diagnoses to a group of diagnoses
    :param R: The Trie
    :return: The group of diagnoses
    """
    diagnosis =  R.get_all_diagnosis()

    return diagnosis


def hill_climb(DS, a, M, N, option=1):
    """
    The Hill CLimb algorithm from the paper (The main algorithm)
    :param option:
    :param DS: <SD,COMPS,OBS>. SD - the rules that defines the connection between the components.
                COMPS - The components of the model. OBS - The inputs and outputs.
    :param a: The observation
    :param M: Climb restart limit
    :param N: number of tries
    :param option: 1 if we want to use our data structure, 2 if we want to use the Trie
    :return: list of diagnoses
    """
    SD = DS[0]
    COMPS = DS[1]
    OBS = DS[2]
    if option==1:
        R = DiagnosisData()
    elif option==2:
        R=TrieNode("*")
    else:
        return
    n = 0
    while n < N:
        w = random_diagnosis(SD,a)
        m = 0
        while m< M:
            w_tag = improved_diagnosis(w) # should be improved_diagnosis(w.p)
            if doesnt_entail_false(SD,a,w_tag):
                if len(w_tag[1]) == 0:
                    return [[]]
                w = w_tag
                m = 0
            else:
                m +=1
        sub_diagnoses = R.search_sub_diagnosis(w[1])
        if not is_subsumed(sub_diagnoses):
            add_to_trie(R,w[1])
            remove_subsumed(R,sub_diagnoses)

        n+=1
    if option == 1:
        if R.index == 0: #No Solution
            return None
    elif option == 2:
        if len(R.children)==0:
            return None
    return convert_trie_to_set_of_components(R)




"""
# create model
input_num = 3
BM = booleanModel(input_num)

# The inputs
x = BM.names["input_1"]
y = BM.names["input_2"]
z = BM.names["input_3"]

# First AND gate
and_0 = BM.create_component([x,y],"and")

# Second AND gate
and_1 = BM.create_component([z,y],"and")

# First OR gate
or_0 = BM.create_component([and_0.get_output(),and_1.get_output()],"or")

COMPS = [and_0,and_1,or_0]
OBS = [x,y,z,or_0.get_output()]

DS = [BM,COMPS,OBS]
a = [x.get_id(),y.get_id(),1*(z.get_id()),-1*(or_0.get_output().get_id())]
M = 4
N = 4
print(hill_climb(DS,a,M,N))
"""


