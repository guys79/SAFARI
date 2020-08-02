from typing import Tuple
import SAFARI
import Description


class TrieNode(object):
    """
    Our trie node implementation. Very basic. but does the job
    """

    def __init__(self, component_name):
        self.component_name = component_name
        self.children = []
        # Is it the last character of the word.`
        self.diagnosic_finished = False
        # How many times this character appeared in the addition process
        self.counter = 1

    def paths(self):
        '''       private function
        :return: paths of the tree, including *
        '''
        if not self.children:
            return [[self.component_name]]  # one path: only contains self.value
        paths = []
        for child in self.children:
            for path in child.paths():
                paths.append([self.component_name] + path)
        return paths


    def add_diagnosis(self,new_diagnosis):
        """
          Adding a diagnosic in the trie structure
          """
        components_names = sorted([component.name for component in new_diagnosis])
        node = self
        for component_name in components_names:
            found_in_child = False
            # Search for the character in the children of the present `node`
            for child in node.children:
                if child.component_name == component_name:
                    # We found it, increase the counter by 1 to keep track that another
                    # word has it as well
                    child.counter += 1
                    # And point the node to the child that contains this char
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new chlid
            if not found_in_child:
                new_node = TrieNode(component_name)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
        # Everything finished. Mark it as the end of a word.
        node.diagnosic_finished = True

    def get_all_diagnosis(self):
        '''
        :return: list of diagnoses of tree
        '''
        paths=self.paths()
        new_paths=[]
        for diagnosis in paths:
            diagnosis=diagnosis[1:]
            new_paths.append(diagnosis)
        return new_paths

    def search_sub_diagnosis(self, diagnosis):
        """
        :param diagnosis: list of components
        :param root: the Trie root
        :return: true and the sub tree the diagnoses in, false otherwise
        """
        diagnosis_component_names = [component.name for component in diagnosis]
        all_diagnoses = self.get_all_diagnosis()
        sub_trees = []
        for element in all_diagnoses:
            if set(diagnosis_component_names).issubset(set(element)):
                sub_trees.append(element)
        if len(sub_trees) == 0:
            return []
        else:
            return sub_trees

    def delete_diagnosis(self,diagnosis):
        '''
           this function deletes sub tree with full diagnosis
           :param root: root of the Trie
           :param diagnosis: list of components *names*
           '''
        self.recursive_delete(self.children, diagnosis, 0)


    def recursive_delete(self,nodes, components, i):
        '''
        helper function!
        :param nodes: list of nodes
        :param components: list of the diagnoses components name
        :param i: the index of run
        '''
        for node in nodes:
            if node.component_name == components[i]:
                if len(node.children) == 0:  # leaf node
                    nodes.remove(node)
                elif len(node.children) == 1:  # only 1 diagnosis need to delete in the end
                    self.recursive_delete(node.children, components, i + 1)
                    nodes.remove(node)
                else:  # more than 1 diagnosis
                    self.recursive_delete(node.children, components, i + 1)





if __name__ == "__main__":
    # create model
    input_num = 3
    BM = SAFARI.booleanModel(input_num)

    # The inputs
    x = BM.names["input_1"]
    y = BM.names["input_2"]
    z = BM.names["input_3"]

    # First AND gate
    and_0 = BM.create_component([x, y], "and")

    # Second AND gate
    and_1 = BM.create_component([z, y], "and")

    # First OR gate
    or_0 = BM.create_component([and_0.get_output(), and_1.get_output()], "or")

    new_comp=BM.create_component([x,y],"or")

    or_2=BM.create_component([x,y],"or")

    #tests
    diagnosis=[or_2,or_0]
    diagnosis2=[or_0,new_comp]
    root = TrieNode('*')
    root.add_diagnosis(diagnosis2)
    print(root.get_all_diagnosis())
    root.add_diagnosis(diagnosis)
    print(root.get_all_diagnosis())
    diagnosis.append(new_comp)
    root.add_diagnosis(diagnosis)
    print(root.get_all_diagnosis())
    root.add_diagnosis([and_1,and_0])
    print(root.get_all_diagnosis())
    print("delete....")
    root.delete_diagnosis(['or_0','or_2'])
    print(root.get_all_diagnosis())


#todo:add remove function that removes diagnosic.need to assume that the trie has only minimal diagnosic
# so if we delete diagnosic we need to delete the leaf nodes recursively(if not leaf than there is another diagnostic that uses that nodr
#todo: search function but not by order as it is now- to find diagnosis of [and_0,or_1] in trie where exist [and_0,and_1,or_1]
#mabye to do it we can export all possible diagnosis to list of list of names and for list of names ask if contains what we
#want to find?