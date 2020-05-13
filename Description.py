class literal:
    """
    This class represents a literal
    """

    def __init__(self,id):
        """
        The constructor of the literal
        :param id: The id of the literal
        """
        try:
            self.id = int(id)
        except:
            raise Exception("id must be integer")


        self.value = False


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

    def get_id(self):
        return self.id

class Component:
    """
    This class represent a single description of a component
    """

    def __init__(self,inputs,output,functionality,health,name):
        """
        The constructor of the class
        :param inputs: The inputs of the component (group of literals)
        :param output: The output of the component (a literal)
        :param functionality: The functionality of the component
        :param health: The health literal
        :param name: The name of the component
        """
        self.inputs = inputs
        self.output = output
        self.health = health
        self.functionality = functionality
        self.cnf = self.get_CNF_representation()
        self.name = name

    def get_name(self):
        """
        This function will return the name of the component
        :return: The name pf the component
        """
        return self.name

    def get_cnf(self):
        """
        This function will return the CNF expression
        :return: The CNF expression
        """
        return self.cnf

    def get_cnf_name(self):
        """
        This function will return the CNF expression with literal names instead of id's
        :return: The CNF expression with literal names instead of id's
        """
        id_name_dictionary = {}
        id_name_dictionary[self.health.get_id()] = "%s_health" % (self.name)
        id_name_dictionary[self.output.get_id()] = "%s_output" % (self.name)
        for i in range(len(self.inputs)):
            input = self.inputs[i]
            id_name_dictionary[input.get_id()] = "%s_input_%d" % (self.name,i)

        name_cnf = []
        for clause in self.cnf:
            name_cnf_clause = []
            for i in range(len(clause)):
                if clause[i] < 0:
                    name_cnf_clause.append("NOT(%s)" %(id_name_dictionary[-1*clause[i]]))
                else:
                    name_cnf_clause.append("%s" % (id_name_dictionary[clause[i]]))
            name_cnf.append(name_cnf_clause)
        return name_cnf

    def get_inputs(self):
        """
        This function will return the inputs of the component
        :return: The inputs of the component
        """
        return self.inputs

    def get_output(self):
        """
        Ths function will return the output of the controller
        :return: the output of the controller
        """
        return self.output

    def get_health(self):
        """
        This function will return the health literal of the component
        :return: The health literal of the component
        """
        return self.health

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
        elif self.functionality == "not":
            return  self.not_function()


    def not_function(self):
        """
        CNF not function
        :return: CNF not function
        """
        if len(self.inputs)!=1:
            raise Exception("More than one input")
        # 1- health, 2- input, 3 - output
        c1 = [-1*(self.health.get_id()),-1*(self.inputs[0].get_id()),-1*(self.output.get_id())]
        c2 = [-1*(self.health.get_id()),self.inputs[0].get_id() ,self.output.get_id()]
        return [c1,c2]

    def and_function(self):
        """
        CNF and function
        :return: CNF and function
        """

        if len(self.inputs)<2:
            raise Exception("less than two input")
        clauses = []
        end_clause = [-1*(self.health.get_id())]
        for i in range(len(self.inputs)):
            clause = [-1*(self.health.get_id()),self.inputs[i].get_id(),-1*(self.output.get_id())]
            end_clause.append(-1 * (self.inputs[i].get_id()))
            clauses.append(clause)
        end_clause.append(self.output.get_id())
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
        end_clause = [-1*(self.health.get_id())]
        for i in range(len(self.inputs)):
            clause = [-1*(self.health.get_id()),self.inputs[i].get_id(),self.output.get_id()]
            end_clause.append(-1 * (self.inputs[i].get_id()))
            clauses.append(clause)
        end_clause.append(-1*(self.output.get_id()))
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
        end_clause = [-1*(self.health.get_id())]
        for i in range(len(self.inputs)):
            clause = [-1*(self.health.get_id()),-1*(self.inputs[i].get_id()),self.output.get_id()]
            end_clause.append(self.inputs[i].get_id())
            clauses.append(clause)
        end_clause.append(-1*(self.output.get_id()))
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
        end_clause = [-1*(self.health.get_id())]
        for i in range(len(self.inputs)):
            clause = [-1*(self.health.get_id()), -1*(self.inputs[i].get_id()), -1*(self.output.get_id())]
            end_clause.append(self.inputs[i].get_id())
            clauses.append(clause)
        end_clause.append(self.output.get_id())
        clauses.append(end_clause)
        return clauses

    def xor_function(self):
        """
        CNF xor function
        :return: CNF xor function
        """

        if len(self.inputs)!=2:
            raise Exception("not two inputs")
        in1 = self.inputs[0].get_id()
        in2 = self.inputs[1].get_id()
        out = self.output.get_id()
        # 1- health, 2- input1 , 3 - input2, 4- output
        c1 = [-1*(self.health.get_id()), -1*in1, -1*in2 , -1*out]
        c2 = [-1*(self.health.get_id()), in1 ,in2, -1*out]
        c3 = [-1*(self.health.get_id()), in1 ,-1*(in2), out]
        c4 = [-1*(self.health.get_id()), -1*(in1) ,in2, out]

        return [c1,c2,c3,c4]

    def xnor_function(self):
        """
        CNF xnor function
        :return: CNF xnor function
        """

        if len(self.inputs) != 2:
            raise Exception("not two inputs")
        in1 = self.inputs[0].get_id()
        in2 = self.inputs[1].get_id()
        out = self.output.get_id()
        # 1- health, 2- input1 , 3 - input2, 4- output
        c1 = [-1*(self.health.get_id()), -1 * in1, -1 * in2, out]
        c2 = [-1*(self.health.get_id()), in1, in2, out]
        c3 = [-1*(self.health.get_id()), in1, -1 * (in2), -1 * out]
        c4 = [-1*(self.health.get_id()), -1 * (in1), in2, -1 *out]
        return [c1, c2, c3, c4]

class booleanModel:
    """
    This class represents the boolean model
    """
    def __init__(self,input_num):
        """
        The constructor of the class
        :param input_num: The number of model inputs
        """
        self.num_of_literals = 0
        self.names = {}
        self.inputs = []
        for i in range(input_num):
            self.inputs.append(self.create_literal())
        for i in range(len(self.inputs)):
            self.names["input_%d"%(i+1)] = self.inputs[i]

    def get_model_cnf(self):
        """
        This function will return the model's cnf
        :return: The model's cnf
        """
        cnf_model = []
        for comp in self.names.values():
            try:
                cnf = comp.get_cnf()
                for clause in cnf:
                    cnf_model.append(clause)
            except:
                type(comp)
        return cnf_model

    def get_name_model_cnf(self):
        """
        This function will return the model's name cnf (literal names instead of id's)
        :return: The model's name cnf
        """
        cnf_model = []
        for comp in self.names.values():
            try:
                cnf = comp.get_cnf()
                for clause in cnf:
                    cnf_model.append(clause)
            except:
                type(comp)
        return cnf_model

    def print_model_cnf(self):
        """
        This function will print the model's cnf
        :return: nothing
        """
        cnf_model = []
        for comp in self.names.values():
            try:
                cnf = comp.get_cnf()
                print(comp.get_name())
                print(cnf)
            except:
                type(comp)
        return cnf_model

    def print_name_model_cnf(self):
        """
        This function will print the model's name cnf (literal names instead of id's)
        :return: nothing
        """
        cnf_model = []
        for comp in self.names.values():
            try:
                cnf = comp.get_cnf_name()
                print(comp.get_name())
                print(cnf)
            except:
                type(comp)
        return cnf_model

    def create_literal(self):
        """
        This function will create a literal
        :return: The literal
        """
        self.num_of_literals +=1
        return literal(self.num_of_literals)

    def create_component(self,inputs,num_of_input,func):
        """
        This function will create a component
        :param inputs: The inputs of the components (other components' outputs)
        :param num_of_input: The number of inputs (besides the already received inputs)
        :param func: The functionality of the component
        :return: The component
        """
        for i in range(num_of_input - len(inputs)):
            inputs.append(self.create_literal())
        health = self.create_literal()
        output = self.create_literal()
        comp_name = self.name_component(func)
        comp = Component(inputs, output, func, health,comp_name)
        self.names[comp_name] = comp

    def name_component(self,func):
        """
        This function will create a name of the component
        :param func: The functionality of the component
        :return: The anme of the component
        """
        i = 0
        name = "%s_%d" % (func,i)
        while name in self.names.keys():
            i+=1
            name = "%s_%d" % (func, i)
        return name

# The example from wikipedia
# https://en.wikipedia.org/wiki/Tseytin_transformation


# create model
input_num = 3
BM = booleanModel(input_num)

# The inputs
x1 = BM.names["input_1"]
x2 = BM.names["input_2"]
x3 = BM.names["input_3"]

# First not gate
BM.create_component([x1],1,"not")
not_0 = BM.names["not_0"]

# Second not gate
BM.create_component([x2],1,"not")
not_1 = BM.names["not_1"]

# First and gate
BM.create_component([not_0.get_output(),x2],2,"and")
and_0 = BM.names["and_0"]

# Second and gate
BM.create_component([not_1.get_output(),x1],2,"and")
and_1 = BM.names["and_1"]

# Third and gate
BM.create_component([not_1.get_output(),x3],2,"and")
and_2 = BM.names["and_2"]

# First or gate
BM.create_component([and_0.get_output(),and_1.get_output()],2,"or")
or_0 = BM.names["or_0"]

# Second or gate
BM.create_component([and_2.get_output(),or_0.get_output()],2,"or")
or_1 = BM.names["or_1"]

#print(BM.get_model_cnf())
#print(BM.get_name_model_cnf())
#BM.print_model_cnf()
BM.print_name_model_cnf()

