import openpyxl
from openpyxl.styles.borders import Border, Side
from openpyxl.styles import PatternFill

thin_border = Border(left=Side(style='thin'), 
                     right=Side(style='thin'), 
                     top=Side(style='thin'), 
                     bottom=Side(style='thin'))

wb = None

redFill = PatternFill(start_color='EE1111',
                    end_color='EE1111',
                    fill_type='solid')


'''
    Store final result in the excel format.

'''
def generateFinalReport(res_dict):

    try:	
        wb = openpyxl.load_workbook('result.xlsx')
    except Exception:
        raise Exception("Please install openpyxl package!!\nCommand to install the package - (pip install openpyxl)")
    else:
        sheet = wb["Sheet1"]

        row = "C"
        col = 5
        
        for key, val in res_dict.items():
            sheet["%s"%(row+str(col))].border = thin_border
            sheet["%s"%(chr(ord(row)+1)+str(col))].border = thin_border
            sheet["%s"%(chr(ord(row)+2)+str(col))].border = thin_border
            sheet["%s"%(chr(ord(row)+3)+str(col))].border = thin_border
            
            sheet["%s"%(row+str(col))] = key
            sheet["%s"%(chr(ord(row)+1)+str(col))] = "%s"%(", ".join(v for v in val))

            if any( v in ["GPL", "LGPL", "GNU General Public License"] for v in val):
                sheet["%s"%(row+str(col))].fill = redFill
                sheet["%s"%(chr(ord(row)+1)+str(col))].fill = redFill
                sheet["%s"%(chr(ord(row)+2)+str(col))].fill = redFill
                sheet["%s"%(chr(ord(row)+3)+str(col))].fill = redFill
                
            col = col+1
            
        
        wb.save('result.xlsx')
        return True
    
