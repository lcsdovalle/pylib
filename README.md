# pylib
stack of tools



# MyBigQuery lib

- import: `from google.cloud import bigquery`

### Para inserir no banco

    ```
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
    ```

### Para ler do banco 
```
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

```

### Para atualizar os dados
``` 
    client = bigquery.Client()
    stream = Update(PROJECT_ID).set_client(client).set_table("accessClassroomByUsers").set_dataset(DB)

    data = ['professores = 12'] # defines the SET values to be updated
    where = 'professores = 4' # defines the conditional to update values

    stream.build_query(data = data, where = where)

    r = stream.execute_query()

    print(r)

```
