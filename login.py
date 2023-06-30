from conexionGmail import ConexionGmail
from gestionDatos import GestionDatos

CUENTAS_FILE = 'listaUsuarios.txt'
DATOS_USUARIO_FILE = 'datosUsuario.json'

class Login:
    def __init__(self, archivoCredenciales, scopes):
        self.autenticador = ConexionGmail(archivoCredenciales, scopes)
        self.archivoCredenciales = archivoCredenciales
        self.direccionCorreo = ""
    
    def registrarUsuario(self, direccionCorreo):
        self.autenticador.permitirAcceso()  
        if not GestionDatos.existeCuenta(direccionCorreo, CUENTAS_FILE):
            GestionDatos.agregarCuenta(direccionCorreo, CUENTAS_FILE)
            datosUsuario = {
                "nombres": "",  # Agrega los nombres del usuario
                "apellidos": ""  # Agrega los apellidos del usuario
            }
            GestionDatos.guardarDatos(direccionCorreo, datosUsuario)
            print("Cuenta creada exitosamente. Inicie sesión")
        else:
            print("Error en la creación de la cuenta. Volver a intentarlo")
    
    def iniciarSesion(self, direccionCorreo):
        if GestionDatos.existeCuenta(direccionCorreo, CUENTAS_FILE):
            # El usuario existe, mostrar el menú de opciones
            return True
        else:
            # El usuario no está registrado, volver al menú principal
            print("Usuario no registrado.")
            return False
