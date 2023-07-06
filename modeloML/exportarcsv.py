import pandas as pd
from spamML import limpiar_texto

DATASET = r'modeloML\labeled_emails_español.csv'
class SpamML:
    def getTexto(self, texto):
        self.texto = texto
    def detectarSpam(self):
        self.email = pd.DataFrame({'email': [self.texto], 'label': ["nn"]})
        self.email['email'].head().apply(limpiar_texto)
        X_valid = self.cv.transform(self.email["email"])
        resultado = self.NB.predict(X_valid)
        print(f"El email es: {resultado}")
        df1 = pd.DataFrame({'email': [self.texto], 'label': [resultado]})
        self.df = pd.concat([df1, self.df])
        self.df.head(1)
        self.df.to_csv(DATASET)
        self.df.to_csv(DATASET, encoding='utf-8')