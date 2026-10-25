import unicodedata
from html import escape
import streamlit as st
from aurora import hero, project_context
from portfolio_ui import setup_portfolio, heading, portfolio_footer, icon, image_data, CATEGORY_ICONS, COURSE
from projects import PROJECTS, TARGET_COUNT

setup_portfolio()
hero('PORTAFOLIO DE INTERFACES MULTIMODALES', 'Distintas entradas.', 'Nuevas perspectivas.',
     'Texto, imágenes, voz y dispositivos. Un recorrido de aprendizaje a través de interfaces que reconocen, transforman y conectan.', kind='vision')
independent=sum(p['slug']!='tablero' for p in PROJECTS)
st.markdown(f'<div class="aurora-summary"><span><strong>{len(PROJECTS):02d}</strong> experiencias</span><span><strong>{independent:02d}</strong> apps independientes</span><span><strong>{len(PROJECTS)-independent:02d}</strong> tablero integrado</span></div>',unsafe_allow_html=True)

with st.sidebar:
    st.subheader('Sobre la colección')
    st.write('Portafolio académico de Juan José Hoyos. Ejercicios de Interfaces Multimodales del profesor Carlos Mario Correa, con diseño y adaptación propios.')
    st.markdown(f'[Material de la clase ↗]({COURSE})')
    st.markdown('[Guía visual Aurora ↗](https://github.com/Jhuza/Portafolio-apps/blob/main/docs/guia-visual-aurora.md)')
    st.caption('La disponibilidad de modelos, APIs, cámara y dispositivos se comprueba dentro de cada app.')


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFD',text.casefold()) if unicodedata.category(c)!='Mn')


def clear_filters():
    st.session_state['modality']='Todas'
    st.session_state['search']=''
    st.session_state['sort']='Orden de la colección'


heading('experiencias','01','Explora las experiencias','grid','Encuentra una herramienta. Prueba una idea.')
left,middle,right=st.columns([1,1.7,1.1])
with left:
    category=st.selectbox(':material/tune: Modalidad',['Todas']+sorted({p['category'] for p in PROJECTS}),key='modality')
with middle:
    query=st.text_input('Buscar una experiencia',placeholder='OCR, voz, sensores…',icon=':material/search:',key='search').strip()
with right:
    order=st.selectbox(':material/sort: Ordenar por',['Orden de la colección','Nombre A–Z','Modalidad'],key='sort')
filtered=[(index,p) for index,p in enumerate(PROJECTS,1)
          if (category=='Todas' or p['category']==category)
          and (not query or normalized(query) in normalized(' '.join(str(p[k]) for k in ('slug','title','description','technology','category'))))]
if order=='Nombre A–Z':
    filtered.sort(key=lambda pair:normalized(pair[1]['title']))
elif order=='Modalidad':
    filtered.sort(key=lambda pair:(pair[1]['category'],normalized(pair[1]['title'])))
result,reset=st.columns([3,1])
with result:
    scope=f' · {escape(category)}' if category!='Todas' else ''
    st.markdown(f'<p class="jhg-result-count" role="status">{len(filtered)} de {len(PROJECTS)} experiencias{scope}</p>',unsafe_allow_html=True)
with reset:
    st.button('Limpiar filtros',icon=':material/filter_alt_off:',on_click=clear_filters,disabled=category=='Todas' and not query and order=='Orden de la colección',use_container_width=True)

cards=[]
for index,p in filtered:
    symbol=CATEGORY_ICONS.get(p['category'],'spark')
    cards.append('<article class="aurora-project">'
        f'<div class="aurora-cover"><img src="{image_data(p["image"])}" alt="" loading="lazy" decoding="async" width="1659" height="948"><span class="aurora-cover-index">{index:02d}</span></div>'
        f'<div class="aurora-project-body"><p class="aurora-project-tag">{escape(p["category"])}</p>'
        f'<h3>{icon(symbol)}<span>{escape(p["title"])}</span></h3><p class="aurora-project-description">{escape(p["description"])}</p>'
        f'<p class="aurora-project-flow">{escape(p["technology"])}</p>'
        f'<div class="aurora-project-links"><a class="jhg-open" href="{escape(p["url"],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Abrir {escape(p["title"],quote=True)}">Abrir app {icon("arrow")}</a>'
        f'<a class="jhg-code" href="{escape(p["repo"],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Ver código de {escape(p["title"],quote=True)}">{icon("code")} Código</a></div></div></article>')
if cards:
    st.markdown('<div class="aurora-project-grid">'+''.join(cards)+'</div>',unsafe_allow_html=True)
else:
    st.info('No hay coincidencias. Prueba otro término o pulsa Limpiar filtros.',icon=':material/search_off:')

heading('fichas','02','Dentro de cada experiencia','file','Objetivo · Entrada · Resultado · Límites')
selected=st.selectbox(':material/info: Consulta la ficha de una app',[p['title'] for p in PROJECTS],key='detail')
project=next(p for p in PROJECTS if p['title']==selected)
project_context(project)
st.markdown(f'[Abrir {project["title"]} ↗]({project["url"]}) · [Ver repositorio ↗]({project["repo"]})')
st.caption('Cada portada es una ilustración de la función de la app, no una captura de resultados. Las fichas explican cómo utilizar y comprobar cada experiencia.')
pending=max(TARGET_COUNT-len(PROJECTS),0)
if pending:
    st.info(f'Faltan {pending} experiencias por incorporar a la colección.')
portfolio_footer()
