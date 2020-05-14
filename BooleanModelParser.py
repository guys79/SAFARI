import os
from Description import literal,booleanModel

class BooleanModelParse:
    """
    This class will read from a text file, parse it and create from
    it the boolean model
    """

    def get_boolean_model(self,file_name):
        """
        This function will return the boolean model from the given file
        :param file_name: The name of the file
        :return: The boolean model
        """
        path = "%s\\res\\%s.isc.txt" % (os.getcwd(),file_name)
        text = self.get_text(path)
        node_num_to_name = self.node_num_to_name(text)
        input_name_to_literal = self.get_model_inputs(text)
        model = self.build_model(text,node_num_to_name,input_name_to_literal)
        return model


    def get_text(self,path):
        """
        This function will get the file's text
        :param path: The path to the file
        :return: The files text
        """
        file = open(path,'r')
        with file:
            data = file.readlines()
            return data

    def node_num_to_name(self,text):
        """
        This function will create a dictionary.
        key - node number, value - the name of the node
        :param text: The file's text
        :return: The dictionary
        """
        node_num_to_name = {}
        for line in text:
            split = line.split(" ")
            if self.is_number(split[0][0]):
                node_num_to_name[split[0]] = split[1]
        return node_num_to_name


    def get_model_inputs(self,text):
        """
        This function will infer from the text the inputs and will crate them
        :param text: The file's text
        :return: A dictionary where the key is the name of the node and the value is the literal object
        """
        names_to_literal = {}
        id = 1
        num_of_from = 0
        for line in text:
            split = line.split(" ")
            if self.is_number(split[0][0]):
                if num_of_from ==0:
                    if split[2] == "inpt":
                        num_of_from = int(split[3])
                        if num_of_from == 1:
                            num_of_from = 0
                        new_input = literal(id)
                        id += 1
                        names_to_literal[split[1]] = new_input
                else:
                    names_to_literal[split[1]] = new_input
                    num_of_from -=1
        return names_to_literal

    def build_model(self,text,node_num_to_name,name_to_literal):
        """
        This function will create the boolean model
        :param text: The file's text
        :param node_num_to_name: Dictionary, key - node number, value - node name
        :param name_to_literal: Dictionary, key - node name, value - literal object
        :return: The new boolean model
        """
        inputs = list(name_to_literal.values())
        model = booleanModel(len(inputs),inputs=inputs)
        for i in range(len(text)):
            split = text[i].split(" ")
            if self.is_number(split[0][0]):
                if split[2] != "inpt" and split[2] !="from":
                    func = split[2]
                    output_num = int(split[3])
                    inputs = text[i+1].split("\t")
                    input_literals = []
                    for k in range(1,len(inputs)):
                        name = node_num_to_name["%d" %(int(inputs[k]))]
                        liter = name_to_literal[name]
                        input_literals.append(liter)
                    comp = model.create_component(input_literals,func)
                    output_literal = comp.get_output()
                    if output_num !=1:
                        for j in range(output_num):
                            node_name = text[i+2+j].split(" ")[1]
                            name_to_literal[node_name] = output_literal
                    else:
                        node_name = text[i].split(" ")[1]
                        name_to_literal[node_name] = output_literal
        return model

    def is_number(self,num):
        """
        This function will return true IFF the given string is a number
        :param num: The given string
        :return: True IFF the given string is a number
        """
        try:
            int(num)
            return True
        except:
            return False


v = BooleanModelParse()
mod = v.get_boolean_model("2")
cnf = mod.get_model_cnf()
print(cnf)
mod.print_name_model_cnf()
mod.print_model_cnf()