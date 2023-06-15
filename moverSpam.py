from googleapiclient.discovery import build
from autenticacion import AutenticadorGmail

class moverSpam:
    def __init__(self, credentials):
        self.credentials = credentials

    def obtenerCarpetasCorreo(self):
        # Acceso a la API de Gmail
        service = build('gmail', 'v1', credentials=self.credentials)

        # Obtener las carpetas de correo
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No se encontraron carpetas de correo.')
        else:
            print('Carpetas de correo:')
            for label in labels:
                print(label['name'])
                
    def moverCorreo(self, spam_folder_name):
        # Acceso a la API de Gmail
        service = build('gmail', 'v1', credentials=self.credentials)

        # Obtener el ID de la carpeta de destino
        labels = service.users().labels().list(userId='me').execute()
        spam_folder_id = None

        for label in labels['labels']:
            if label['name'] == spam_folder_name:
                spam_folder_id = label['id']
                break

        if spam_folder_id is None:
            print('No se encontró la carpeta de spam.')
        else:
            # Obtener los correos electrónicos marcados como spam
            results = service.users().messages().list(userId='me', q='is:spam').execute()
            spam_messages = results.get('messages', [])

            # Mover los correos electrónicos marcados como spam a la carpeta de destino
            for message in spam_messages:
                modify_request = {'removeLabelIds': ['INBOX'], 'addLabelIds': [spam_folder_id]}
                service.users().messages().modify(userId='me', id=message['id'], body=modify_request).execute()