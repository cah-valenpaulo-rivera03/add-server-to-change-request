import configparser

def set_config(section, key, value):
    config = configparser.ConfigParser()

    config.add_section(section)
    config.set(section, key, value)
    
    with open(r"assets\config", 'w') as configfile:
        config.write(configfile)

def get_config(section, key):
    config = configparser.ConfigParser()
    config.read(r"assets\config")

    return config[section][key]