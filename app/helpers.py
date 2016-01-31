import json

def dict_to_json_file(_dict, path):
    """Converts a dictionary to json and saves it to a file."""
    with open(path, "w") as fp:
         json.dump(_dict, fp, indent=4)

def json_file_to_dict(path):
    """Opens a json file and returns it converted to a dictionary."""
    with open(path, "r") as fp:
        return json.load(fp)

def convert_to_64_bit(number):
    """Takes a 32-bit number and returns it as a 64-bit number."""
    return number + 76561197960265728

def convert_to_32_bit(number):
    """Takes a 64 bit number and returns it as a 32-bit number."""
    return number - 76561197960265728
