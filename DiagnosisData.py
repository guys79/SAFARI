

class DiagnosisData():
    def __init__(self):
        self.dictionary={}
        self.index=0

    def add_diagnosis(self,diagnosis):
        pass

    #todo test
    def delete_diagnosis(self,diagnosis_index):
        '''
        :param diagnosis: list of components
        :this function deletes the diagnosis from the data structure
        '''
        for component_name in self.dictionary.keys():
            if self.dictionary.get(component_name).contains(diagnosis_index):
                self.dictionary.get(component_name).remove(diagnosis_index)


    def search_sub_diagnosis(self,diagnosis):
        pass

    #todo test
    def get_all_diagnosis(self):
        '''
        :return: list of all diagnoses
        '''
        diagnoses={}#dictionary of index and the components of the diagnosis of the index
        for component in self.dictionary.keys():
            for index in self.dictionary.get(component):
                if index in diagnoses:#already found the diagnosis
                    diagnoses.get(index).append(component)
                else:#nre diagnosis
                    diagnoses[index]=[component]
        #orginaize in list of diagnosis:
        diagnoses_list=[]
        for index in diagnoses.keys():
            diagnoses_list.append(diagnoses.get(index))
        return diagnoses_list

