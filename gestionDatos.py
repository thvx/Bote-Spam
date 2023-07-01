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