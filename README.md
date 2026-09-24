# Portafolio · Interfaces multimodales

Galería de las nueve experiencias originales de texto, imagen, audio, documentos, datos y sistemas ciberfísicos. Dirección visual Aurora: negro profundo, azul/naranja, tarjetas con las imágenes originales y tipografía editorial.

## Ejecutar

Python 3.10 o posterior. Validación local realizada con Python 3.12.

```sh
python -m pip install -r requirements.txt
python -m streamlit run Intro.py
```

La entrada de Streamlit Cloud sigue siendo `Intro.py`. El catálogo está en `projects.py`: conserva las nueve experiencias y el acceso a recursos educativos. ChatPDF y Visión usan los enlaces de despliegue indicados por el propietario y enlazan a sus repositorios. Los otros siete destinos se mantienen; su disponibilidad externa no forma parte de las pruebas locales.

Las imágenes originales se incluyen desde el repositorio, sin solicitudes a un proveedor externo. La cuadrícula pasa de tres columnas a dos y a una en pantallas pequeñas. Los enlaces tienen nombres accesibles y foco de teclado visible; se respeta la preferencia de reducción de movimiento.

## Verificación

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

La prueba arranca la app y verifica las nueve tarjetas, los dos destinos actualizados, los repositorios y los enlaces educativos conservados.

Consulta `AURORA.md` para mantener la identidad compartida con las otras apps.
