import json
import os
from datetime import datetime

class GestionDatos:
    @staticmethod
    def obtenerUsuario(direccionCorreo, datosUsuarioFile):
        with open(datosUsuarioFile, "r") as file:
            datosUsuario = json.load(file)
            if direccionCorreo in datosUsuario:
                usuario = datosUsuario[direccionCorreo]
                #print("Datos del usuario:")
                #print(f"Nombres: {usuario['nombres']}")
                #print(f"Apellidos: {usuario['apellidos']}")
                #print(f"Correo electrónico: {direccionCorreo}")
            else:
                print("Error: El usuario no existe")

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
