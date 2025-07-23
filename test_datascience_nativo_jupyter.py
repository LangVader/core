# CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL DATA SCIENCE
# Archivo .vdr ejecutado nativamente para Jupyter Notebook

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

class VaderDataScienceJupyter:
    def __init__(self):
        self.data = None
        print("📊 VADER 7.0 - Jupyter Data Science Runtime")
    
    def cargar_datos(self, archivo, tipo='csv'):
        if tipo == 'csv':
            self.data = pd.read_csv(archivo)
        elif tipo == 'excel':
            self.data = pd.read_excel(archivo)
        print(f"✅ Datos cargados: {self.data.shape}")
        return self.data
    
    def explorar_datos(self):
        print("📋 INFORMACIÓN DEL DATASET")
        print(f"Forma: {self.data.shape}")
        print(f"Columnas: {list(self.data.columns)}")
        print(self.data.describe())
        return self.data.head()
    
    def crear_visualizaciones(self):
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            self.data[numeric_cols].hist(figsize=(12, 8))
            plt.tight_layout()
            plt.show()
    
    def entrenar_modelo(self, target_col):
        feature_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
        feature_cols.remove(target_col)
        
        X = self.data[feature_cols]
        y = self.data[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        score = model.score(X_test, y_test)
        print(f"Precisión del modelo: {score:.4f}")
        
        return model

# Crear instancia
vader_ds = VaderDataScienceJupyter()
print("🎯 Análisis Vader Data Science listo")
