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

class Component:
    """
    This class represent a single description of a component
    """

    def __init__(self,inputs,output,functionality):
        """
        The constructor of the class
        :param inputs: The inputs of the component (group of literals)
        :param output: The output of the component (a literal)
        :param functionality: The functionality of the component
        """
        self.inputs = inputs
        self.output = output
        self.health = literal("health")
        self.functionality = functionality
        self.cnf = self.get_CNF_representation()

    def get_CNF_representation(self):
        """
        This function will return the CNF representation of the component
        :return: TEH cnf representation of the component
        """

        if self.functionality == "and":
            return self.and_function()
        elif self.functionality == "nand":
            return self.nand_function()
        elif self.functionality == "or":
            return self.or_function()
        elif self.functionality == "nor":
            return self.nor_function()
        elif self.functionality == "xor":
            return self.xor_function()
        elif self.functionality == "xnor":
            return self.xnor_function()

    def not_function(self):
        """
        CNF not function
        :return: CNF not function
        """
        if len(self.inputs)!=1:
            raise Exception("More than one input")
        # 1- health, 2- input, 3 - output
        c1 = [-1,-2,-3]
        c2 = [-1,2 ,3]
        return [c1,c2]

    def and_function(self):
        """
        CNF and function
        :return: CNF and function
        """

        if len(self.inputs)<2:
            raise Exception("less than two input")
        clauses = []
        end_clause = [-1]
        for i in range(len(self.inputs)):
            clause = [-1,i+2,-1*(len(self.inputs)+2)]
            end_clause.append(-1 * (i + 2))
            clauses.append(clause)
        end_clause.append(len(self.inputs) + 2)
        clauses.append(end_clause)
        return clauses

    def nand_function(self):
        """
        CNF nand function
        :return: CNF nand function
        """

        if len(self.inputs)<2:
            raise Exception("less than two input")
        clauses = []
        end_clause = [-1]
        for i in range(len(self.inputs)):
            clause = [-1,i+2,len(self.inputs)+2]
            end_clause.append(-1 * (i + 2))
            clauses.append(clause)
        end_clause.append(-1*(len(self.inputs) + 2))
        clauses.append(end_clause)
        return clauses

    def or_function(self):
        """
        CNF or function
        :return: CNF or function
        """

        if len(self.inputs)<2:
            raise Exception("less than two input")
        clauses = []
        end_clause = [-1]
        for i in range(len(self.inputs)):
            clause = [-1,-1*(i+2),len(self.inputs)+2]
            end_clause.append(i + 2)
            clauses.append(clause)
        end_clause.append(-1*(len(self.inputs) + 2))
        clauses.append(end_clause)
        return clauses

    def nor_function(self):
        """
        CNF nor function
        :return: CNF nor function
        """

        if len(self.inputs) < 2:
            raise Exception("less than two input")
        clauses = []
        end_clause = [-1]
        for i in range(len(self.inputs)):
            clause = [-1, -1*(i+2), -1*(len(self.inputs) + 2)]
            end_clause.append(i + 2)
            clauses.append(clause)
        end_clause.append(len(self.inputs) + 2)
        clauses.append(end_clause)
        return clauses

    def xor_function(self):
        """
        CNF xor function
        :return: CNF xor function
        """

        if len(self.inputs)!=2:
            raise Exception("not two inputs")
        # 1- health, 2- input1 , 3 - input2, 4- output
        c1 = [-1, -2, -3 , -4]
        c2 = [-1, 2 ,3, -4]
        c3 = [-1, 2 ,-3, 4]
        c4 = [-1, -2 ,3, 4]

        return [c1,c2,c3,c4]

    def xnor_function(self):
        """
        CNF xnor function
        :return: CNF xnor function
        """

        if len(self.inputs) != 2:
            raise Exception("not two inputs")

        # 1- health, 2- input1 , 3 - input2, 4- output
        c1 = [-1, -2, -3, 4]
        c2 = [-1, 2, 3, 4]
        c3 = [-1, 2, -3, -4]
        c4 = [-1, -2, 3, -4]

        return [c1, c2, c3, c4]


func = "xnor"
des1 = Component([1,2],[1],func)
#des2 = Description([1,2,3],[1],func)
print(des1.cnf)
#print(des2.function_converters)