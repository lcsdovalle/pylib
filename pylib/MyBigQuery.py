

class Stream():
    def __init__(self,project_id):
        self.project_id = project_id
        self.dataset = False
        self.table = False
        self.errors = False
        
    def set_dataset(self,dataset):
        self.dataset =  dataset or False
        return self

    def set_table(self,table):
        self.table =  table or False
        return self

    def set_client(self,client):
        self.client =  client or False
        return self
        
    def get_tableid(self):
        return "{}.{}.{}".format(
            self.project_id,
            self.dataset,
            self.table
        )
    def inserir(self,rows):
        self.errors = self.client.insert_rows_json(
            self.get_tableid(),
            rows
        )
        if self.errors == []:
            self.errors = False
        else:
            return self.errors
    def execute_query(self):
        return self.client.query(self.sql)

class Reader(Stream):
    def __init__(self,PROJECT_ID):
        super().__init__(PROJECT_ID)
        self.sql = ""

    def build_query(self,**kwargs):
        """ Build sql instruction """
    ## where, what
    ## what is * by default
    ## grouped_by = 'data,chromebooks' defines the result's order
        what = kwargs.get("what","*")
        group_by = kwargs.get("group_by",'')
        where = kwargs.get("where",'')
        self.sql = "SELECT {} FROM {} WHERE {} {} ".format(
            what,
            self.get_tableid(),
            where,
            group_by
        )


class Update(Stream):
    def __init__(self,PROJECT_ID):
        super().__init__(PROJECT_ID)

    def build_query(self,**kwargs):
        data = kwargs.get("data",'')
        where = kwargs.get("where","true")
        self.sql = "UPDATE {} SET {} WHERE {}".format(
            self.get_tableid(),
            ",".join(data),
            where
        )
    