class ObservationParser:
    '''
    this class parse and return all observations for certain model
    '''
    def __init__(self,model_name):
        self.model_name=model_name

    def get_observations(self):
        file_name=self.model_name+"_iscas85.obs"
        f = open("observations\\"+file_name, "r")
        observations_list=[]
        for line in f:
            information=line[1:len(line)-3]#get line information only
            if information[-1]!=']':
                information=information+"]"
            information=information.split(",")
            literal_array=information[2:len(information)]#only the literal array
            literal_array[0]=literal_array[0][1:]#first literal
            literal_array[-1]=literal_array[-1][:-1]#first literal
            observation=[]
            for i in range(len(literal_array)):
                if literal_array[i].__contains__("-"):
                    observation.append((i+1)*-1)
                else:
                    observation.append(i+1)
            observations_list.append(observation)
        return observations_list





#test
parser=ObservationParser("74181")
print(parser.get_observations())