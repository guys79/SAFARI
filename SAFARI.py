from trie import TrieNode

def random_diagnosis(SD, a):
    """
    Returns a random diagnosis using SAT solver
    :param SD: The rules that defines the connection between the components
    :param a: The observation
    :return: A random diagnosis
    """
    pass


def improved_diagnosis(w):
    """
    This function will return the diagnosis with one less negative literal
    :param w: The diagnosis
    :return: The diagnosis with one less negative literal
    """
    pass


def doesnt_entail_false(SD, a, w_tag):
    """
    SD ∧ a ∧ w′ 6|=⊥
    :param SD: The rules that defines the connection between the components
    :param a: The observation
    :param w_tag: The diagnosis
    :return: True IFF the above expression is satisfied
    """
    pass


def is_subsumed(R, w):
    """
    returns true if w subsumed in R
    :param R: Thr Trie
    :param w: The diagnosis
    :return: True if w subsumed in R
    """
    pass


def add_to_trie(R, w):
    """
    This function will add the diagnosis to the Trie
    :param R: Thr Trie
    :param w: The diagnosis
    :return:
    """
    pass

def remove_subsumed(R,w):
    """
    Removes from R all the diagnoses that are subsumed in w
    :param R: Thr Trie
    :param w: The diagnosis
    :return:
    """
    pass


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

    R = TrieNode('*')
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

        if not is_subsumed(R,w):
            add_to_trie(R,w)
            remove_subsumed(R,w)

        n+=1
    return R

