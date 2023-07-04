import os
import json
from gestionDatos import GestionDatos
from conexionGmail import ConexionGmail

CUENTAS_FILE = "listaUsuarios.txt"
DATOS_USUARIO_FILE = "datosUsuario.json"

class ConfiguracionUsuario:
    def modificarDatos(self, direccionCorreo):
        usuario = GestionDatos.obtenerUsuario(direccionCorreo, DATOS_USUARIO_FILE)
        if usuario:
            # Obtener los datos actuales del usuario
            datos_actuales = {
                "nombres": usuario["nombres"],
                "apellidos": usuario["apellidos"],
                "direccionCorreo": direccionCorreo
            }

            print("Datos actuales:")
            print(datos_actuales)

            # Obtener los nuevos datos del usuario
            nuevos_datos = {}
            nuevos_datos["nombres"] = input("Ingrese los nuevos nombres: ")
            nuevos_datos["apellidos"] = input("Ingrese los nuevos apellidos: ")
            nuevos_datos["direccionCorreo"] = direccionCorreo

            # Actualizar los datos del usuario
            usuario.update(nuevos_datos)

            with open(DATOS_USUARIO_FILE, 'r+') as archivo:
                datosUsuario = json.load(archivo)
                datosUsuario[direccionCorreo] = usuario
                archivo.seek(0)
                json.dump(datosUsuario, archivo, indent=4)
                archivo.truncate()

            print("Datos actualizados correctamente.")
        else:
            print("Debe iniciar sesión primero")

    def eliminarCuenta(self, direccionCorreo):
        confirmacion = input("¿Está seguro de que desea eliminar su cuenta? (S/N): ")
        if confirmacion.upper() == "S":
            direccionConfirmacion = input("Ingrese su correo electrónico para confirmar la eliminación de la cuenta: ")
            if direccionConfirmacion == direccionCorreo:
                datosUsuario = GestionDatos.cargarDatosUsuario(DATOS_USUARIO_FILE)
                
                if direccionCorreo in datosUsuario: #Borrado de datos
                    del datosUsuario[direccionCorreo]
                    with open(DATOS_USUARIO_FILE, 'w') as archivo:
                        json.dump(datosUsuario, archivo, indent=4)

                with open(CUENTAS_FILE, 'r') as archivo: #Borrado de registro
                    lineas = archivo.readlines()
                with open(CUENTAS_FILE, 'w') as archivo:
                    for linea in lineas:
                        if direccionCorreo not in linea:
                            archivo.write(linea)
                    print("Cuenta eliminada correctamente.")
                    ConexionGmail.cerrarSesion(self)
                    return True
            else:
                print("Correo electrónico incorrecto. Cancelando la eliminación de la cuenta.")
                return False
        else:
            print("Cancelando la eliminación de la cuenta.")
        return False