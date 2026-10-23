# Portafolio de Interfaces Multimodales

Colección académica de Juan José Hoyos (Jhuza), a partir de los ejercicios de clase del profesor Carlos Mario Correa. Reúne 14 despliegues propios; el objetivo es incorporar las 18 experiencias. Los cuatro espacios restantes no se presentan como apps terminadas.

## Ejecutar

```sh
python -m pip install -r requirements.txt
python -m streamlit run Intro.py
```

La entrada de Streamlit Cloud sigue siendo `Intro.py`. `projects.json` contiene las fichas, enlaces propios y metadatos. `projects.py` carga el catálogo y su objetivo. El número de apps se calcula desde los registros reales.

## Incorporar una app

Después de crear el fork y desplegarlo, agregar su ficha a `projects.json`: título, modalidad, propósito, entrada, salida, pasos, tecnología, límites, URL de la demo y repositorio de Jhuza. Reutilizar una portada del repositorio o añadir una ilustración propia. Las ilustraciones no son evidencias de ejecución. No incluir claves de API ni resultados inventados.

Copiar el tema y los componentes Aurora al nuevo repo, añadir `app_info.json` y llamar a `app_header()` al iniciar su interfaz. Conservar sus dependencias y su lógica; revisar su versión de Python antes de desplegar.

## Verificación

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

Las pruebas verifican el catálogo, enlaces propios, filtros, búsquedas y selección de fichas. No certifican disponibilidad de modelos o dispositivos externos. Consulta [la guía visual](docs/guia-visual-aurora.md) y [AURORA.md](AURORA.md).
