import pycosat as sat_solver
import random
import os
from benchParser import benchParse
from SAFARI import hill_climb
import time
import pandas as pd

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
    path1_results = "experimentDD.csv"
    path2_results = "experimentTrio.csv"
    num_of_iteration_per_model = 3
    #num_of_iteration_per_model = 100
    options = {1,2}
    bp = benchParse()
    dictionary = {}
    dictionary[1] = {}
    dictionary[2] = {}
    for file in onlyfiles:
        for i in range(num_of_iteration_per_model):

            # File name
            file_name = file[:file.index(".")]
            print("Model - %s, Iteration %d "% (file_name,i+1))
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

            for option in options:
                if not file_name in dictionary[option]:
                    dictionary[option][file_name] = []
                # Preforming the algorithm
                start = time.time()
                diagnosis = hill_climb(DS, a, M, N, option=option)
                end = time.time()
                total_time = end-start
                dictionary[option][file_name].append(total_time)

    df1 = pd.DataFrame.from_dict(dictionary[1])
    df2 = pd.DataFrame.from_dict(dictionary[2])
    df1.to_csv(path1_results)
    df2.to_csv(path2_results)


def get_min_cardinality(diagnoses):
    min_card = None
    #print(diagnoses)
    for diagnosis in diagnoses:
        if min_card == None or len(diagnosis)<min_card:
            min_card = len(diagnosis)
    return min_card



def experiment2():
    """
    Thjs function will conduct the experiment
    :return: Experiment results
    """
    path = "%s\\res" % os.getcwd()
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    tests = []

    max_m = 10
    #max_m = 100
    #num_of_iteration_per_model = 10
    num_of_iteration_per_model = 2
    options = {1,2}
    bp = benchParse()
    dictionary_time = {}
    dictionary_quality = {}
    dictionary_time[1] = {}
    dictionary_quality[1] = {}
    dictionary_time[2] = {}
    dictionary_quality[2] = {}
    #for file in {"c17.","c432.","c499."}:
    for file in {"c17.","c432."}:

        # File name
        file_name = file[:file.index(".")]
        path1_time_results = "experiment_DD_time.csv"
        path1_quality_results = "experiment_DD_quality.csv"
        path2_time_results = "experiment_trio_time.csv"
        path2_quality_results = "experiment_trio_quality.csv"

        for i in range(max_m):

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
            for option in options:
                num_of_bugs = 3
                a = get_random_observation_with_x_bugged_components(num_of_bugs, BM)
                print(a)
                M = i + 1
                N = 4

                sum_time = 0
                sum_card = 0
                for j in range(num_of_iteration_per_model):
                    if not file_name in dictionary_quality[option]:
                        dictionary_quality[option][file_name] = {}
                        dictionary_time[option][file_name] = {}


                    # Preforming the algorithm
                    start = time.time()
                    diagnosis = hill_climb(DS, a, M, N, option=option)
                    end = time.time()
                    total_time = end-start
                    sum_time += total_time
                    sum_card += get_min_cardinality(diagnosis)
                dictionary_time[option][file_name]["%d"%M]=sum_time/float(num_of_iteration_per_model)
                dictionary_quality[option][file_name]["%d"%M]=sum_card/float(num_of_iteration_per_model)



        df1_time = pd.DataFrame.from_dict(dictionary_time[1])
        df1_quality = pd.DataFrame.from_dict(dictionary_quality[1])
        df2_time = pd.DataFrame.from_dict(dictionary_time[2])
        df2_quality = pd.DataFrame.from_dict(dictionary_quality[2])
        df1_time.to_csv(path1_time_results)
        df1_quality.to_csv(path1_quality_results)
        df2_time.to_csv(path2_time_results)
        df2_quality.to_csv(path2_quality_results)



if __name__ == "__main__":
    experiment()
    experiment2()