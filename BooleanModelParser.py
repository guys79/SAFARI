import os
from Description import literal,Component,booleanModel
class BooleanModelParse:
    def get_boolean_model_and_test(self,file_name):
        path = "%s\\res\\%s.isc.txt" % (os.getcwd(),file_name)
        text = self.get_text(path)
        node_num_to_name = self.node_num_to_name(text)
        input_name_to_literal = self.get_model_inputs(text)
        for name in input_name_to_literal.keys():
            lit = input_name_to_literal[name]
           # print("%s - %s" % (name,lit.get_id()))
        model = self.build_model(text,node_num_to_name,input_name_to_literal)
        return model
    def get_text(self,path):
        file = open(path,'r')
        with file:
            data = file.readlines()
            return data

    def node_num_to_name(self,text):
        node_num_to_name = {}
        for line in text:
            split = line.split(" ")
            if self.is_number(split[0][0]):
                node_num_to_name[split[0]] = split[1]
        return node_num_to_name


    def get_model_inputs(self,text):
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
        try:
            int(num)
            return True
        except:
            return False


v = BooleanModelParse()
mod = v.get_boolean_model_and_test("2")
cnf = mod.get_model_cnf()
print(cnf)
mod.print_name_model_cnf()
mod.print_model_cnf()