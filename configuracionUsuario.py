import os
import json
from gestionDatos import GestionDatos

CUENTAS_FILE = "listaUsuarios.txt"
DATOS_USUARIO_FILE = "datosUsuario.json"

class ConfiguracionUsuario:
    @staticmethod
    def menu():
        print("1. Modificar datos")
        print("2. Eliminar cuenta")
        print("3. Volver al menú principal")

    @staticmethod
    def modificarDatos(direccionCorreo):
        usuario = GestionDatos.obtenerUsuario(direccionCorreo, DATOS_USUARIO_FILE)
        if usuario:
            # Obtener los datos actuales del usuario
            datos_actuales = {
                "nombres": usuario["nombres"],
                "apellidos": usuario["apellidos"],
                "direccionCorreo": usuario["direccionCorreo"]
            }

            print("Datos actuales:")
            print(datos_actuales)

            # Obtener los nuevos datos del usuario
            nuevos_datos = {}
            nuevos_datos["nombres"] = input("Ingrese los nuevos nombres: ")
            nuevos_datos["apellidos"] = input("Ingrese los nuevos apellidos: ")
            nuevos_datos["direccionCorreo"] = input("Ingrese el nuevo correo electrónico: ")

            # Actualizar los datos del usuario
            usuario.update(nuevos_datos)

            with open(DATOS_USUARIO_FILE, 'w') as archivo:
                json.dump(usuario, archivo)
            print("Datos actualizados correctamente.")
        else:
            print("Debe iniciar sesión primero")

    @staticmethod
    def eliminarCuenta(direccionCorreo):
        usuario = GestionDatos.obtenerUsuario(direccionCorreo, DATOS_USUARIO_FILE)
        if usuario:
            confirmacion = input("¿Está seguro de que desea eliminar su cuenta? (S/N): ")
            if confirmacion.upper() == "S":
                direccionCorreo = input("Ingrese su correo electrónico para confirmar la eliminación de la cuenta: ")

                if direccionCorreo == usuario["direccionCorreo"]:
                    os.remove(CUENTAS_FILE)
                    os.remove(DATOS_USUARIO_FILE)
                    print("Cuenta eliminada correctamente.")
                else:
                    print("Correo electrónico incorrecto. Cancelando la eliminación de la cuenta.")
            else:
                print("Cancelando la eliminación de la cuenta.")
        else:
            print("Debe iniciar sesión primero")
