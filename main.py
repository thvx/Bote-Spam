from gestionUsuarios.login import Login

scopes = ['https://www.googleapis.com/auth/gmail.readonly']
archivoCredenciales = r'credencialesAcceso\credentials.json'

def menuPrincipal():
    print("Seleccione una opción:")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

def ejecutar():
    login = Login(archivoCredenciales, scopes)

    opcionPrincipal = 0

    while opcionPrincipal != 3:
        menuPrincipal()
        opcionPrincipal = int(input("Opcion: "))
        if opcionPrincipal == 1:
            direccionCorreo = input("Ingrese su direccion de correo: ")
            login.registrarUsuario(direccionCorreo)
        elif opcionPrincipal == 2:
            direccionCorreo = input("Ingrese su direccion de correo: ")
            login.iniciarSesion(direccionCorreo, scopes)
        elif opcionPrincipal == 3:
            break
        else:
            print("Opcion invalida. Intente nuevamente.")

if __name__ == "__main__":
    ejecutar()
