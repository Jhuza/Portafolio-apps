import io
import json
from pathlib import Path
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from aurora import setup, hero, project_context, section, footer

ROOT=Path(__file__).resolve().parents[1]
project=json.loads((ROOT/'tablero_info.json').read_text(encoding='utf-8'))
setup("Tablero propio","DIBUJO / INTERACCIÓN")
hero(project['title'],project['headline'],project['accent'],project['description'],kind='vision')
project_context(project)
with st.sidebar:
    st.subheader("Configura tu tablero")
    mode=st.selectbox("Herramienta",['Pincel','Línea','Rectángulo','Círculo'])
    stroke_width=st.slider("Grosor del trazo",1,30,5)
    stroke_color=st.color_picker("Color del trazo",'#4C8DFF')
    bg_color=st.color_picker("Color del fondo",'#0D1420')
    fill=st.checkbox("Rellenar figuras",value=False)
    fill_color=st.color_picker("Color del relleno",'#FF8A4C') if fill else 'rgba(0,0,0,0)'
    shape=st.selectbox("Formato",['Cuadrado','Vertical','Horizontal'])
    st.caption("Cambiar el formato o el fondo inicia un tablero nuevo. Descarga primero el dibujo que quieras conservar.")

height={'Cuadrado':320,'Vertical':400,'Horizontal':240}[shape]
mode_value={'Pincel':'freedraw','Línea':'line','Rectángulo':'rect','Círculo':'circle'}[mode]
left,right=st.columns([1,1],gap='large')
with left:
    section('01','Dibuja','Ratón o pantalla táctil')
    st.caption("La barra del lienzo permite mover objetos, deshacer, rehacer y limpiar. Aparece al pasar sobre el tablero.")
    canvas=st_canvas(fill_color=fill_color,stroke_width=stroke_width,stroke_color=stroke_color,background_color=bg_color,width=320,height=height,drawing_mode=mode_value,return_image_data=True,key=f'own_canvas_{shape}_{bg_color}')
with right:
    section('02','Guarda tu creación','PNG / JSON')
    if canvas.image_data is not None and canvas.json_data and canvas.json_data.get('objects'):
        data=io.BytesIO()
        Image.fromarray(np.asarray(canvas.image_data,dtype=np.uint8),'RGBA').save(data,format='PNG')
        st.image(data.getvalue(),caption='Vista previa de tu dibujo',width=320)
        st.download_button('Descargar dibujo PNG',data.getvalue(),file_name='tablero-aurora.png',mime='image/png')
        st.download_button('Descargar trazos JSON',json.dumps(canvas.json_data,ensure_ascii=False,indent=2),file_name='trazos-aurora.json',mime='application/json')
        st.caption(f"{len(canvas.json_data['objects'])} objetos en el tablero · 320 × {height} px")
    else:
        st.info('Dibuja para habilitar la vista previa y las descargas.')
footer('EXPLORAR / DIBUJAR / CREAR')
