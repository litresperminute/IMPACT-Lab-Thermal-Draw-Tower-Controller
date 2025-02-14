from configuration import configuration, configurations

import json

CONFIG_FILE = "configurations.json"

def load_configurations():
    """ Load configuration objects from JSON file """
    configurations = []
    try:
        with open(CONFIG_FILE, "r") as file:
            data = json.load(file)

            for config in data:
                configuration.from_dict(config)

            return data
        
            #return [configuration.from_dict(cfg) for cfg in data]
    except  (FileNotFoundError, json.JSONDecodeError):
        return [] 
    
def save_configurations(configs):
    """ Saves configuration object changes to JSON file """
    with open(CONFIG_FILE, "w") as file:
        json.dump([cfg.to_dict() for cfg in configs], file, indent=4)

def delete_configuration(config):
    """ Deletes configuration object from JSON file """
    for config_object in configurations:
        if config_object.configuration_name == config.configuration_name:
            configurations.remove(config_object)
    save_configurations(configurations)

#def rename_configuration(old_name, new_name):
    #""" Renames configuration object """
    #valid_name = True
    #for config in configurations:
        #if config.configuration_name == new_name:
            #valid_name = False
    
    #if valid_name == False:
        #open_duplicate_warning_window(new_name)

    #for config in configurations:
        #if config.configuration_name == old_name and valid_name == True:
            #config.configuration_name = new_name
