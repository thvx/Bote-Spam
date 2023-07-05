import numpy as np
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def limpiar_texto(texto):
  if pd.isnull(texto):
    return []
  nopunc = [char for char in texto if char not in string.punctuation]
  nopunc = ''.join(nopunc)
  palabras_procesadas = [palabra for palabra in nopunc.split() if palabra.lower() not in stopwords.words('spanish')]
  return palabras_procesadas

class SpamML:
    def __init__(self):
        self.df = pd.read_csv('labeled_emails_español.csv')

    def configuracionSpam(self):
        print("Entrenando modelo...")
        nltk.download('stopwords')
        self.df = pd.read_csv('labeled_emails_español.csv')
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(how='any', inplace=True, axis=0)
        self.df['email'].head().apply(limpiar_texto)
        cv = CountVectorizer(analyzer=limpiar_texto)
        X_train = cv.fit_transform(self.df['email'])
        NB = MultinomialNB().fit(X_train, self.df['label'])
        print("¡Modelo entrenado exitosamente!\n\n")
        return cv, NB

    def getConfig(self, cv, NB):
        self.cv = cv
        self.NB = NB

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