# Portafolio de Interfaces Multimodales

Colección académica de Juan José Hoyos (Jhuza), a partir de los ejercicios del profesor Carlos Mario Correa. Reúne **18 experiencias: 17 apps independientes y un tablero propio integrado**.

[Abrir portafolio](https://jhginterfacesmultimodalesportfolio.streamlit.app/)

Identidad JHG con logo propio, 18 portadas vectoriales, botones azules y navegación compacta. El catálogo permite filtrar, buscar sin tildes, ordenar y limpiar la selección. Consulta [las decisiones de diseño](docs/DISENO-JHG.md).

## Ejecutar

```sh
python -m pip install -r requirements.txt
python -m streamlit run Intro.py
```

La entrada de Streamlit Cloud es `Intro.py`. `projects.json` contiene las fichas, enlaces y metadatos. `pages/18_Tablero.py` implementa el tablero con pincel, figuras, colores, grosores, formatos y exportación PNG/JSON.

## Evidencia y atribución

Cada ficha incluye propósito, entrada, salida, uso, tecnología, límites, demo y código. Las portadas son ilustraciones; no se presentan como capturas de resultados. La disponibilidad de APIs, modelos y dispositivos se verifica dentro de cada app.

El conteo de 18 corresponde a esta colección. Consulta la [comparación con el material de clase](docs/COBERTURA.md) para distinguirla de otros ejemplos enlazados por el profesor.

## Mantener la colección

Para incorporar otra app, añadir su ficha y enlaces propios a `projects.json`. Copiar `aurora.py`, `aurora.css`, `app_info.json` y el tema de `.streamlit/config.toml`; llamar a `app_header()` al iniciar. Revisar compatibilidad de dependencias antes de desplegar. No incluir claves ni resultados inventados.

## Verificación

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

Las pruebas verifican catálogo, enlaces propios, filtros, búsqueda, selección de fichas y controles/exportaciones del tablero con un lienzo simulado. Las interacciones reales del lienzo se revisan en el navegador.

[Guía visual](docs/guia-visual-aurora.md) · [Componentes Aurora](AURORA.md)
