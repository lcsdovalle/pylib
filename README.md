# pylib
stack of tools

# Mongo lib

# Dependências 
    pip install virtualenv

    virtualenv venv

    pip install --upgrade google-api-core google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib google-cloud-core

### Para criar uma coleção e adicionar um documento logo em seguida.

    
        from pylib.mongo import MongoDrive
        mongo = MongoDrive(string_conexao=config.string_conexao,db='dashboard')
        mongo.criarColecao("Funcionario")
        mongo.inserirUmRegistro({"Nome":"Lucas Thomas"})
        print(mongo.ultimoRegistro)
    
### Cria vários registros em uma coleção pre existente
    
        from pylib.mongo import MongoDrive
        mongo = MongoDrive(string_conexao=config.string_conexao,db='dashboard')
        mongo.usarColecao("Funcionarios")
        mongo.inserirVariosRegistros([{"Nome":"Lucas Thomas"},{"Nome":"Ennio Sousa"}])
        print(mongo.ultimoRegistro.inserted_ids)
    

### Busca todos os dados de uma coleção
    
        from pylib.mongo import MongoDrive
        mongo = MongoDrive(string_conexao=config.string_conexao,db='dashboard')
        mongo.usarColecao("dashboard")
        mongo.buscarTudo()
        for i in mongo.ultimosRegistros:
            print(i.get("Nome))
        print(mongo.ultimoRegistro.inserted_ids)
    

### Busca  alguns dados da coleção
    
        from pylib.mongo import MongoDrive
        mongo = MongoDrive(string_conexao=config.string_conexao,db='dashboard')
        mongo.usarColecao("dashboard")
        mongo.buscarPor(params={"_id":0,"Nome":1})
        for i in mongo.ultimosRegistros:
            print(i.get("Nome"))
        print(mongo.ultimoRegistro.inserted_ids)
    


# MyBigQuery lib

- import: `from google.cloud import bigquery`

### Para inserir no banco

    
        from flask.pylib.MyBigQuery import Stream
        linhas = [
            {"data":"2021-01-01","professores":4,"alunos":10}
        ]

        stream = Stream(PROJECT_ID)
        stream.set_client(bigquery.Client())
        stream.set_dataset("chromedash")
        stream.set_table("accessClassroomByUsers")

        stream.inserir(linhas)
        if not stream.errors:
            "Inserido com sucesso"
        else:
            print(stream.errors)
    

### Para ler do banco 

    client = bigquery.Client()
    stream = Reader(PROJECT_ID).set_client(client).set_table("chrome_atividade").set_dataset(DB)

    # what para substituir o *
    # condicional
    # group_by como retornar
    stream.build_query(where="data is not null", group_by="GROUP BY registro_uso, data")

    query_job = stream.execute_query()  # Make an API request.

    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print(row)
        print("name={}, count={}".format(row[1], len(row)))



### Para atualizar os dados
 
    client = bigquery.Client()
    stream = Update(PROJECT_ID).set_client(client).set_table("accessClassroomByUsers").set_dataset(DB)

    data = ['professores = 12'] # defines the SET values to be updated
    where = 'professores = 4' # defines the conditional to update values

    stream.build_query(data = data, where = where)

    r = stream.execute_query()

    print(r)



### Para executar uma query aleatóriamente

client = bigquery.Client()
stream = Update(PROJECT_ID).set_client(client).set_table("accessClassroomByUsers").set_dataset(DB)

stream.set_sql("TRUNCATE {}".format(stream.get_tableid() ) )
stream.execute_query()



# Mailing 
**Adiciona recurso para o envio de e-mails NO DJANGO**

# Implantação
- Adicionar ao arquivo settings.py as variáveis:
    
        MAILING_ENDPOINT = ''
        MAILING_JSON = BASE_DIR / 'core/files/mailing.json'
        MAILING_FROM = 'no-reply@domain.com'
    
    - MAILING_ENDPOINT: webservice que recebe o payload para o envio do email. Exemplo:https://gitlab.com/-/snippets/2076852
    - MAILING_JSON: caminho para o arquivo do projeto em cloud, vale ressaltar que neste caso utilizar conta de serviço
    - MAILING_FROM: conta que será impersonada para enviar os e-mails

### Exemplo de uso
    
        from pylib.mailing import Email
        mail = Email()
        mail.setAssunto("TESTANDO MAILING")
        mail.addRementente("")
        mail.addRementente("")
        mail.setMensagem('core/confirmacao.html')
        mail.enviarGmail()
    
