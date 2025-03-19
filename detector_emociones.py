import nltk
nltk.download('all')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import numpy as np
from transformers import pipeline

class DetectorEmociones:
    def __init__(self):
        # Descargar recursos necesarios de NLTK
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        try:
            nltk.data.find('tokenizers/punkt/spanish.pickle')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        # Inicializar el modelo de análisis de sentimientos en español
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis", 
            model="pysentimiento/robertuito-sentiment-analysis",
            return_all_scores=True
        )
        
        # Diccionario de emociones negativas y palabras asociadas en español
        self.emociones_negativas = {
            'tristeza': ['triste', 'melancolía', 'pena', 'dolor', 'llanto', 'lágrima', 'sufrir', 'llorar', 'soledad', 'despedida'],
            'miedo': ['temor', 'terror', 'asustado', 'pánico', 'horror', 'temible', 'miedo', 'espanto', 'pesadilla'],
            'ira': ['enojo', 'rabia', 'furia', 'odio', 'resentimiento', 'cólera', 'ira', 'rencor', 'venganza'],
            'ansiedad': ['angustia', 'nervios', 'preocupación', 'inquietud', 'desasosiego', 'ansiedad', 'agobio'],
            'desesperación': ['desesperanza', 'impotencia', 'rendición', 'derrota', 'abismo', 'vacío', 'nada', 'perdido']
        }

    def analizar_poema(self, texto):
        try:
            # Dividir el texto en fragmentos más pequeños si es necesario
            max_length = 500  # Un poco menos que el límite típico de 512 tokens
            fragmentos = []
            
            # Dividir el texto por líneas primero
            lineas = texto.split('\n')
            fragmento_actual = ""
            
            for linea in lineas:
                # Si agregar esta línea excedería el límite, guardar el fragmento actual
                if len(fragmento_actual) + len(linea) > max_length and fragmento_actual:
                    fragmentos.append(fragmento_actual)
                    fragmento_actual = linea
                else:
                    fragmento_actual += "\n" + linea if fragmento_actual else linea
                    
            # Agregar el último fragmento si existe
            if fragmento_actual:
                fragmentos.append(fragmento_actual)
                
            # Si no hay fragmentos (caso improbable), usar el texto original
            if not fragmentos:
                fragmentos = [texto]
                
            # Analizar cada fragmento y combinar resultados
            sentimiento_negativo_total = 0
            
            for fragmento in fragmentos:
                if not fragmento.strip():
                    continue
                    
                try:
                    resultado = self.sentiment_analyzer(fragmento)
                    if resultado and len(resultado) > 0:
                        # Extraer score negativo
                        sentimiento_fragmento = next((score['score'] for score in resultado[0] if score['label'] == 'NEG'), 0)
                        sentimiento_negativo_total += sentimiento_fragmento
                except Exception as e:
                    print(f"Advertencia: Error al analizar un fragmento: {e}")
                    
            # Normalizar el sentimiento negativo total según la cantidad de fragmentos
            if fragmentos:
                sentimiento_negativo = sentimiento_negativo_total / len(fragmentos)
            else:
                sentimiento_negativo = 0
            
            # El resto del código es igual...
            # Tokenizar el texto (sin especificar idioma para evitar errores)
            tokens = word_tokenize(texto.lower())
            palabras = [palabra for palabra in tokens if palabra.isalpha()]
            
            # Contar ocurrencias de palabras relacionadas con emociones negativas
            conteo_emociones = {emocion: 0 for emocion in self.emociones_negativas}
            for palabra in palabras:
                for emocion, palabras_clave in self.emociones_negativas.items():
                    if palabra in palabras_clave or any(clave in palabra for clave in palabras_clave):
                        conteo_emociones[emocion] += 1
            
            # Determinar la emoción predominante
            emocion_predominante = max(conteo_emociones.items(), key=lambda x: x[1])
            
            # Calcular intensidad en escala de 1 a 10
            intensidad = min(round(sentimiento_negativo * 10, 1), 10)
            
            return {
                'sentimiento_negativo': sentimiento_negativo,
                'intensidad': intensidad,
                'emocion_predominante': emocion_predominante[0] if emocion_predominante[1] > 0 else 'neutral',
                'detalle_emociones': conteo_emociones
            }
        except Exception as e:
            print(f"Error durante el análisis: {e}")
            return {
                'sentimiento_negativo': 0,
                'intensidad': 0,
                'emocion_predominante': 'error',
                'detalle_emociones': {emocion: 0 for emocion in self.emociones_negativas}
            }

if __name__ == "__main__":
    detector = DetectorEmociones()
    
    print("📝 Detector de Emociones Negativas en Poemas (Español) 📝")
    print("--------------------------------------------------------")
    print("Ingresa un poema para analizar (escribe 'salir' para terminar):")
    
    while True:
        print("\nEscriba su poema (presione Enter dos veces para finalizar):")
        lineas = []
        while True:
            linea = input()
            if not linea:
                break
            lineas.append(linea)
        
        poema = "\n".join(lineas)
        
        if poema.lower() == 'salir':
            print("¡Hasta pronto!")
            break
            
        if not poema.strip():
            continue
            
        resultado = detector.analizar_poema(poema)
        
        print("\n✨ Resultado del análisis:")
        print(f"📊 Intensidad emocional negativa: {resultado['intensidad']}/10")
        print(f"😔 Emoción predominante: {resultado['emocion_predominante']}")
        print(f"📋 Detalle de emociones detectadas:")
        for emocion, valor in resultado['detalle_emociones'].items():
            if valor > 0:
                print(f"  - {emocion}: {valor} referencias")