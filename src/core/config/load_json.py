import json

class LoadJson:
    def __init__(self):
        self.__config: json = self.loadJsonFile("config.json")
        self.__httpHeader: json = self.loadJsonFile("header.json")

    def load_json_file(self, json_file_name: str) -> json: # loads and returns json data
        try:
            with open("configurations/" + json_file_name, "r") as f:
                jsonFile: json = json.load(f)
                return jsonFile
        except FileNotFoundError:
            print(f"<< Error: File 'configurations/{json_file_name}' not found. >>")
            exit()
        except json.JSONDecodeError as e:
            print(f"<< Error: loading JSON configuration from 'configurations/{json_file_name}': {e} >>")
            exit()
            
    def get_config(self) -> json:
        return self.__config
    def get_http_header(self) -> json:
        return self.__httpHeader