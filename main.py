from login import Login
from configuracionUsuario import ConfiguracionUsuario

scopes = ['https://www.googleapis.com/auth/gmail.readonly']
archivoCredenciales = 'credentials.json'

def menuPrincipal():
    print("Seleccione una opción:")
    print("1. Registrar usuario")
    print("2. Iniciar sesión")
    print("3. Salir")

def menuUsuario():
    print("Seleccione una opción:")
    print("1. Configuracion de usuario")
    print("2. Sincronizar correo")
    print("3. Detectar Spam")
    print("4. Volver al menú principal")

def ejecutar():
    login = Login(archivoCredenciales, scopes)

    opcionPrincipal = 0
    opcionUsuario = 0

    while opcionPrincipal != 3:
        menuPrincipal()
        opcionPrincipal = int(input("Opcion: "))

        if opcionPrincipal == 1:
            direccionCorreo = input("Ingrese su direccion de correo: ")
            login.registrarUsuario(direccionCorreo)
        elif opcionPrincipal == 2:
            direccionCorreo = input("Ingrese su direccion de correo: ")
            if login.iniciarSesion(direccionCorreo):
                while opcionUsuario != 4:
                    menuUsuario()
                    opcionUsuario = int(input("Opcion: "))
                    if opcionUsuario == 1:
                        ConfiguracionUsuario.menu()
                        opcionConf = int(input("Opcion: "))
                        if opcionConf == 1:
                            ConfiguracionUsuario.modificarDatos(direccionCorreo)
                        elif opcionConf == 2:
                            ConfiguracionUsuario.eliminarCuenta(direccionCorreo)
                        else:
                            break
                    elif opcionUsuario == 2:
                        print("Sincronizar correo")
                    elif opcionUsuario == 3:
                        print("Detectar Spam")
                    elif opcionUsuario == 4:
                        break
                    else:
                        print("Operacion invalida. Intente nuevamente.")
            elif opcionPrincipal == 3:
                break
        else:
            print("Opcion invalida. Intente nuevamente.")

if __name__ == "__main__":
    ejecutar()
