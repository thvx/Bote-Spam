import sys
from gestionUsuarios.conexionGmail import ConexionGmail
from gestionUsuarios.gestionDatos import GestionDatos
from gestionUsuarios.configuracionUsuario import ConfiguracionUsuario
from modeloML.spamML import SpamML
from modeloML.listas import menuListas

CUENTAS_FILE = r'gestionUsuarios\listaUsuarios.txt'
DATOS_USUARIO_FILE = r'gestionUsuarios\datosUsuario.json'

class Login:
    def __init__(self, archivoCredenciales, scopes):
        self.autenticador = ConexionGmail(archivoCredenciales, scopes)
        self.archivoCredenciales = archivoCredenciales
    
    def registrarUsuario(self, direccionCorreo):
        if not GestionDatos.existeCuenta(direccionCorreo, CUENTAS_FILE):
            self.autenticador.permitirAcceso()  
            GestionDatos.agregarCuenta(direccionCorreo, CUENTAS_FILE)
            datosUsuario = {
                "nombres": "",  # Agrega los nombres del usuario
                "apellidos": ""  # Agrega los apellidos del usuario
            }
            GestionDatos.guardarDatos(direccionCorreo, datosUsuario)
            print("Cuenta creada exitosamente. Inicie sesión")
        else:
            print("La cuenta ya se encuentra registrada. Iniciar sesion")

    @staticmethod
    def menuUsuario():
        print("Seleccione una opción:")
        print("1. Editar datos de usuario")
        print("2. Configurar spam")
        print("3. Detectar Spam")
        print("4. Realizar acciones sobre el spam")
        print("5. Eliminar cuenta")
        print("6. Cerrar sesion")
    
    def iniciarSesion(self, direccionCorreo, scopes):
        detectorSpam = SpamML()
        if GestionDatos.existeCuenta(direccionCorreo, CUENTAS_FILE) and self.autenticador.iniciarSesionGmail(scopes):
            self.menuUsuario()
            opcion = int(input("Opcion: "))
            while opcion > 0 and opcion < 6:
                if opcion == 1:
                    ConfiguracionUsuario.modificarDatos(self, direccionCorreo)
                elif opcion == 2:
                    cv, NB = detectorSpam.configuracionSpam()
                elif opcion == 3:
                    ultimoCorreo = GestionDatos.obtenerUltimoCorreo()
                    encoding = sys.getdefaultencoding()
                    ultimoCorreo = ultimoCorreo.decode(encoding)
                    print("El correo es: \n \n" + ultimoCorreo)
                    detectorSpam.getTexto(ultimoCorreo)
                    detectorSpam.getConfig(cv, NB)
                    detectorSpam.detectarSpam()
                elif opcion ==4:
                    menuListas()
                elif opcion == 5:
                    if ConfiguracionUsuario.eliminarCuenta(self, direccionCorreo):
                        break
                    else:
                        self.menuUsuario()
                elif opcion == 6:
                    ConexionGmail.cerrarSesion(self)
                    break
                else:
                    print("Opcion invalida. Intente nuevamente.")
                self.menuUsuario()
                opcion = int(input("Opcion: "))
        else:
            print("Usuario no registrado.")
            return False