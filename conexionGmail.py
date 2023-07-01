from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import webbrowser

TOKEN_FILE = r'G:\Mi unidad\V ciclo\Ingeniería de Requisitos\Bote de spam\token.json'

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

        service = build('gmail', 'v1', credentials=creds)
        try:
            results = service.users().messages().list(userId='me').execute()
            message_count = results.get('resultSizeEstimate', 0)
            print(f"Número de mensajes: {message_count}")
            return True
        except Exception as e:
            print("Error al iniciar sesión:", str(e))
            return False
        
    def obtenerUsuario(self, service):
        user_info = service.users().getProfile(userId='me').execute()
        return user_info