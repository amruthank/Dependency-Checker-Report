import sys, json
from extract_license_urls import web_init
from text_processing import getLicenseNames
from report_generate import generateFinalReport
import logging

logging.basicConfig(level = logging.DEBUG)

component_urls_dict = {}
result_dictionary = {}


class File:

    def __init__(self, file):
        self.file = file
        self.valid_files = ["json"] #List of valid file types
        self.file_name, self.file_type = self.fetch_file_name_and_type()
        self.dependency_dic = {}
        
        if self.is_valid_file():
            self.file_parser()
        else:
            raise Exception("Invalid file!")

    def fetch_file_name_and_type(self): #Take care of file type.
        return ((self.file).rsplit(".", 1))

    def is_valid_file(self):
        return ((self.file_type) in self.valid_files)

    def file_parser(self):

        if self.file_type == "json":
            with open(self.file) as f: #Open and load a file.
                data = json.load(f)
                
            for line in data: #Create result dictionary.
                if line.startswith("depen"):
                    for key, val in data[line].items():
                        if len(val)>1 and "version" in val: #If nested dependencies are found
                            self.dependency_dic["%s"%key] = val["version"]
                        elif val:
                            self.dependency_dic["%s"%key] = val
                        else:
                            self.dependency_dic["%s"%key] = "None"

        print(json.dumps(self.dependency_dic, indent = 4))
        return self.fetch_license_url_from_internet()
    

    #Query "license of component" to fetch url's.
    def fetch_license_url_from_internet(self):

        for key, val in (self.dependency_dic).items():
            component_urls_dict["%s"%key]= web_init(key)
            self.extract_component_licenses(key, component_urls_dict["%s"%key])

        
        self.generate_report(result_dictionary)

    #Finalize the license names for the component.
    def extract_component_licenses(self, oss_name, url_list):
        
        result_dictionary["%s"%oss_name] = []
        result_dictionary["%s"%oss_name] = getLicenseNames(url_list)


    #Final report generation.
    def generate_report(self, res):
        generateFinalReport(res)
        
def file_parser():
    file1 = File(input())
    
if __name__ == "__main__":
    file_parser()
