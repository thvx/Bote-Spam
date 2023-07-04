import json
import os
import string

from oauth2client import file, client, tools
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
import os.path
import re
import time
import dateutil.parser as parser
from datetime import datetime
import base64
from bs4 import BeautifulSoup
import datetime
import csv
import webbrowser
STORAGE_FILE = r'\storage.json'
class GestionDatos:
    @staticmethod
    def obtenerUsuario(direccionCorreo, datosUsuarioFile):
        with open(datosUsuarioFile, "r") as file:
            datosUsuario = json.load(file)
            if direccionCorreo in datosUsuario:
                return datosUsuario[direccionCorreo]
            else:
                print("Error: El usuario no existe")
                return None

    @staticmethod
    def existeCuenta(direccionCorreo, listaUsuariosFile):
        with open(listaUsuariosFile, 'r') as file:
            usuarios = file.read().splitlines()
            if direccionCorreo in usuarios:
                return True
            else:
                return False

    @staticmethod
    def agregarCuenta(direccionCorreo, listaUsuariosFile):
        with open(listaUsuariosFile, 'a') as file:
            file.write(direccionCorreo + '\n')

    @staticmethod
    def cargarDatosUsuario(datosUsuarioFile):
        if os.path.isfile(datosUsuarioFile):
            with open(datosUsuarioFile, 'r') as archivo:
                return json.load(archivo)
        else:
            return {}
    
    @staticmethod
    def guardarDatos(direccionCorreo, datosUsuario):
        datosUsuarioFile = "datosUsuario.json"

        if not os.path.isfile(datosUsuarioFile):
            with open(datosUsuarioFile, "w") as file:
                json.dump({}, file)

        with open(datosUsuarioFile, "r+") as file:
            datos = json.load(file)
            datos[direccionCorreo] = datosUsuario
            file.seek(0)
            json.dump(datos, file, indent=4)
            file.truncate()



    def obtenerUltimoCorreo():
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        store = file.Storage(STORAGE_FILE)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

        user_id = 'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

        mssg_list = unread_msgs['messages']

        final_list = []
        temp_dict = {}
        m_id = mssg_list[0]['id']
        message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
        payld = message['payload']
        try:
            # Fetching message body
            mssg_parts = payld['parts']  # fetching the message parts
            part_one = mssg_parts[0]  # fetching first element of the part
            part_body = part_one['body']  # fetching body of the message
            part_data = part_body['data']  # fetching data from the body
            clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
            clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
            clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
            print(clean_two)

        except:
            pass

