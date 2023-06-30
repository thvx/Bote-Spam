from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os.path
import json
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

    def iniciarSesionGmail(self):
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        creds = None

        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, self.scopes)

        if not creds or not creds.valid:
            if not creds:
                # No existe el archivo de token, se solicita acceso al usuario
                creds = self.permitirAcceso()

            if not os.path.exists(os.path.dirname(TOKEN_FILE)):
                # Se crea el directorio si no existe
                os.makedirs(os.path.dirname(TOKEN_FILE))

            # Se guarda el archivo de token
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        url = service.authorization_url()
        webbrowser.open(url)
        return service
    
    def obtenerUsuario(self, service):
        user_info = service.users().getProfile(userId='me').execute()
        return user_info