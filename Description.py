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
        """
        This function will return the is of the literal
        :return: The literal's id
        """
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
        func = self.functionality.lower()
        if func == "and":
            return self.and_function()
        elif func == "nand":
            return self.nand_function()
        elif func == "or":
            return self.or_function()
        elif func == "nor":
            return self.nor_function()
        elif func == "xor":
            return self.xor_function()
        elif func == "xnor":
            return self.xnor_function()
        elif func == "not":
            return  self.not_function()
        elif func == "buff":
            return self.buff_function()
        else:
            raise Exception("Function not recognized")


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

    def buff_function(self):
        """
           CNF buff function
           :return: CNF buff function
        """
        c1 = [-1*(self.health.get_id()),self.inputs[0].get_id(),self.output.get_id()]
        c2 = [-1*(self.health.get_id()),-1*(self.inputs[0].get_id()),-1*(self.output.get_id())]
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
    def __init__(self,input_num,inputs = None):
        """
        The constructor of the class
        :param input_num: The number of model inputs
        """
        self.num_of_literals = 0
        self.names = {}
        if inputs == None:
            self.inputs = []
            for i in range(input_num):
                self.inputs.append(self.create_literal())
        else:
            self.inputs = inputs
            self.num_of_literals = len(self.inputs)
        for i in range(len(self.inputs)):
            self.names["input_%d"%(self.inputs[i].get_id())] = self.inputs[i]

    def set_outputs(self,outputs):
        """
        This function will set the outputs
        :param outputs: The given outputs
        :return: None
        """
        self.outputs = outputs

    def get_outputs(self):
        """
        This function will return the outputs of the model
        :return: The outputs of the model
        """
        return self.outputs

    def get_healthy_literals(self):
        """
        This function will return the healthy literals in the model
        :return: The healthy literals in the model
        """
        healthy = []
        for comp in self.names.values():
            try:
                healthy.append((comp.get_health(),comp))
            except:
                1
        return healthy

    def get_diagnosis(self,cnf_solution):
        """
        This function will infer from the cnf solution the diagnosis
        :param cnf_solution: The cnf solution
        :return: a list of the healthy components and a list of non-healthy components (the diagnosis)
        """
        healthy = self.get_healthy_literals()
        healthy_comp = []
        not_healthy_comp = []

        for health in healthy:
            value = cnf_solution[health[0].get_id()-1]
            if value<0:
                not_healthy_comp.append(health[1])
            else:
                healthy_comp.append(health[1])
        return healthy_comp, not_healthy_comp


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

    def get_components(self):
        """
        This function will return the components of the model
        :return: The components of the model
        """
        values = self.names.values()
        comps = []
        for val in values:
            try:
                val.get_health()
                comps.append(val)
            except(Exception):
                pass

        return comps

    def get_inputs(self):
        """
        This function will return the inputs of the model
        :return: The inputs of the model
        """
        return self.inputs

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

    def create_component(self,inputs,func):
        """
        This function will create a component
        :param inputs: The inputs of the components (other components' outputs)
        :param num_of_input: The number of inputs (besides the already received inputs)
        :param func: The functionality of the component
        :return: The component
        """
        health = self.create_literal()
        output = self.create_literal()
        comp_name = self.name_component(func)
        comp = Component(inputs, output, func, health,comp_name)
        self.names[comp_name] = comp
        return comp

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
x = BM.names["input_1"]
y = BM.names["input_2"]
z = BM.names["input_3"]

# First AND gate
and_0 = BM.create_component([x,y],"and")

# Second AND gate
and_1 = BM.create_component([z,y],"and")

# First OR gate
or_0 = BM.create_component([and_0.get_output(),and_1.get_output()],"or")
#