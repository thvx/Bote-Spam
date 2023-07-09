import sqlite3

class ListaBBDD:

    def __init__(self, correo):
        self.correo = correo
        self.conex = sqlite3.connect('correoSpam')
        self.cursor = self.conex.cursor()

    def existeCorreo(self):
        self.cursor.execute(f'SELECT * FROM CORREOS_SPAM WHERE DIRECCIÓN_CORREO={self.correo}')
        correo_encontrado = self.cursor.fetchone()
        if correo_encontrado == self.correo:
            return True
        else:
            return False

    def actualizarReincidencia(self):
        self.cursor.execute(f"UPDATE CORREOS_SPAM SET REINCIDENCIAS=REINCIDENCIAS+1 WHERE DIRECCIÓN_CORREO={self.correo}")
        self.conex.commit()

    def hallarReincidencias(self):
        self.cursor.execute(f"SELECT * FROM CORREOS_SPAM WHERE DIRECCIÓN_CORREO={self.correo}")
        reincidencias = self.cursor.fetchone()[1]
        return reincidencias

    def agregarCorreo(self):
        self.cursor.execute(f'INSERT INTO CORREOS_SPAM VALUES({self.correo}, 1)')
        self.conex.close()