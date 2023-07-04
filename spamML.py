import numpy as np
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords
from stop_words import get_stop_words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

def limpiar_texto(texto):
  if pd.isnull(texto):
    return []
  nopunc = [char for char in texto if char not in string.punctuation]
  nopunc = ''.join(nopunc)
  palabras_procesadas = [palabra for palabra in nopunc.split() if palabra.lower() not in stopwords.words('spanish')]
  return palabras_procesadas

class SpamML:
    def __init__(self, texto):
        self.texto = texto
        self.df = pd.read_csv('labeled_emails_español.csv')
        nltk.download('stopwords')

    def detectarSpam(self):
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(how='any', inplace=True, axis=0)
        df1 = pd.DataFrame({'email': [self.texto], 'label': ["nn"]})
        df2 = pd.concat([self.df, df1])
        df2['email'].head().apply(limpiar_texto)
        email_bow = CountVectorizer(analyzer=limpiar_texto).fit_transform(self.df['email'])
        X_train, X_test, y_train, y_test = train_test_split(email_bow, self.df['label'], test_size=0.2, random_state=3)
        classifier = MultinomialNB().fit(X_train, y_train)
        x_train_pred = classifier.predict(X_train)
        x_test_pred = classifier.predict(X_test)
        a = CountVectorizer(analyzer=limpiar_texto).fit_transform(df2['email'])
        y_pred = classifier.predict(a)
        resultado = y_pred[-1]
        print("Predicción del spam: ", resultado)
        df1 = pd.DataFrame({'email': [self.texto], 'label': [resultado]})
        self.df = pd.concat([self.df, df1])


