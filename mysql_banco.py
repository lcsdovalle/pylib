import pymysql
class banco():
    def __init__(self,host,user,passwd,db,porta=None):
        if porta is None:
            porta = 3306
        self.host = host
        self.user = user
        self.pssd = passwd
        self.db = db
        self.conexao =   self.conectar(porta)
        self.table = ""
        self.campos = None
        self.valores = None
        self.query =  None  
        self.result = None
    def tabela(self,tabela):
        self.table = tabela
        return self
    
    def inserir(self,param):
        self.query = ""
        c = []
        v = []
        for campo in param:
            c.append(campo)
            if type(param[campo]) == int:
                v.append("{}".format(param[campo]))
            else:
                v.append("'{}'".format(param[campo]))
        self.query = "INSERT INTO {}({}) values ({})".format(
            self.table,
            ",".join(c),
            ",".join(v)
            )        
        # print(self.query)
        return self
    def conectar(self,porta):
        return pymysql.connect(
            host = self.host,
            user = self.user,
            passwd = self.pssd,
            database= self.db,
            port=porta
        )   
    def autalizar(self,condicao,param):
        self.query = ""
        params =[]
        for campo in param:
            if type(param[campo]) == str:
                params.append(
                    "{} = '{}'".format(campo,param[campo])
                )
            elif type(param[campo]) == int:
                params.append(
                    "{} = {}".format(campo,param[campo])
                )
        if len(params) ==1:
            pass
        self.query = "UPDATE {} SET {} WHERE {}".format(
            self.table,
            ",".join(params),
            condicao
            )
        
    def executar(self):
        try:
            self.conexao.cursor().execute(self.query)
            self.result = self.conexao.commit()
        except Exception as e :
            print(e)
            self.conexao.rollback()
            return False
