import pycosat as sat_solver
import random
import os
from benchParser import benchParse
from SAFARI import hill_climb

def get_random_observation_with_x_bugged_components(x,model):
    """
    This function will generate an observation that can happen from 'x' malfunction components
    :param x: An integer - The number of  malfunction components
    :param model: The Boolean model
    :return: An observation that can happen from 'x' malfunction components
    """
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
    selected = sat_solver.solve(cnf)

    """
    solution_list = list(iter)

    selected = solution_list[0]
    print("solution with misfunction")
    print(selected)
    """

    # After this we have a perfect observation
    for literal in selected:
        if abs(literal) in id_outputs:
            obs.append(literal)
    print("the observation")

    return obs


def parse_results_to_csv(query_results):
    """
    This function will parse the results and save them in a csv file name 'results.csv'
    :param query_results: The given data to save
    :return: None
    """
    with open('results.csv', 'w') as file:
        file.write("")
    with open('results.csv','a') as file:
        header = ""
        for key in query_results[0].keys():
            header = "%s%s," % (header,key)
        header = "%s\n" % header
        file.write(header)

    for parse_dictionary in query_results:
        with open('results.csv','a') as f:
            line = ""
            for key in parse_dictionary.keys():
                line = "%s%s," % (line, parse_dictionary[key])
            line = "%s\n" % line
            f.write(line)


def experiment():
    """
    Thjs function will conduct the experiment
    :return: Experiment results
    """
    path = "%s\\res" % os.getcwd()
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    tests = []
    bp = benchParse()
    for file in onlyfiles:
        # File name
        file_name = file[:file.index(".")]

        # The dictionary of the test
        dictionary_test = {}

        # The model
        BM = bp.get_model(file_name)

        # The components
        COMPS = BM.get_components()

        # The observations (input + output)
        OBS = []
        for input in BM.get_inputs():
            OBS.append(input)
        for output in BM.get_outputs():
            OBS.append(output)

        # The final System Description
        DS = [BM, COMPS, OBS]

        # Generating observation with 'x' bugs
        num_of_bugs = 3
        a = get_random_observation_with_x_bugged_components(num_of_bugs, BM)
        print(a)
        M = 8
        N = 4

        # Preforming the algorithm
        diagnosis = hill_climb(DS, a, M, N,option=1 )

        print(diagnosis)

        print()

if __name__ == "__main__":
    experiment()