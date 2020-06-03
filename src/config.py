import yaml

config_file = open('./data/config.yml', 'r', encoding='utf-8')
config = yaml.safe_load(config_file.read())
config_file.close()
