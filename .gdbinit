python
import sys, os

sys.path.insert(0, "/home/user/work/nlohmann_json_pretty_printer/")
import nlohmann_json_pretty_printer
nlohmann_json_pretty_printer.register_printer_gen(None)
end