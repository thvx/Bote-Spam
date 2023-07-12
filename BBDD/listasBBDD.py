import sqlite3

class ListaBBDD:

    def __init__(self, correo):
        self.correo = correo
        self.conex = sqlite3.connect('BBDD/correosSpam')
        self.cursor = self.conex.cursor()

    def existeCorreo(self):
        self.cursor.execute(f'SELECT DIRECCION_CORREO FROM CORREOS_SPAM')
        correo_encontrado = self.cursor.fetchall()
        j = 0
        if correo_encontrado == []:
            return False
        for i in correo_encontrado:
            if correo_encontrado[j][0] == self.correo:
                return True
            j=j+1
        return False

    def actualizarReincidencia(self):
        self.cursor.execute(f"UPDATE CORREOS_SPAM SET REINCIDENCIAS=REINCIDENCIAS+1 WHERE DIRECCION_CORREO='{self.correo}'")
        self.conex.commit()

    def hallarReincidencias(self):
        self.cursor.execute(f"SELECT * FROM CORREOS_SPAM WHERE DIRECCION_CORREO='{self.correo}'")
        reincidencias = self.cursor.fetchone()[1]
        return reincidencias

    def agregarCorreo(self):
        self.cursor.execute(f"INSERT INTO CORREOS_SPAM VALUES('{self.correo}', 1)")
        self.conex.commit()
        self.conex.close()