# Detector de Emociones Negativas en Poemas

Este proyecto es una herramienta para analizar poemas en español y detectar emociones negativas predominantes. Utiliza la biblioteca `transformers` de Hugging Face y recursos de `nltk` para realizar el análisis de sentimientos.

## Requisitos

Para instalar las dependencias necesarias, ejecuta:

```sh
pip install -r requirements.txt
```

## Uso

Para ejecutar el detector de emociones, simplemente ejecuta el script `detector_emociones.py`:

```sh
python detector_emociones.py
```

El programa te pedirá que ingreses un poema y luego analizará el texto para detectar emociones negativas. Mostrará la intensidad emocional negativa y la emoción predominante.

## Estructura del Proyecto

- `detector_emociones.py`: Script principal que contiene la clase `DetectorEmociones` y el código para ejecutar el análisis.
- `requirements.txt`: Archivo con las dependencias necesarias para el proyecto.
- `.gitignore`: Archivo para ignorar archivos y carpetas innecesarias en el control de versiones.

## Ejemplo de Uso

```sh
📝 Detector de Emociones Negativas en Poemas (Español) 📝
--------------------------------------------------------
Ingresa un poema para analizar (escribe 'salir' para terminar):

Escriba su poema (presione Enter dos veces para finalizar):
En un rincón del alma
donde el sol no brilla
la tristeza se esconde
y el dolor se anida

✨ Resultado del análisis:
📊 Intensidad emocional negativa: 7.5/10
😔 Emoción predominante: tristeza
📋 Detalle de emociones detectadas:
  - tristeza: 3 referencias
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para discutir cualquier cambio que te gustaría hacer.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
