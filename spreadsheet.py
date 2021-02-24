from pylib.auth import authService
from pylib.auth2 import clientAuth

class gSheet(clientAuth):
    def __init__(self,creds,id=False):
        self.scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/spreadsheets',
        ]
        super().__init__(f"{creds}.json",self.scopes)
        self.id= id
        self.service = super().getService('sheets','v4')
        self.data = ''
        self.values = []
    def setSpreadsheetId(self,id):
        self.id = id
    def addScope(self,scope):
        self.scopes.append(scope)
    def getData(self,sheet):
        if self.id:
            try:
                print('Abrindo planilha')
                self.data = self.service.spreadsheets().values().get(spreadsheetId=self.id,range=sheet).execute()
                return self.data.get('values')
            except Exception as error:
                return str(error)
        else:
            return "Informe o id primeiro"

    def setValue(self,row):
        self.values.append(row)


    def pushData(self,sheet):
        body= {'values':self.values}
        result = self.service.spreadsheets().values().update(
        spreadsheetId=self.id, 
        range=sheet,
        valueInputOption='RAW', 
        body=body).execute()
        return result['updatedCells']

    def appendRows(self,sheet,row):
        values = []
        values.append(row)
        body=   {
            "values":values,
            }
            
        result = self.service.spreadsheets().values().append(spreadsheetId=self.id, 
        range=sheet, 
        valueInputOption='RAW', 
        insertDataOption='INSERT_ROWS', 
        body=body).execute()

        return result['updates']['updatedRows']