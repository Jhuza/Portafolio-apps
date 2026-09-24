import base64
from html import escape
from pathlib import Path
import streamlit as st
from aurora import footer, hero, section, setup
from projects import PROJECTS

ROOT = Path(__file__).resolve().parent
setup("Interfaces multimodales", "PORTAFOLIO / IA")
hero("PORTAFOLIO DE INTERFACES MULTIMODALES", "Distintas entradas.", "Nuevas perspectivas.",
     "Una colección de aplicaciones de inteligencia artificial para explorar texto, imágenes, documentos y sonido.", kind="vision")

with st.sidebar:
    st.subheader("Aplicaciones con inteligencia artificial")
    st.write("La inteligencia artificial permite mejorar la toma de decisiones con el uso de datos, automatizar tareas rutinarias y proporcionar análisis avanzados en tiempo real, lo que resulta en una mayor eficiencia y precisión en diversos campos.")
    st.caption("Una colección para explorar distintas formas de interacción entre personas y modelos.")


@st.cache_data(show_spinner=False)
def image_data(filename):
    """Bundle existing repository art; no external asset request is required."""
    content = (ROOT / filename).read_bytes()
    mime = "image/png" if filename.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(content).decode('ascii')}"


section("01—09", "Explora las experiencias", "Texto / Imagen / Audio / Datos")
cards = []
for index, project in enumerate(PROJECTS, start=1):
    source_link = ""
    if project.get("repo"):
        source_link = f'<a href="{escape(project["repo"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Ver código de {escape(project["title"], quote=True)}">Código ↗</a>'
    cards.append(
        '<article class="aurora-project">'
        f'<div class="aurora-cover"><img src="{image_data(project["image"])}" alt="" loading="lazy"><span class="aurora-cover-index">{index:02d}</span></div>'
        f'<div class="aurora-project-body"><p class="aurora-project-tag">{escape(project["category"])}</p>'
        f'<h3>{escape(project["title"])}</h3><p class="aurora-project-description">{escape(project["description"])}</p>'
        f'<div class="aurora-project-links"><a href="{escape(project["url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Abrir {escape(project["title"], quote=True)}">Explorar aplicación ↗</a>{source_link}</div></div></article>'
    )
st.markdown('<div class="aurora-project-grid">' + "".join(cards) + '</div>', unsafe_allow_html=True)

st.markdown('<aside class="aurora-resource"><div><h3>Seguir explorando</h3><p>Páginas y ejercicios prácticos sobre aplicaciones de inteligencia artificial.</p></div><a href="https://sites.google.com/view/aplicacionesdeia/inicio" target="_blank" rel="noopener noreferrer">Ver recursos ↗</a></aside>', unsafe_allow_html=True)
footer("APRENDER / EXPLORAR / CONSTRUIR")
