from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import googleapiclient.discovery
import json


class User():
    def __init__(self,service):
        self.service = service
        self.ou = False
        self.user =  False
        self.todos_usuarios = {}
    
    def gravar(self, usuarios):
        if usuarios:
            todos = {}
            for u in usuarios:
                todos[u.get('primaryEmail')] = u
            json.dump(todos,open('../project/db_gsuite.json','w',encoding="utf-8"))
            
    def carregar_todos_usuarios(self):
        
        total = 0
        iniciado = False
        pagetoken = True
        usuarios = []
        while pagetoken is not None:
            try:
                if not iniciado:
                    r = self.service.users().list(customer="my_customer").execute()
                    pagetoken = r.get("nextPageToken",None)
                    iniciado = True
                    usuarios += r.get('users',[]) 
                    total += len(r.get('users',[]))
                else:
                    r = self.service.users().list(customer="my_customer",pageToken=pagetoken,maxResults=500).execute()
                    pagetoken = r.get("nextPageToken",None)
                    usuarios += r.get('users',[])
                    total += len(r.get('users',[]))
                if not pagetoken or pagetoken is None or 'users' not in r:
                    break
                print(total, 'usuários encontrados')
            except:
                pass
        self.gravar(usuarios) 
        # return json.load(open("db_gsuite.json",'r',encoding="utf-8"))

        
    def carregar_usuario(self,user_email):
        try:
            r = json.load(open("../project/db_gsuite.json",'r',encoding="utf-8"))
            self.user = r[user_email]
            return self
        except Exception as e:
            return False

    def ler_ou(self):
        if not self.user:
            return False
        return self.user['orgUnitPath']
    
    def ler_inep(self):
        if not self.user:
            return "000000"
        if 'aluno' in self.user['primaryEmail']:
            if "organizations" not in self.user:
                return "000000"
            
            if 'department' not in self.user['organizations'][0]:
                return "000000"
            
            return self.user.get("organizations")[0].get('department')
        

        r = self.user['customSchemas'] if 'customSchemas' in self.user else False
        if r:
            r = r.get('Escolas',False)
            if r:
                r =  r.get('INEP',False)
                if r:
                    return r

        return "000000"
class ChromeBooks():
    def __init__(self,service):
        self.service = service or False
        self.pagetoken = None

    def execute_query(self,**kwargs):
        if self.pagetoken is not None:
            return self.service.chromeosdevices().list(
                customerId="my_customer",
                maxResults=1000,
                pageToken=self.pagetoken
            ).execute()
        else:
            return self.service.chromeosdevices().list(
                customerId="my_customer",
                maxResults=1000
            ).execute()
    def carregar_todos_chromebooks(self):
        r = self.execute_query()
        self.pagetoken = r.get('nextPageToken',None)
        chromes = []
        chromes += r.get('chromeosdevices',False)
        while self.pagetoken is not None:
            r = self.execute_query()
            self.pagetoken = r.get('nextPageToken',None)
            chromes += r.get('chromeosdevices',False)
        return chromes



        


#https://github.com/googleapis/google-api-python-client/blob/master/samples/service_account/tasks.py
class authService():
    def __init__(self,scopes,jsonfile,email=None):
            self.userEmail = email
            self.SERVICE_ACCOUNT_FILE = jsonfile
            self.SCOPES = scopes
    def getService(self,*args,**kwargs):
            credentials = service_account.Credentials.from_service_account_file(
                    self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)
            if self.userEmail is not None:                
                delegated_credentials = credentials.with_subject(self.userEmail)
                credentials = delegated_credentials

            return googleapiclient.discovery.build(args[0], args[1], credentials=credentials)
    def setScope(self,scopes):
            pass        

# auth = authService('jsons/credential.json','lucas@gsaladeaula.com.br').getService('admin','directory_v1')
# users = auth.users().list(customer="my_customer").execute()
# print(users)
class clientAuth():

    def __init__(self,creds,scopes):
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = scopes
        # print(SCOPES)
        self.service = None
        self.creds = creds
        

    def getService(self,*args):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.creds, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build(args[0], args[1], credentials=creds)
        return self.service  
              
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

class TurmaClassroom():

    def __init__(self,turma_id_gsuite,json_file,pessoa):
        self.turma_pronta = None        
        self.turma_id = turma_id_gsuite
        self.json = json_file
        self.turma_gsuite =""
        self.atividades = ""
        self.escopos = [
            'https://www.googleapis.com/auth/classroom.courses',
            'https://www.googleapis.com/auth/classroom.profile.emails',
            'https://www.googleapis.com/auth/classroom.profile.photos',
            'https://www.googleapis.com/auth/classroom.rosters',
            'https://www.googleapis.com/auth/classroom.coursework.me',
            'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
            'https://www.googleapis.com/auth/classroom.coursework.students',
            'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
            'https://www.googleapis.com/auth/classroom.topics',
            'https://www.googleapis.com/auth/classroom.topics.readonly',
            # 'https://www.googleapis.com/auth/drive',
            # 'https://www.googleapis.com/auth/drive.appdata',
            # 'https://www.googleapis.com/auth/drive.file',
            # 'https://www.googleapis.com/auth/drive.metadata',
            # 'https://www.googleapis.com/auth/drive.metadata.readonly',
            # 'https://www.googleapis.com/auth/drive.photos.readonly',
            # 'https://www.googleapis.com/auth/drive.readonly',
            # 'https://www.googleapis.com/auth/drive.scripts',
            'https://www.googleapis.com/auth/classroom.announcements',
            'https://www.googleapis.com/auth/classroom.announcements.readonly',

        ]
        self.service = authService(self.escopos,self.json,pessoa).getService('classroom','v1')        
        self.name = ""
        self.section = ""
        self.description = ""
        self.descriptionHeading = ""
        self.ownerId = ""
        self.creationTime = ""
        self.updateTime = ""
        self.enrollmentCode = ""
        self.courseState = ""
        self.alternateLink = ""
        self.teacherGroupEmail = ""
        self.courseGroupEmail = ""
        self.teacherFolder = []
        self.courseMaterialSets = []
        self.guardiansEnabled = ""
        self.avisos = ""

    def carregar_turma(self,turma_pronta=None):
        try:
            print('Carregando turma....')
            if turma_pronta is None:
                self.turma_gsuite = self.service.courses().get(id=self.turma_id).execute()                    
            else:
                self.turma_gsuite = turma_pronta
            self.name = self.turma_gsuite.get('name')
            self.section = self.turma_gsuite.get('section')
            self.description = self.turma_gsuite.get('description')
            self.descriptionHeading = self.turma_gsuite.get('descriptionHeading')
            self.ownerId = self.turma_gsuite.get('ownerId')
            self.creationTime = self.turma_gsuite.get('creationTime')
            self.updateTime = self.turma_gsuite.get('updateTime')
            self.enrollmentCode = self.turma_gsuite.get('enrollmentCode')
            self.courseState = self.turma_gsuite.get('courseState')
            self.alternateLink = self.turma_gsuite.get('alternateLink')
            self.teacherGroupEmail = self.turma_gsuite.get('teacherGroupEmail')
            self.courseGroupEmail = self.turma_gsuite.get('courseGroupEmail')
            self.teacherFolder = self.turma_gsuite.get('teacherFolder')
            self.courseMaterialSets = self.turma_gsuite.get('courseMaterialSets')
            self.guardiansEnabled = self.turma_gsuite.get('guardiansEnabled')
            
            return self
        except Exception as e:
            print(e)

    def carregar_atividades(self):
        """ CARREGA AS ATIVIDADES DA TURMA CONSIDERANDO QUE TEM MENOS DE 30"""
        if self.turma_id:
            act = self.service.courses().courseWork().list(courseId=self.turma_id).execute()
            if act.get('courseWork') is not None:
                self.atividades= act.get('courseWork')


    def filtrar(self,criterio):     
        """ INFORME O NOME DO TÓPICO PARA TER ATIVIDADES PROCESSADAS"""   
        # TODO: ATIVIDADE SÓ CARREGA 30, COLOCAR PARA CARREGAR TUDO 
        atividades = []
        for atv  in self.atividades:
            topico = self.service.courses().topics().get(courseId=self.turma_id,id=atv.get('topicId')).execute()            
            if criterio not in topico.get('name').lower():
                atividades.append(atv)
        self.atividades = atividades

        
    def carregar_avisos_mural(self):
        """ CARREGA OS AVISOS DO MURAL"""
        if self.turma_id:
            ann = self.service.courses().announcements().list(courseId=self.turma_id).execute()
            self.avisos= ann.get('announcements',None)            
                

    def copiar_avisos_mural(self,id_turma, professor_email,logger=None):
        #TODO: Copiar avisos do mural para a outra turma
        if not self.avisos:
            return False
        else:
            servico_temporario = self.inpersona_professor(professor_email) #* INICIA O SERVIÇO IMPERSONADO COMO A ESCOLA
            if servico_temporario: #* SE DEU CERTO CONTINUA
                for att in self.avisos:
                    # novo_aviso["courseId"]= a.get('courseId'),
                    # novo_aviso["id"]= a.get(),
                    
                    novo_aviso = {}
                    novo_aviso['text']= att['text']
                    novo_aviso['state']= att.get("state")
                    novo_aviso['assigneeMode']= att.get('assigneeMode')
                    novo_aviso['individualStudentsOptions'] = att.get('individualStudentsOptions')
                    if "materials" in att: #* SE A ATIVIDADE TEM MATERIAIS
                        materiais = self.preparar_materiais(att.get('materials'))
                        novo_aviso['materials'] = materiais
                    """ CRIA A CÓPIA """
                    try:
                        servico_temporario.courses().announcements().create(
                            courseId=id_turma,
                            body=novo_aviso
                        ).execute()
                        if logger is not None:
                            logger.add_row_csv([
                                "Sucesso ao postar aviso",
                                self.turma_id, # id turma origem
                                self.name, # nome turma origem
                                novo_aviso.get('id'), #id atividade origem
                                novo_aviso.get('name'), # nome atividade
                                id_turma  #id turma destino   
                            ])
                    except Exception as e:
                        if logger is not None:
                            logger.add_row_csv([
                                "Falha ao postar aviso: {}".format(str(e)),
                                self.turma_id, # id turma origem
                                self.name, # nome turma origem
                                novo_aviso.get('id'), #id atividade origem
                                novo_aviso.get('name'), # nome atividade
                                id_turma  #id turma destino   
                            ])
                        else:
                            print(f"Erro: ")   
    def nao_existe(self,turma_id,professor_email,fonte):
        try:
            for atv in self.atividades:
                if 'Avaliação diagnóstica' in atv.get('title'):
                    return False
            return True
        except:
            return True                
    def copiar_atividades_para_turma(self,id_turma, professor_email,logger):
        """ Copia as atividades de uma turma para outra """
        # id_turma que receberá as atividades
        # professor_email dono da turma que receberá a atividade        
        servico_temporario = self.inpersona_professor(professor_email) #* INICIA O SERVIÇO IMPERSONADO COMO A ESCOLA
        if servico_temporario: #* SE DEU CERTO CONTINUA
            # self.atividades[0].pop(0)
            for atividade in self.atividades:
                nova_atividade = {}
                nova_atividade['id'] = atividade.get('id')
                nova_atividade['title'] = atividade.get('title')
                nova_atividade['state'] = atividade.get('state')
                nova_atividade['maxPoints'] = 0            
                nova_atividade['submissionModificationMode'] = atividade.get('MODIFIABLE_UNTIL_TURNED_IN')            
                nova_atividade['assigneeMode'] =  "ALL_STUDENTS"
                nova_atividade['workType'] = atividade.get('workType')
                # nova_atividade['scheduledTime'] = "2020-07-15T17:00:00.045123456Z"
                nova_atividade['dueDate'] = atividade.get('dueDate')
                nova_atividade['dueTime'] = atividade.get('dueTime')
                # nova_atividade['SubmissionModificationMode'] = 'MODIFIABLE_UNTIL_TURNED_IN'
                if 'maxPoints' in atividade:
                    nova_atividade['maxPoints'] = atividade.get('maxPoints')
                if 'description' in atividade:
                    nova_atividade['description'] = atividade.get('description')
                if 'topicId' in atividade:
                    nova_atividade['topicId'] = self.cria_topico_se_nao_existe(
                        servico_temporario,
                        id_turma,
                        self.obter_topico_nome(atividade.get('topicId'))
                    )
                if "materials" in atividade: #* SE A ATIVIDADE TEM MATERIAIS
                    materiais = self.preparar_materiais(atividade.get('materials'))
                    nova_atividade['materials'] = materiais
                self.copiar_atividade(id_turma, servico_temporario,nova_atividade,logger)

    def obter_topico_nome(self,topico_id):
        """ OBTER O NOME DO TÓPICO ANTIGO """
        topico = self.service.courses().topics().get(courseId=self.turma_id,id=topico_id).execute()
        return topico.get('name')

    def inpersona_professor(self,email_prof):
        """ INICIA O SERVIÇO COM O EMAIL DA ESCOLA"""
        try:
            return authService(self.escopos,self.json,email_prof).getService('classroom','v1')        
        except:
            return False

    def cria_topico_se_nao_existe(self,servico_temporario,turma_temporaria_id,topico_nome):
        try:
            nome = topico_nome
            ok = self.topico_ja_existe(servico_temporario,turma_temporaria_id,topico_nome) # verifica se já tem tópico
            if ok.get('pode_criar'): # se não existir ainda, então cria
                novo_topico = servico_temporario.courses().topics().create(
                    courseId=turma_temporaria_id,
                    body={"name":topico_nome}
                ).execute()
                return novo_topico.get('topicId')
            else: #se ja existir, retorna o id já existente com o mesmo nome
                return ok.get('topico_ja_existe_id')
        except Exception as e:
            print(str(e))
            return False
    def topico_ja_existe(self,servico_temporario,turma_temporaria_id,topico_nome):

        r = {}
        r['pode_criar'] = True    
        ja_existe = servico_temporario.courses().topics().list(
            courseId=turma_temporaria_id            
        ).execute()
        if ja_existe.get('topic') is not None:
            for t in ja_existe.get('topic'):
                if topico_nome == t.get('name'):
                    r['pode_criar'] = False
                    r['topico_ja_existe_id'] = t.get('topicId')
                    return r

        return r

    def preparar_materiais(self,materiais):
        """ TRANSFORMA OS MATERIAIS EM LINKS """
        # print(materiais)
        if materiais is None:
            return None
        i = 0 
        materiais_filtrados = []
        for material in materiais:            
            if 'form' in material:
                dicionario = {}
                form_url = material.get('form').get('formUrl')
                title = material.get('form').get('title')
                dicionario['link'] = {'url':form_url,'title':title}                
                materiais_filtrados.append(dicionario)
            elif 'driveFile' in material:
                dicionario = {}
                a_url = material.get('driveFile').get('driveFile').get('alternateLink')
                a_title = material.get('driveFile').get('driveFile').get('title')
                dicionario['link'] = {'url':a_url,'title':a_title}                
                materiais_filtrados.append(dicionario)
            else:
                materiais_filtrados.append(material)       
            i+=1
        return materiais_filtrados

    def criar_nova_turma(self,body):
        pass

    def deletar_atividades(self,turma_id,professor_email,criterios):
        servico_temporario = self.inpersona_professor(professor_email) #* INICIA O SERVIÇO IMPERSONADO COMO A ESCOLA

        if servico_temporario: #* SE DEU CERTO CONTINUA
            criterios_map_turmas = ['1ª','2ª','3ª','4ª','5ª']
            criterios_map_nivel = ['EF','EJA']

            try:
                turma = servico_temporario.courses().get(id=turma_id).execute()
            except Exception as e:
                print(e)
                return False
            
            if (
                    any(c in turma.get('name') for c in criterios_map_turmas) 
                    and 
                    any(cc in turma.get('name') for cc in criterios_map_nivel) 
                    or "EJA" in turma.get('name')
                ):
                #!PODE LER AS ATIVIDADES E APAGAR DESEJADANOS CRITÉRIOS
            
                #* carregar as atividades
                atividades = servico_temporario.courses().courseWork().list(courseId=turma_id).execute().get('courseWork',False)
                if atividades:
                    atividades = [atv for atv in atividades if 'Avaliação diagnóstica' == atv.get('title') ]
                    if len(atividades):

                        #! DELETAR A ATIVIDADE
                        for atv in atividades:
                            try:
                                servico_temporario.courses().courseWork().delete(
                                    courseId=turma_id,
                                    id=atv.get('id')
                                ).execute()
                                msg = "Atividade {} apagad com sucesso na turma {}".format(atv.get("title"),turma_id)
                                print(msg)
                            except Exception as e:
                                print(
                                    "Falha ao apagar a atividade na turma: {}".format(turma_id)
                                )

    def copiar_atividade(self,turma_temporaria_id,servico_temporario,body,logger):
        try:
            """ APENAS EXECUTA A CÓPIA DA ATIVIDADE """
            # turma_temporaria_id
            # servico_temporario
            # body
            servico_temporario.courses().courseWork().create(
                courseId=turma_temporaria_id,
                body=body
            ).execute()
            logger.add_row_csv([
                "Sucesso",
                self.turma_id, # id turma origem
                self.name, # nome turma origem
                self.alternateLink, #link turma origem
                body.get('id'), #id atividade origem
                body.get('name'), # nome atividade
                turma_temporaria_id  #id turma destino   
            ])
            print(f"Atividade: {body.get('title')} funcionou")
        except Exception as e:
            print(f"Falhou por: {str(e)}")
            logger.add_row_csv([
                "Erro: {}".format(str(e)),
                self.turma_id, # id turma origem
                self.name, # nome turma origem
                self.alternateLink, #link turma origem
                body.get('id'), #id atividade origem
                body.get('name'), # nome atividade
                turma_temporaria_id  #id turma destino                   
            ])

    def inicicar_drive_service(self):
        pass
