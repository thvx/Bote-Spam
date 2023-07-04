from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

TOKEN_FILE = r'token.json'
STORAGE_FILE = r'\storage.json'

class ConexionGmail:
    def __init__(self, archivoCredenciales, scopes):
        self.archivoCredenciales = archivoCredenciales
        self.scopes = scopes

    def permitirAcceso(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.archivoCredenciales, self.scopes)
        creds = flow.run_local_server(port=0)
        return creds
    
    def obtenerURLAutorizacion(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.archivoCredenciales, self.scopes)
        authorization_url, _ = flow.authorization_url(prompt='consent')
        return authorization_url

    def iniciarSesionGmail(self, SCOPES):
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.archivoCredenciales, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        service = build('gmail', 'v1', credentials = creds)
        user_id =  'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        try:
            unread_msgs = service.users().messages().list(userId=user_id,labelIds=[label_id_one, label_id_two]).execute()
            # We get a dictonary. Now reading values for the key 'messages'
            mssg_list = unread_msgs['messages']
            print ("Total unread messages in inbox: ", str(len(mssg_list)))

            labels = service.users().labels().list(userId=user_id).execute()
            labels_list = labels.get('labels', [])

            if not labels_list:
                print("No se encontraron carpetas.")
            else:
                print("Carpetas:")
                for label in labels_list:
                    print(label['name'])

            return True
        except Exception as e:
            print("Error al iniciar sesión:", str(e))
            return False
        
    def obtenerUsuario(self, service):
        user_info = service.users().getProfile(userId='me').execute()
        return user_info
    
    def cerrarSesion(self):
        if os.path.exists(TOKEN_FILE):
            os.remove(TOKEN_FILE)
            print("Sesion cerrada correctamente.")
        else:
            print("No hay sesión activa")