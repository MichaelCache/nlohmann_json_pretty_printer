import gdb
import re

nlohmann_json_type_regex = re.compile(r"nlohmann::.*?basic_json<.*")

def register_printer_gen(obj=None):
    gdb.printing.register_pretty_printer(obj, NlohmannJsonPrinterGen())

class NlohmannJsonPrinterGen(gdb.printing.PrettyPrinter):
    def __init__(self):
        super().__init__('nlohmann_json_pretty_printer')
        self.enabled = True
        
    def __call__(self, val):
        t = gdb.types.get_basic_type(val.type)
        if re.match(nlohmann_json_type_regex, str(t)):
            json_type = str(val["m_data"]['m_type'])
            if json_type.endswith("object") or json_type.endswith("array"):
                return NlohmannJsonConainerPrinter(val)
            elif json_type.endswith("string") or json_type.endswith("boolean") or \
                json_type.endswith("number_integer") or \
                json_type.endswith("number_unsigned") or \
                json_type.endswith("number_float") or \
                json_type.endswith("number") or json_type.endswith("null"):
                return NlohmannJsonPrinter(val)
            else:
                return None
        else:
            return None 
    

class NlohmannJsonConainerPrinter:
    def __init__(self, value):
        self.value = value
        self.json_type = str(value["m_data"]['m_type'])

    def to_string(self):
        if self.json_type.endswith("object"):
            return "object"
        elif self.json_type.endswith("array"):
            return "array"
        else:
            return "not supported json type:{}".format(self.json_type)
    
    def children(self):
        if self.json_type.endswith("object"):
            js_map = self.value["m_data"]["m_value"]["object"].dereference()
            map_printer = gdb.default_visualizer(js_map)
            map_children = map_printer.children()
            return map_children
        elif self.json_type.endswith("array"):
            js_array = self.value["m_data"]["m_value"]["array"].dereference()
            array_printer = gdb.default_visualizer(js_array)
            array_children = array_printer.children()
            return array_children
        else:
            return ()
        
class NlohmannJsonPrinter:
    def __init__(self, value):
        self.value = value
        self.json_type = str(value["m_data"]['m_type'])

    def to_string(self):
        if self.json_type.endswith("null"):
            return "null"
        elif self.json_type.endswith("string"):
            return self.value["m_data"]["m_value"]["string"].dereference()
        elif self.json_type.endswith("boolean"):
            return self.value["m_data"]["m_value"]["boolean"]
        elif self.json_type.endswith("number_integer"):
            return self.value["m_data"]["m_value"]["number_integer"]
        elif self.json_type.endswith("number_unsigned"):
            return self.value["m_data"]["m_value"]["number_unsigned"]
        elif self.json_type.endswith("number_float"):
            return self.value["m_data"]["m_value"]["number_float"]
        else:
            print(self.json_type)
            return "not supported json type:{}".format(self.json_type)
    
                  