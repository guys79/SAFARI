from DiagnosisData import DiagnosisData
import pycosat as sat_solver
from Description import literal,Component,booleanModel
import random
def random_diagnosis(SD, a):
    """
    Returns a random diagnosis using SAT solver
    :param SD: The rules that defines the connection between the components
    :param a: The observation
    :return: A random diagnosis
    """
    cnf = SD.get_model_cnf()
    for observation in a:
        cnf.append(observation)

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
    if len(not_healthy) > 0:
        random.shuffle(not_healthy)
        healthy.append(not_healthy[0])
        not_healthy.remove(not_healthy[0])

    return w[0], not_healthy


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
        cnf_model.append(observation)

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
                w = w_tag
                m = 0
            else:
                m +=1
        sub_sumed_index=R.search_sub_diagnosis()
        if not is_subsumed(sub_sumed_index):
            add_to_trie(R,w)
            remove_subsumed(R,sub_sumed_index)

        n+=1
    convert_trie_to_set_of_components(R)


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

cnf = BM.get_model_cnf()
cnf_name = BM.get_name_model_cnf()
obs = []
obs.append([1])
obs.append([2])
obs.append([-3])
#obs.append([9])
obs.append([-9])
w = random_diagnosis(BM,obs)
to_print = []
for comp in w[1]:
    to_print.append(comp.get_name())
print(to_print)
w = improved_diagnosis(w)

to_print = []
for comp in w[1]:
    to_print.append(comp.get_name())
print(to_print)
#w = ([and_0,or_0],[and_1])
print(doesnt_entail_false(BM,obs,w))
print(len("111111111011111111011111111011111111"))