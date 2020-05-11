class literal:
    """
    This class represents a literal
    """

    def __init__(self,name):
        """
        The constructor of the literal
        :param name: The name of the literal
        """
        self.value = False
        self.name = name

    def set_value(self,value):
        """
        This function will set the value of the literal
        :param value: The value
        :return:
        """
        self.value = value

    def get_value(self):
        """
        This function will return the value of the literal
        :return: The value of the literal
        """
        return self.value

class Description:
    """
    This class represent a single description of a component
    """

    def __init__(self,inputs,output,cnf):
        """
        The constructor of the class
        :param inputs: The inputs of the component (group of literals)
        :param output: The output of the component (a literal)
        :param cnf: The CNF expression that represents the functionality of the component
        """
        self.inputs = inputs
        self.output = output
        self.cnf = cnf






