import base64
from html import escape
from pathlib import Path
import streamlit as st
from aurora import footer, hero, project_context, section, setup
from projects import PROJECTS, TARGET_COUNT

ROOT = Path(__file__).resolve().parent
setup("Interfaces multimodales", "PORTAFOLIO / IA", sidebar="collapsed")
hero("PORTAFOLIO DE INTERFACES MULTIMODALES", "Distintas entradas.", "Nuevas perspectivas.",
     "Texto, imágenes, voz y dispositivos. Una colección de experiencias para explorar cómo nos comunicamos con la tecnología.", kind="vision")
st.markdown('<p class="aurora-author">Juan José Hoyos · JHUZA / LAB · Interfaces multimodales</p>', unsafe_allow_html=True)
pending = max(TARGET_COUNT - len(PROJECTS), 0)
st.markdown(f'<div class="aurora-summary"><span><strong>{len(PROJECTS):02d}</strong> experiencias multimodales</span><span><strong>17</strong> apps independientes</span><span><strong>01</strong> tablero integrado</span></div>', unsafe_allow_html=True)

with st.sidebar:
    st.subheader("Sobre la colección")
    st.write("Portafolio académico de Juan José Hoyos. Reúne las aplicaciones desarrolladas y adaptadas en la clase de Interfaces Multimodales.")
    st.caption("Ejercicios y repositorios base compartidos por el profesor Carlos Mario Correa. Personalización e integración visual: Jhuza.")
    st.markdown("[Material de la clase ↗](https://sites.google.com/view/interfacesmultimodales/p%C3%A1gina-principal)")
    st.markdown("[Guía visual Aurora ↗](https://github.com/Jhuza/Portafolio-apps/blob/main/docs/guia-visual-aurora.md)")
    st.caption("17 despliegues propios y un tablero integrado en este portafolio. La disponibilidad de modelos, APIs, cámara y dispositivos se comprueba dentro de cada app.")


@st.cache_data(show_spinner=False)
def image_data(filename):
    content = (ROOT / filename).read_bytes()
    mime = "image/png" if filename.endswith(".png") else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(content).decode('ascii')}"


section("01", "Explora las experiencias", "Cada proyecto abre su propia app")
left, right = st.columns([1, 2])
with left:
    category = st.selectbox("Filtrar por modalidad", ["Todas"] + sorted({p["category"] for p in PROJECTS}))
with right:
    query = st.text_input("Buscar una experiencia", placeholder="Por ejemplo: OCR, voz, sensores…").strip().casefold()
filtered = [(index, p) for index, p in enumerate(PROJECTS, 1)
            if (category == "Todas" or p["category"] == category)
            and (not query or query in " ".join(str(p[k]) for k in ("slug", "title", "description", "technology", "category")).casefold())]
st.caption(f"{len(filtered)} de {len(PROJECTS)} experiencias")
cards = []
for index, p in filtered:
    cards.append(
        '<article class="aurora-project">'
        f'<div class="aurora-cover"><img src="{image_data(p["image"])}" alt="" loading="lazy"><span class="aurora-cover-index">{index:02d}</span></div>'
        f'<div class="aurora-project-body"><p class="aurora-project-tag">{escape(p["category"])}</p>'
        f'<h3>{escape(p["title"])}</h3><p class="aurora-project-description">{escape(p["description"])}</p>'
        f'<p class="aurora-project-flow">{escape(p["technology"])}</p>'
        f'<div class="aurora-project-links"><a href="{escape(p["url"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Abrir {escape(p["title"], quote=True)}">Abrir aplicación ↗</a>'
        f'<a href="{escape(p["repo"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Ver código de {escape(p["title"], quote=True)}">Código ↗</a></div></div></article>'
    )
if cards:
    st.markdown('<div class="aurora-project-grid">' + "".join(cards) + '</div>', unsafe_allow_html=True)
else:
    st.info("No hay coincidencias. Prueba otro término o selecciona Todas las modalidades.")

section("02", "Dentro de cada experiencia", "Objetivo · Entrada · Resultado · Límites")
selected = st.selectbox("Consulta la ficha de una app", [p["title"] for p in PROJECTS])
project = next(p for p in PROJECTS if p["title"] == selected)
project_context(project)
st.markdown(f'[Abrir {project["title"]} ↗]({project["url"]}) · [Ver repositorio ↗]({project["repo"]})')
st.caption("Las fichas describen el funcionamiento de las apps. Las portadas son ilustraciones; no representan capturas de resultados.")

if pending:
    st.markdown(f'<aside class="aurora-pending"><strong>Colección en construcción</strong><br>Faltan {pending} experiencias para completar las {TARGET_COUNT}. Se incorporarán con sus propios repositorios y enlaces de despliegue.</aside>', unsafe_allow_html=True)
st.markdown('<aside class="aurora-resource"><div><h3>El proceso de aprendizaje</h3><p>Exploraciones de reconocimiento, transformación de información e interacción multimodal.</p></div><a href="https://sites.google.com/view/interfacesmultimodales/p%C3%A1gina-principal" target="_blank" rel="noopener noreferrer">Material de la clase ↗</a></aside>', unsafe_allow_html=True)
footer("APRENDER / EXPLORAR / CONSTRUIR")
