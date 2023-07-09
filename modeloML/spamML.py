import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from joblib import dump, load

DATASET = r'modeloML\labeled_emails_español.csv'
def limpiar_texto(texto):
  if pd.isnull(texto):
    return []
  nopunc = [char for char in texto if char not in string.punctuation]
  nopunc = ''.join(nopunc)
  palabras_procesadas = [palabra for palabra in nopunc.split() if palabra.lower() not in stopwords.words('spanish')]
  return palabras_procesadas

class SpamML:
    def configuracionSpam(self):
        print("Entrenando modelo...")
        nltk.download('stopwords')
        self.df = pd.read_csv(DATASET)
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(how='any', inplace=True, axis=0)
        self.df['email'].head().apply(limpiar_texto)
        cv = CountVectorizer(analyzer=limpiar_texto)
        X_train = cv.fit_transform(self.df['email'])
        NB = MultinomialNB().fit(X_train, self.df['label'])
        print("¡Modelo entrenado exitosamente!\n\n")
        dump(NB, 'modelo_entrenado.joblib')

    def getTexto(self, texto):
        self.texto = texto
    def detectarSpam(self):
        NB = load('modelo_entrenado.joblib')
        self.email = pd.DataFrame({'email': [self.texto], 'label': ["nn"]})
        self.email['email'].head().apply(limpiar_texto)
        cv = CountVectorizer(analyzer=limpiar_texto)
        X_valid = cv.transform(self.email["email"])
        resultado = NB.predict(X_valid)
        print(f"El email es: {resultado}")
        df1 = pd.DataFrame({'email': [self.texto], 'label': [resultado]})
        self.df = pd.concat([df1, self.df])
        # self.df.to_csv(DATASET) // PARA EXPORTAR EL .CSV
        return resultado[0]