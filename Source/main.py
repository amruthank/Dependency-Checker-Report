import sys, json
from extract_license_urls import *
from text_processing import getLicenseNames
from report_generate import generateFinalReport
import time
import multiprocessing

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
            try:
                with open(self.file) as f: #Open and load a file.
                    data = json.load(f)
            except json.JSONDecodeError:
                    raise Exception("Error in the json file.")
                    
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
    

    #Query "license of component" to extract first three url's!
    def fetch_license_url_from_internet(self): #TODO: Speedup the process.

        #Function to extract license URL's.
        automation = SeleniumDriver()
        start_time1 = time.time()
        for key, val in (self.dependency_dic).items():
            component_urls_dict["%s"%key]= automation.get_urls(key)["%s"%key]
        end_time1 = time.time()
        #print(f'\nTotal execution time with headerless browser: {end_time1-start_time1:.2f}s\n')
        print("Total execution time with headerless browser: %s"%(end_time1-start_time1))
        automation.close_browser()

        #Function to extract license names from top 3 URL's.
        start_time2 = time.time()
        pool = multiprocessing.Pool()
        pool_res = pool.map(getLicenseNames, list(component_urls_dict.values()))
        end_time2 = time.time()
        #print(f'\nTotal execution time with parallel programming: {end_time2-start_time2:.2f}s\n')

        for id, key in enumerate(self.dependency_dic):
            result_dictionary["%s"%key] = pool_res[id]
           
        self.generate_report(result_dictionary)

    #Finalize the license names for the component.
    def extract_component_licenses(self, oss_name, license_list):    
        result_dictionary["%s"%oss_name] = []
        result_dictionary["%s"%oss_name] = getLicenseNames(license_list)

    #Final report generation.
    def generate_report(self, res):
        print(json.dumps(res, indent = 4))
        generateFinalReport(res, result_type = "graph")
        
def file_parser(file_name):
    file1 = File(file_name)
    
#if __name__ == "__main__":
#    file_parser()






##################################################################FRONT END##################################################################################

'''try:
    from Tkinter import *
except ImportError:
'''

from tkinter import *
    
from tkinter import messagebox


try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1
from tkinter import filedialog


#import billing_GUI_support


Ftype=[('Excel (*.xls*)', '*.xl*'),('Any File (*.*)', '*')]
#Beginning of Open source License Text Generation GUI function!
def olt_gui(): 
    root = Tk()
    
    #root.iconbitmap('oslt.ico')
    top = open_source_License_ui(root)
                    
    root.mainloop()
#End of olt_gui finction.



'''
you can change any thing from here, Please Be Adviced, with great power comes great responsibility.
Only change if you know what you are doing responsibly
'''

class open_source_License_ui:

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.top = top
        self.upload_file_path = ""

        top.geometry("300x250+500+200")
        top.title("Dependenct Checker Tool")
        top.configure(background="#0c9ee2") #0c9ee2
        top.configure(highlightbackground="#0c9ee2")
        top.configure(highlightcolor="black")

        self.var = StringVar()
    
        self.browse = Button(top)
        self.browse.place(relx=0.80, rely=0.09, height=26, width=55)
        self.browse.configure(activebackground="#0a83bb")
        self.browse.configure(activeforeground="#000000")
        self.browse.configure(background="#0a83bb")
        self.browse.configure(command=self.Browse_file)
        self.browse.configure(disabledforeground="#a3a3a3")
        self.browse.configure(foreground="#000000")
        self.browse.configure(highlightbackground="#0a83bb")
        self.browse.configure(highlightcolor="black")
        self.browse.configure(pady="0")
        self.browse.configure(text='''Browse''')


        self.entry_field = Entry(top)
        self.entry_field.place(relx=0.03, rely=0.07, relheight=0.12, relwidth=0.75)
        self.entry_field.configure(background="white")
        self.entry_field.configure(disabledforeground="#a3a3a3")
        self.entry_field.configure(font="TkFixedFont")
        self.entry_field.configure(foreground="#000000")
        self.entry_field.configure(highlightbackground="#0c9ee2")
        self.entry_field.configure(highlightcolor="black")
        self.entry_field.configure(insertbackground="black")
        self.entry_field.configure(selectbackground="#c4c4c4")
        self.entry_field.configure(selectforeground="black")


        self.Label1 = Label(top)
        self.Label1.place(relx=0.03, rely=0.02, height=22, width=544)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(anchor=W)
        self.Label1.configure(background="#0c9ee2")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#0c9ee2")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Upload *.json file:''')
        

        self.Compile_button = Button(top)
        self.Compile_button.place(relx=0.35, rely=0.65, height=40, width=80)
        self.Compile_button.configure(activebackground="#0a83bb") #0c9ee2
        self.Compile_button.configure(activeforeground="#000000")
        self.Compile_button.configure(background="#0a83bb")
        self.Compile_button.configure(disabledforeground="#a3a3a3")
        self.Compile_button.configure(foreground="#000000")
        self.Compile_button.configure(highlightbackground="#0a83bb")
        self.Compile_button.configure(highlightcolor="black")
        self.Compile_button.configure(pady="0")
        self.Compile_button.configure(text='''Run''')
        self.Compile_button.configure(command=self.Run)


    def Browse_file(self):
        self.upload_file_path = filedialog.askopenfilename(filetypes= Ftype)
        try:
            self.entry_field.insert("end",(self.upload_file_path).split("/")[-1])
        except Exception:
            self.entry_field.insert("end",self.upload_file_path)
        
    
    def Run(self):

        if self.entry_field.get() == "":
            messagebox.showwarning("Warining", "Please upload the *.json file!", size = 0.5)
        else:
            try:
                file_parser(self.entry_field.get())

            except Exception:
                raise("Error!! Parsing the file")
    

if __name__ == '__main__':
    olt_gui()


##################################################################END OF FRONT END###########################################################################
