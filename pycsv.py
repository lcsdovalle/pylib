import csv

class PyCsv():
    def __init__(self, file):
        self.file = file+".csv"
    def openfile(self):
        return open(self.file)
    def write_rows(self,rows):
        # Escrever vários dados no csv de uma vez
        # Passar como parâmetro uma lista [['asd'],['asd']]
        with open(self.file,'w',newline='',encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
    def add_row_csv(self,row):
        # Adiciona uma linha ao csv
        # Passar como parâmetro uma lista simples ['s']
        try:
            # row = map(str.strip,row)
            with open(self.file,'a',newline='',encoding="utf-8") as csvfile:        
                writercsv = csv.writer(csvfile)
                writercsv.writerow(row)
            return True
        except NameError:
            return False
    def get_content_as_dictionary(self):
        # A primeira linha se tornará indices para os items do dicionário
        try:
            return csv.DictReader(open(self.file))
        except:
            return False
    def write_one_row(self,row):
        # Escrever uma linha ao csv
        # Passar como parâmetro uma lista simples ['s']
        try:
            with open(self.file,'w',newline='',encoding="utf-8") as csvfile:        
                writercsv = csv.writer(csvfile)
                writercsv.writerow(row)
            return True
        except:
            return False
    def get_content(self):
        # A primeira linha se tornará indices para os items do dicionário
        try:
            return csv.reader(open(self.file,'r',encoding='utf-8'))
        except:
            return False
    def debug(self):
        print("chegando em debug")
        self.read()
