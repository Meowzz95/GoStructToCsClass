import os
import re
import logging

logging.basicConfig()
_logger = logging.getLogger("GoStructToCsClass")
_logger.setLevel(logging.DEBUG)

NOT_STARTED = 0
STRUCT_LINE = 1
STRUCT_CONTENT = 2
ENDED = 3

class Main:
    def __init__(self, input_path):
        self.state = NOT_STARTED
        self.output=[]
        self.input_path = input_path
        self.class_name = ""

    def process_not_started(self,line):
        if "struct" in line:
            self.state = STRUCT_LINE
            return 0
        return 1

    def process_struct_line(self, line):
        class_name = line.strip().split(" ")[1]
        self.class_name = class_name
        self.output.append(f"public class {class_name}\n")
        self.output.append("{\n")
        self.state = STRUCT_CONTENT
        return 1

    def write_json_annotation(self,json_name):
        self.output.append(f"    [JsonProperty(PropertyName = \"{json_name}\")]\n")
        _logger.debug(f"Writting json annotation -> {self.output[len(self.output) - 1]}")

    def write_property(self,name:str,prop_type:str):
        output_type = prop_type
        if prop_type.startswith("["):
            list_type = re.findall(".*\[\s*\](\w+).*",output_type)
            output_type = f"{list_type[0]}[]"

        self.output.append(f"    public {output_type} {name} {{ get; set; }}\n\n")
        _logger.debug(f"Writting property -> {self.output[len(self.output)-1]}")

    def process_struct_content(self,line):
        if "}" in line:
            self.state = ENDED
            return 0

        propertyNameMatch = re.findall("(\w+).+",line)
        _logger.debug(f"Property {propertyNameMatch[0]} found")

        typeMatch = re.findall("\w+\s+([^\s]+)\s+.*",line)
        _logger.debug(f"Type is {typeMatch[0]}")

        jsonNameMatch = re.findall(".+json:\"(\w+)\".+",line)
        _logger.debug(f"Json name is {jsonNameMatch[0]}")

        self.write_json_annotation(jsonNameMatch[0])
        self.write_property(propertyNameMatch[0],typeMatch[0])

        return 1

    def end(self):
        self.output.append("}\n")
        self.write_file()

    def write_file(self):
        if not os.path.exists("./out"):
            os.mkdir("out")
        with open(f"./out/{self.class_name}.cs","w") as fp:
            fp.writelines(self.output)


    def get_class_name(self,line:str):
        line = line.strip()
        return line.split(" ")[1]

    def start(self):

        with open(self.input_path) as fp:
            lines = fp.readlines()
            index = 0
            while True:
                line = lines[index]
                indexDelta = 1
                if self.state == NOT_STARTED:
                    indexDelta = self.process_not_started(line)
                elif self.state == STRUCT_LINE:
                    indexDelta = self.process_struct_line(line)
                elif self.state == STRUCT_CONTENT:
                    indexDelta = self.process_struct_content(line)
                elif self.state == ENDED:
                    self.end()
                    break

                index += indexDelta





if __name__ == '__main__':
    Main("input.txt").start()

