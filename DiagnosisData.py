class DiagnosisData():
    """
    This class will contain the diagnoses
    """
    def __init__(self):
        """
        The constructor of the class
        """
        self.dictionary={} # Component name value - list of diagnoses' indexes
        self.index=0

    def add_diagnosis(self,diagnosis):
        """
        This function will add the diagnostic to the data structure
        :param diagnosis: The given diagnosis
        :return:
        """
        for component in diagnosis:
            comp_name = component.get_name()
            index_list = set()
            if comp_name in self.dictionary:
                index_list = self.dictionary[comp_name]
            index_list.add(self.index)
            self.dictionary[comp_name] = index_list
        self.index += 1


    def delete_diagnosis(self,diagnosis_index):
        """
        :param diagnosis: list of components
        :this function deletes the diagnosis from the data structure
        """
        to_delete = []
        for component_name in self.dictionary.keys():
            if diagnosis_index in self.dictionary[component_name]:
                self.dictionary[component_name].remove(diagnosis_index)
                if len(self.dictionary[component_name]) == 0:
                    to_delete.append(component_name)
        for comp_name in to_delete:
            del self.dictionary[comp_name]



    def search_sub_diagnosis(self,diagnosis):
        """
        This function will check if the given diagnosis is a sub-diagnosis
        of any of the diagnoses.
        :param diagnosis: The given diagnosis
        :return: A set of indexes where each index is the index of the super-set diagnosis
        """
        diagnosis_name = []
        for component in diagnosis:
            component_name = component.get_name()
            diagnosis_name.append(component_name)

        first = True
        for component_name in diagnosis_name:
            if component_name in self.dictionary:
                index_set = self.dictionary[component_name]
                if first:
                    intersection = index_set
                    first = False
                else:
                    intersection = index_set.intersection(intersection)
            else:
                return set()
        return intersection


    def get_all_diagnosis(self):
        """
        :return: list of all diagnoses
        """
        diagnoses={}  # dictionary of index and the components of the diagnosis of the index
        for component in self.dictionary.keys():
            for index in self.dictionary.get(component):
                if index in diagnoses:  # already found the diagnosis
                    diagnoses.get(index).append(component)
                else:  # nre diagnosis
                    diagnoses[index]=[component]
        # organize in list of diagnosis:
        diagnoses_list=[]
        for index in diagnoses.keys():
            diagnoses_list.append(diagnoses.get(index))
        return diagnoses_list


