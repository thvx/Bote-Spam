import sys
from gestionUsuarios.conexionGmail import ConexionGmail
from gestionUsuarios.gestionDatos import GestionDatos
from gestionUsuarios.configuracionUsuario import ConfiguracionUsuario
from modeloML.spamML import SpamML
from BBDD.listasBBDD import ListaBBDD

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
        print("2. Configurar Detector de Spam")
        print("3. Detectar Spam")
        print("4. Eliminar cuenta")
        print("5. Cerrar sesion")
    
    def iniciarSesion(self, direccionCorreo, scopes):
        detectorSpam = SpamML()
        if GestionDatos.existeCuenta(direccionCorreo, CUENTAS_FILE) and self.autenticador.iniciarSesionGmail(scopes):
            self.menuUsuario()
            opcion = int(input("Opcion: "))
            while opcion > 0 and opcion < 6:
                if opcion == 1:
                    ConfiguracionUsuario.modificarDatos(self, direccionCorreo)
                elif opcion == 2:
                    try:
                        cv, NB = detectorSpam.configuracionSpam()
                    except:
                        print("Ocurrió un error... \n\n")
                elif opcion == 3:
                    ultimoCorreo = GestionDatos.obtenerUltimoCorreo()
                    detectorSpam.getConfig(cv, NB)
                    if type(ultimoCorreo) != type(None):
                        encoding = sys.getdefaultencoding()
                        ultimoCorreo = ultimoCorreo.decode(encoding)
                        print("El correo es: \n \n" + ultimoCorreo)
                        detectorSpam.getTexto(ultimoCorreo)
                        resultado = detectorSpam.detectarSpam()
                        if resultado == "spam":
                            elc = input("¿Desea guardar la dirección de correo detectada como spam?\ns: si\nn:no\n")
                            if elc == 's':
                                correoSpam = input("Ingrese el nombre de usuario de la dirección de correo spam: ")
                                gestionLista = ListaBBDD(correoSpam)
                                if gestionLista.existeCorreo():
                                    gestionLista.actualizarReincidencia()
                                    reincidencias = gestionLista.hallarReincidencias()
                                    if reincidencias > 5:
                                        print("El correo electrónico supera las 5 reincidencias. Se recomienda bloquearlo ante tantos envíos de correo spam.")
                                else:
                                    gestionLista.agregarCorreo()
                            else:
                                print("Gracias por utilizar Bote-Spam\n")
                    else:
                        print("No se ha podido detectar un correo de manera correcta")
                elif opcion == 4:
                    if ConfiguracionUsuario.eliminarCuenta(self, direccionCorreo):
                        break
                    else:
                        self.menuUsuario()
                elif opcion == 5:
                    ConexionGmail.cerrarSesion(self)
                    break
                else:
                    print("Opcion invalida. Intente nuevamente.")
                self.menuUsuario()
                opcion = int(input("Opcion: "))
        else:
            print("Usuario no registrado.")
            return False
