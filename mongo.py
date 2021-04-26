import pymongo
import config
client = pymongo.MongoClient(config.string_conexao)


class MongoDrive():
    def __init__(self,string_conexao, db):

        # inicia o client
        self.client = pymongo.MongoClient(string_conexao) or False

        # incia o banco
        self.db = self.client[db] or self.client['teste']

        # colecão atual
        self.colecaoAtual = None

        # Último registro inserido
        self.ultimosRegistros = None
    
    def usarColecao(self,nome_colecao):
        self.colecaoAtual = self.db[nome_colecao]
        return self

    def criarColecao(self,nome_colecao=False):
        try:
            self.colecaoAtual = self.db[nome_colecao]
            return self
        except Exception as e:
            raise Exception(e)

    def inserirUmRegistro(self,registro):
        try:
            self.ultimosRegistros = self.colecaoAtual.insert_one(registro)
            return self
        except Exception as e:
            raise Exception(e)

    def inserirVariosRegistros(self,lista_com_dicionario):
        try:
            self.ultimosRegistros = self.colecaoAtual.insert_many(lista_com_dicionario)
            return self
        except Exception as e:
            raise Exception(e)

    def buscarPrimeiro(self):
        try:
            self.ultimosRegistros = self.colecaoAtual.find_one()
            return self
        except Exception as e:
            raise Exception(e)
    
    def buscarTudo(self):
        try:
            self.ultimosRegistros = self.colecaoAtual.find()
            return self
        except Exception as e:
            raise Exception(e)
    def buscarPor(self, params = dict):
        try:
            self.ultimosRegistros = self.colecaoAtual.find({},params)
            return self
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':
    pass
    # try:
    #     mongo = MongoDrive(string_conexao=config.string_conexao,db='dashboard')
    #     mongo.usarColecao("dashboard")
    #     mongo.buscarPor(params={"_id":0,"Nome":1})
    #     for i in mongo.ultimosRegistros:
    #         print(i.get("Nome"))
    # except Exception as e:
    #     print(e)