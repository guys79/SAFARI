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


def add(root, new_diagnosis):
    """
    Adding a diagnosic in the trie structure
    """
    components_names=sorted([component.name for component in new_diagnosis])
    node = root
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


def find_prefix(root, semi_diagnosis) -> Tuple[bool, int]:
    """
    Check and return 
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    components_names=sorted([component.name for component in semi_diagnosis])
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for name in components_names:
        component_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.component_name == name:
                # We found the component existing in the child.
                component_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if component_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter



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

    cnf = BM.get_model_cnf()
    cnf_name = BM.get_name_model_cnf()
    obs = []
    obs.append([1])
    obs.append([2])
    obs.append([-3])
    # obs.append([9])
    obs.append([-9])
    diagnosis=[and_1,or_0]
    root = TrieNode('*')
    add(root, diagnosis)
    print("is True:",find_prefix(root, diagnosis))
    print("is False:",find_prefix(root,[and_0]))
    #add another one:
    new_comp=BM.create_component([x,y],"or")
    diagnosis.append(new_comp)
    add(root, diagnosis)
    add(root,[and_0])
    print("is True:",find_prefix(root, diagnosis))
    print("is False:",find_prefix(root,[and_0,and_1]))
    print("is True:",find_prefix(root, [and_0]))
