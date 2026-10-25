"""Portfolio identity, navigation and accessible decorative icons."""
import base64
from html import escape
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
SITE = 'https://jhginterfacesmultimodalesportfolio.streamlit.app/'
COURSE = 'https://sites.google.com/view/interfacesmultimodales/p%C3%A1gina-principal'
CODE = 'https://github.com/Jhuza/Portafolio-apps'
PATHS = {
    'grid': '<rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/>',
    'file': '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z M14 3v6h6 M8 13h8 M8 17h5"/>',
    'image': '<rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8" cy="8" r="1.5"/><path d="m3 17 5-5 4 4 4-6 5 7"/>',
    'text': '<path d="M4 5h16 M12 5v15 M8 20h8 M4 5v3 M20 5v3"/>',
    'audio': '<path d="M3 10v4 M7 6v12 M11 3v18 M15 7v10 M19 5v14 M23 10v4"/>',
    'draw': '<path d="m4 15 11-11a2.8 2.8 0 0 1 4 4L8 19l-5 2z M13 6l5 5 M3 21h18"/>',
    'signal': '<path d="M3 8a14 14 0 0 1 18 0 M6 12a9 9 0 0 1 12 0 M9 16a4 4 0 0 1 6 0"/><circle cx="12" cy="20" r="1"/>',
    'arrow': '<path d="M7 17 17 7 M7 7h10v10"/>',
    'code': '<path d="m8 6-6 6 6 6 M16 6l6 6-6 6 M14 3l-4 18"/>',
    'book': '<path d="M12 5v16 M12 5C8 2 4 3 2 4v15c4-2 7-1 10 2 3-3 6-4 10-2V4c-2-1-6-2-10 1z"/>',
    'filter': '<path d="M4 7h16 M4 17h16"/><circle cx="9" cy="7" r="3" fill="#0d1420"/><circle cx="15" cy="17" r="3" fill="#0d1420"/>',
    'spark': '<path d="m12 2 3 7 7 3-7 3-3 7-3-7-7-3 7-3z"/>',
}
CATEGORY_ICONS = {'Documentos':'file','Imagen':'image','Visión':'image','Texto':'text','Audio':'audio','Dibujo':'draw','IoT':'signal'}


def image_data(filename):
    path=ROOT/filename
    if filename.startswith('static/'):
        return 'app/'+filename
    mime={'.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg'}[path.suffix.lower()]
    return f'data:{mime};base64,'+base64.b64encode(path.read_bytes()).decode('ascii')


def icon(name):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ABCFFF" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{PATHS.get(name,PATHS["spark"])}</svg>'
    data=base64.b64encode(svg.encode()).decode('ascii')
    return f'<img class="jhg-icon" src="data:image/svg+xml;base64,{data}" alt="" aria-hidden="true" width="20" height="20">'


def setup_portfolio(title='Interfaces multimodales', sidebar='collapsed', home=True):
    st.set_page_config(page_title=f'{title} · JHG',page_icon=str(ROOT/'assets/LogoJHGwhite.png'),layout='wide',initial_sidebar_state=sidebar)
    css=(ROOT/'aurora.css').read_text(encoding='utf-8')+'\n'+(ROOT/'portfolio.css').read_text(encoding='utf-8')
    st.markdown(f'<style>{css}</style>',unsafe_allow_html=True)
    base='' if home else SITE
    st.markdown(f'<div class="jhg-header-slot" id="inicio"><header class="jhg-header"><a class="jhg-identity" href="{base}#inicio" target="_self" aria-label="JHG · Inicio"><img class="jhg-logo" src="{image_data("assets/LogoJHGwhite.png")}" alt="JHG"><span>JUAN JOSÉ HOYOS<small>INTERFACES MULTIMODALES</small></span></a><nav aria-label="Navegación del portafolio"><a href="{base}#experiencias" target="_self">{icon("grid")}Experiencias</a><a href="{base}#fichas" target="_self">{icon("file")}Fichas</a><a href="{COURSE}" target="_blank" rel="noopener noreferrer">{icon("book")}Aprendizaje {icon("arrow")}</a></nav></header></div>',unsafe_allow_html=True)


def heading(anchor, number, title, symbol, note=''):
    st.markdown(f'<section class="jhg-section" id="{anchor}"><div><span class="jhg-number">{number}</span>{icon(symbol)}<h2>{escape(title)}</h2></div><p>{escape(note)}</p></section>',unsafe_allow_html=True)


def portfolio_footer(home=True):
    base='' if home else SITE
    st.markdown(f'<footer class="jhg-footer"><div><a class="jhg-footer-brand" href="{base}#inicio" target="_self">JHG <span>/ LAB</span></a><p>Aprender, explorar y construir.<br>Juan José Hoyos · Interfaces Multimodales</p></div><nav aria-label="Índice del portafolio"><span class="jhg-footer-label">ÍNDICE</span><a href="{base}#experiencias" target="_self">Experiencias</a><a href="{base}#fichas" target="_self">Fichas de las apps</a><a href="{COURSE}" target="_blank" rel="noopener noreferrer">Proceso de aprendizaje {icon("arrow")}</a><a href="{CODE}" target="_blank" rel="noopener noreferrer">Código del portafolio {icon("code")}</a></nav><div class="jhg-footer-note"><span class="jhg-footer-label">ACERCA DE LA COLECCIÓN</span><p>Ejercicios de la clase de Carlos Mario Correa.<br>Diseño y adaptación: Juan José Hoyos.</p><a href="{base}#inicio" target="_self">Volver al inicio ↑</a></div></footer>',unsafe_allow_html=True)
    # Only trusted, repository-owned code is executed. No user input is interpolated.
    with st.container(key='portfolio_motion'):
        st.html('<script>'+(ROOT/'portfolio_motion.js').read_text(encoding='utf-8')+'</script>',unsafe_allow_javascript=True)
