from DiagnosisData import DiagnosisData
import pycosat as sat_solver
from Description import booleanModel
import random


def get_random_observation_with_x_bugged_components(x,model):
    cnf = model.get_model_cnf()
    inputs = model.get_inputs()
    outputs = model.get_outputs()
    comps = model.get_components()
    obs = []
    # Get input ids
    id_inputs = []
    for input in inputs:
        id_inputs.append(input.get_id())

    # Get output ids
    id_outputs = []
    for output in outputs:
        id_outputs.append(output.get_id())

    # Get component idsf
    id_comps = []
    for comp in comps:
        id_comps.append(comp.get_health().get_id())

    # Generating random input and adding to cnf
    for i in range(len(inputs)):
        is_1 = bool(random.getrandbits(1))
        if not is_1:
            obs.append(-1*id_inputs[i])
            cnf.append([-1*id_inputs[i]])
        else:
            obs.append(id_inputs[i])
            cnf.append([id_inputs[i]])

    changed = set()
    # Generate x misfunctions
    for i in range(x):
        rand_index = random.randint(0, len(id_comps) - 1)
        while rand_index in changed:
            rand_index = random.randint(0, len(id_comps) - 1)
        changed.add(rand_index)
        cnf.append([id_comps[rand_index]*-1])

    # Solve the cnf
    iter = sat_solver.itersolve(cnf)
    solution_list = list(iter)

    selected = solution_list[0]
    print("solution with misfunction")
    print(selected)

    # After this we have a perfect observation
    for literal in selected:
        if abs(literal) in id_outputs:
            obs.append(literal)
    print("the observation")

    return obs







def is_solution_valid(solution,comp_ids):

    for comp_id in comp_ids:
        if not comp_id in solution: #comp not healthy
            return False
    return True




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

    iter = sat_solver.itersolve(cnf)

    solution_list = list(iter)
    if len(solution_list) == 0:
        raise Exception("F**k in observations")
    random.shuffle(solution_list)
    solution = solution_list[0]
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

    iter = sat_solver.itersolve(cnf_model)

    solution_list = list(iter)
    if len(solution_list) == 0:
        return False
    return True


def is_subsumed(sub_sumed_indexes):
    """
    Ths function will check if there are diagnoses that are subsumed using the indexes
    :param sub_sumed_indexes: The list of indexes
    :return: True if there is a diagnosis that is subsumed
    """
    return len(sub_sumed_indexes) !=0


def add_to_trie(R, w):
    """
    This function will add the diagnosis to the Trie
    :param R: The Data Structure
    :param w: The diagnosis
    """
    R.add_diagnosis(w)

def remove_subsumed(R,sub_sumed_indexes):
    """
    Removes from R all the diagnoses that are subsumed in w
    :param R: Thr Data Structure
    :param sub_sumed_indexes: The diagnosis indexes to delete
    """
    for index in sub_sumed_indexes:
        R.delete_diagnosis(index)


def convert_trie_to_set_of_components(R):
    """
    This function will convert the Trie of diagnoses to a group of diagnoses
    :param R: The Trie
    :return: The group of diagnoses
    """
    return R.get_all_diagnosis()
    pass


def hill_climb(DS, a,M,N):
    """
    The Hill CLimb algorithm from the paper (The main algorithm)
    :param DS: <SD,COMPS,OBS>. SD - the rules that defines the connection between the components.
                COMPS - The components of the model. OBS - The inputs and outputs.
    :param a: The observation
    :param M: Climb restart limit
    :param N: number of tries
    :return: The trie pf diagnoses
    """
    SD = DS[0]
    COMPS = DS[1]
    OBS = DS[2]

    R = DiagnosisData()
    n = 0
    while n < N:
        w = random_diagnosis(SD,a)
        m = 0
        while m< M:
            w_tag = improved_diagnosis(w) # should be improved_diagnosis(w.p)
            if doesnt_entail_false(SD,a,w_tag):
                if len(w_tag[1]) == 0:
                    return []
                w = w_tag
                m = 0
            else:
                m +=1
        sub_sumed_index = R.search_sub_diagnosis(w[1])
        if not is_subsumed(sub_sumed_index):
            add_to_trie(R,w[1])
            remove_subsumed(R,sub_sumed_index)

        n+=1
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

from benchParser import *
bp = benchParse()
file_name = "c17"
BM = bp.get_model(file_name)

COMPS = BM.get_components()
OBS = []
for input in BM.get_inputs():
    OBS.append(input)
for output in BM.get_outputs():
    OBS.append(output)

DS = [BM,COMPS,OBS]

BM.print_name_model_cnf()
BM.print_model_cnf()

num_of_bugs = 3
a = get_random_observation_with_x_bugged_components(num_of_bugs,BM)
print(a)
M = 8
N = 4

diagnosis = hill_climb(DS,a,M,N)

print(diagnosis)

print()
