from projeto.settings import MAILING_ENDPOINT
from django.template.loader import render_to_string
import requests
from pylib.googleadmin import authService
from projeto.settings import MAILING_JSON, MAILING_FROM
from email.mime.text import MIMEText
import base64
escopos = {
        "https://mail.google.com/",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.addons.current.action.compose",
}


class Email():
    def __init__(self,endpoint=MAILING_ENDPOINT):
        self.endpoint = endpoint
        self.mensagem = ""
        self.remetentes = []
        self.assunto = "Notificação"
        self.enviado = False
        self.erro = False

    def enviar(self):
        try:
            response = requests.post(
                self.endpoint,
                data=self.getDados()
            )
            try:
                confirmacao = response.json()['Email']
                if 'Enviado' in confirmacao:
                    self.enviado = True
            except Exception as e:
                self.erro = str(e)
        except Exception as e:
            self.erro = str(e)

    def getMensagem(self):
        message = MIMEText(self.mensagem, 'html')
        message['to'] = ','.join(self.remetentes)
        message['from'] = MAILING_FROM
        message['subject'] = self.assunto
        message
        encoded_message =base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': encoded_message.decode()}

    def enviarGmail(self):
        try:
            service = authService(escopos,MAILING_JSON,MAILING_FROM).getService('gmail','v1')
            mensagem = self.getMensagem()
            message = service.users().messages().send(userId='me', body=mensagem).execute()
            
        except Exception as e:
            return False
            
    def getDados(self):
        return {
            "para":self.remetentes,
            "assunto":self.assunto,
            "mensagem":self.mensagem
        }
        
    def setAssunto(self,assunto):
        self.assunto = assunto or "Notificação"
        return self

    def addRementente(self,email):
        """ Adicionar email a lista de remetentes """ 
        self.remetentes.append(email)
        return self

    def setMensagem(self,template,contexto=None):
        """ Prepara html da mensagem """ 
        # template: caminho do html da mensagem
        # contexto: dicionário para carregar no html de template
        if contexto is not None:
            self.mensagem = render_to_string(template,contexto)
        else:
            self.mensagem = render_to_string(template)

        return self


