import os
from Description import literal,booleanModel


class SysParser:
    """
    This class will parse a .sys file and build a boolean model
    """


    def get_model(self,file_name):
        """
        This function will return the model described in the file
        :param file_name: The name of the file
        :return: The model described in the file
        """
        path = "%s\\systems\\%s.sys" % (os.getcwd(), file_name)
        text = self.get_text(path)
        model = self.parse_model(text)
        return model

    def get_text(self, path):
        """
        This function will get the file's text
        :param path: The path to the file
        :return: The files text
        """
        file = open(path, 'r')
        with file:
            data = file.readlines()
            return data

    def parse_model(self, text):
        complete_lines = self.transform_into_complete_lines(text)
        # The name of the model
        model_name = complete_lines[0][:len(complete_lines[0])-2]
        # The names of the inputs
        inputs_names = complete_lines[1][1:len(complete_lines[1])-3].split(",")
        # The names of the otputs
        outputs_names = complete_lines[2][1:len(complete_lines[2])-3].split(",")
        # Removed \n and [ and splitted by ], to get an array of components descriptions
        system_des = complete_lines[3][1:len(complete_lines[3])-4].replace("\n","").replace("[","").split("],")

        dictionary_names_to_literals = {}
        dictionary_names_to_ids = {}
        id_counter = 1

        inputs,id_counter = self.get_literals(dictionary_names_to_literals,dictionary_names_to_ids,inputs_names,id_counter)
        outputs = []

        # Creating model and setting the inputs & outputs of the model
        bm = booleanModel(len(inputs),inputs)


        for component_des in system_des:
            split = component_des.split(",")
            func_name = split[0]
            func_name = self.get_func_name(func_name)
            comp_name = split[1]
            output_name = split[2]
            input_names = split[3:]
            # inputs in other
            #output_literal, id_counter = self.get_literal(dictionary_names_to_literals,dictionary_names_to_ids,output_name,id_counter)
            input_literals, id_counter = self.get_literals(dictionary_names_to_literals,dictionary_names_to_ids,input_names,id_counter)
            bm.set_index(id_counter)
            comp = bm.create_component(input_literals,func_name)
            id_counter = bm.get_index()
            comp_output = comp.get_output()

            id_counter = self.add_literal(dictionary_names_to_literals,dictionary_names_to_ids,comp_output,output_name,id_counter)
            if output_name[0] == 'o':
                outputs.append(comp_output)

        bm.set_outputs(outputs)
        return bm,dictionary_names_to_ids,dictionary_names_to_literals



    def transform_into_complete_lines(self,text):
        complete_lines = []
        complete_line = ""
        for line in text:
            complete_line+=line
            if line[len(line)-2:] == ".\n":
                complete_lines.append(complete_line)
                complete_line = ""
        complete_lines.append(complete_line)
        return complete_lines


    def get_literals(self, dictionary_names_to_literals,dictionary_names_to_ids, literal_names,start_id):

        literals = []
        for name in literal_names:
            lit,start_id = self.get_literal(dictionary_names_to_literals,dictionary_names_to_ids,name,start_id)
            literals.append(lit)
        return literals,start_id

    def get_literal(self, dictionary_names_to_literals,dictionary_names_to_ids, name,start_id):
        if name in dictionary_names_to_literals:
            lit = dictionary_names_to_literals[name]
        else:
            lit = literal(start_id)
            dictionary_names_to_literals[name] = literal(start_id)
            dictionary_names_to_ids[name] = start_id
            start_id += 1
        return lit,start_id

    def get_func_name(self, func_name):
        normal_func_name = ""
        for i in range(len(func_name)):
            if self.is_int(func_name[i]):
                break
            normal_func_name = "%s%s" % (normal_func_name,func_name[i])
        return normal_func_name


    def is_int(self, param):
        try:
            int(param)
            return True
        except(Exception):
            return False

    def add_literal(self, dictionary_names_to_literals, dictionary_names_to_ids, literal,name, id_counter):
        dictionary_names_to_ids[name] = id_counter
        id_counter += 1
        dictionary_names_to_literals[name] = literal
        return id_counter


s = SysParser()
model, dictionary_to_id, dictionary_to_literal = s.get_model("c7552")
print()
