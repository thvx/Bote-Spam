from googleapiclient.discovery import build

class SincronizarGmail:
    def __init__(self, credentials):
        self.credentials = credentials

    def sincronizarEmailNoLeido(self):
        service = build('gmail','v1', credentials = self.credentials)
        
        # Obtener los correos electrónicos en tiempo real
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        if not messages:
            print('No hay correos electrónicos no leídos.')
        else:
            print(f'Número de correos electrónicos no leídos: {len(messages)}')