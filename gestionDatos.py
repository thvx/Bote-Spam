import json
import os

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


    def obtenerUltimoCorreo(self):
        SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
        store = file.Storage(STORAGE_FILE)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)
        GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

        user_id = 'me'
        label_id_one = 'INBOX'
        label_id_two = 'UNREAD'

        unread_msgs = GMAIL.users().messages().list(userId='me', labelIds=[label_id_one, label_id_two]).execute()

        mssg_list = unread_msgs['messages']

        final_list = []

        for mssg in mssg_list:
            temp_dict = {}
            m_id = mssg['id']
            message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()
            payld = message['payload']
            headr = payld['headers']

            for one in headr:
                if one['name'] == 'Subject':
                    msg_subject = one['value']
                    temp_dict['Subject'] = msg_subject
                else:
                    pass

            for two in headr:
                if two['name'] == 'Date':
                    msg_date = two['value']
                    date_parse = (parser.parse(msg_date))
                    m_date = (date_parse.date())
                    temp_dict['Date'] = str(m_date)
                else:
                    pass

            for three in headr:
                if three['name'] == 'From':
                    msg_from = three['value']
                    temp_dict['Sender'] = msg_from
                else:
                    pass

            temp_dict['Snippet'] = message['snippet']

            try:

                # Fetching message body
                mssg_parts = payld['parts']  # fetching the message parts
                part_one = mssg_parts[0]  # fetching first element of the part
                part_body = part_one['body']  # fetching body of the message
                part_data = part_body['data']  # fetching data from the body
                clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
                clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
                soup = BeautifulSoup(clean_two, "lxml")
                mssg_body = soup.body()
                # mssg_body is a readible form of message body
                # depending on the end user's requirements, it can be further cleaned
                # using regex, beautiful soup, or any other method
                temp_dict['Message_body'] = mssg_body

            except:
                pass

            final_list.append(temp_dict)  # This will create a dictonary item in the final list

            # This will mark the messagea as read
            GMAIL.users().messages().modify(userId=user_id, id=m_id, body={'removeLabelIds': ['UNREAD']}).execute()
            with open('labeled_emails_español.csv', 'w', encoding='utf-8', newline='') as csvfile:
                fieldnames = ['email', 'label']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
                writer.writeheader()
                writer.writerow(final_list['Message_body'])
                writer.writerow('ham')