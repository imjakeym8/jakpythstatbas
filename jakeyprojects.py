import json
from datetime import datetime, timezone, timedelta
from gspread.auth import service_account

class CombotData:
    def __init__(self, combotfile):
        self.combotfile = combotfile
    
    def __format(self):
        with open(self.combotfile) as f:
            data = json.load(f)
        
       
class GsheetEncoder(CombotData):
    def __init__(self):
        super().__init__()
        self.auth = service_account()

    def access_gsheet(self, gsheet_name, gsheet_worksheet):
        self.sh = self.auth.open(gsheet_name)
        self.wks = self.sh.worksheet(gsheet_worksheet)

    def data_range(self, monthbegin, daybegin, duration, monthend=None, dayend=None):
        self.monthbegin = monthbegin
        self.daybegin = daybegin
        if duration % 7 != 0:
            raise ValueError("Invalid duration value.")
        self.duration = duration
        self.monthend = monthend
        self.dayend = dayend    


file = 'tutorials05-gspread/20123-22823.json'
jsoncombot = CombotData(file)
