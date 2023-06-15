from autenticacion import AutenticadorGmail
from sincronizacion import SincronizarGmail
from moverSpam import moverSpam

# Configuración de la API de Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDENTIALS_FILE = 'Ingeniería de Requisitos/Bote de spam/credentials.json'

def menu():
    print("Seleccione una opción:")
    print("1. Sincronizar correos electrónicos no leídos")
    print("2. Mover correos electrónicos marcados como spam")
    print("3. Salir")

while True:
    menu()
    opcion = input("Opción: ")

    if opcion == "1":
        authenticator = AutenticadorGmail(CREDENTIALS_FILE, SCOPES)
        creds = authenticator.autenticar()
        synchronizer = SincronizarGmail(creds)
        synchronizer.sincronizarEmailNoLeido()
    elif opcion == "2":
        authenticator = AutenticadorGmail(CREDENTIALS_FILE, SCOPES)
        creds = authenticator.autenticar()
        mover = moverSpam(creds)
        mover.obtenerCarpetasCorreo()
        spam_folder_name = input("Ingrese el nombre de la carpeta de spam: ")
        mover.moverCorreo(spam_folder_name)
    elif opcion == "3":
        break
    else:
        print("Opción inválida. Intente nuevamente.")