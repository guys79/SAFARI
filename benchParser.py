import os
from Description import *

class benchParse:
    """
    This class will parse a bench file and build a boolean model
    """


    def get_model(self,file_name):
        """
        This function will return the model described in the file
        :param file_name: The name of the file
        :return: The model described in the file
        """
        path = "%s\\res\\%s.bench.txt" % (os.getcwd(), file_name)
        text = self.get_text(path)
        model = self.parse_model(text)
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



    def get_inputs(self,text):
        """
        This function will return the inputs of the model
        :param text: The text in the file
        :return: The inputs of the model
        """
        inputs = []
        name_to_literal = {}
        id = 1
        for i in range(len(text)):
            line = text[i]
            if line[0] != '#':
                inpt = "INPUT"
                if len(line) >= len(inpt) + 3:

                    if inpt == line[:len(inpt)]:
                        new_input = literal(id)
                        id+=1
                        last_bracket = line.rindex(')')
                        name = line[len(inpt)+1:last_bracket].strip()
                        name_to_literal[name] = new_input
                        inputs.append(new_input)
        return inputs,name_to_literal


    def get_outputs(self,text):
        """
       This function will return the outputs' names of the model
       :param text: The text in the file
       :return: The outputs' names in the model
       """
        outputs = []
        for i in range(len(text)):
            line = text[i]
            if line[0] != '#':
                output = "OUTPUT"
                if len(line) >= len(output) + 3:

                    if output == line[:len(output)]:
                        last_bracket = line.rindex(')')
                        name = line[len(output)+1:last_bracket].strip()
                        outputs.append(name)
        return outputs

    def parse_model(self, text):
        """
        This function will parse the model described in the text and will return a new model
        :param text: The text in the file
        :return: A new model (the one described in the file)
        """
        inputs, name_to_literal = self.get_inputs(text)
        created = set()
        changed = True
        model = booleanModel(len(inputs),inputs = inputs)
        while changed:
            changed = False
            for i in range(len(text)):
                line = text[i]

                if len(line) !=0 and line[0] != '#' and line!='\n':
                    output = "OUTPUT"
                    input = "INPUT"
                    if (len(line)<len(output) + 3 or output != line[:len(output)]) and (len(line)<len(input)+3 or input != line[:len(input)]):
                        line = line.replace(" ","")
                        delimiter = "="
                        index_delimiter = line.index(delimiter)
                        index_bracket = line.index("(")
                        num_in_string = line[:index_delimiter]
                        if not num_in_string in created:
                            func = line[index_delimiter+len(delimiter):index_bracket]
                            #print("d%sd" % line[index_bracket+1:len(line)-2].replace(" ",""))
                            names = line[index_bracket+1:len(line)-2].replace(" ","").split(",")
                            input_literals = []

                            are_all_inputs_exist = True

                            for name in names:
                                if name in name_to_literal:
                                    literal = name_to_literal[name]
                                    input_literals.append(literal)
                                else:
                                    are_all_inputs_exist = False
                                    break

                            if are_all_inputs_exist:
                                comp = model.create_component(input_literals,func)
                                changed = True
                                name_to_literal[num_in_string] = comp.get_output()
                                created.add(num_in_string)
        outputs  = self.get_outputs(text)
        out_lit  = []
        for output_name in outputs:
            lit = name_to_literal[output_name]
            out_lit.append(lit)
        model.set_outputs(out_lit)
        return model


"""
from os import listdir
from os.path import isfile, join

path = "%s\\res" % os.getcwd()
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

bp = benchParse()
for file in onlyfiles:
    print(file)
    file_name = file[:file.index(".")]
    g = input("guy")
    model = bp.get_model(file_name)

    #model.print_name_model_cnf()
"""