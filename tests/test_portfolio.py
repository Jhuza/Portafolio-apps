from html.parser import HTMLParser
from pathlib import Path
import sys
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from projects import PROJECTS, TARGET_COUNT


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a": self.links.append(values.get("href"))
        if tag == "article": self.cards += 1


def parsed(app):
    assert not app.exception
    parser = Links()
    parser.feed("\n".join(item.value for item in app.markdown))
    return parser


def test_own_apps_and_code_links_include_the_integrated_board():
    app = AppTest.from_file(str(ROOT / "Intro.py")).run(timeout=30)
    page = parsed(app)
    assert len(PROJECTS) == len({p['url'] for p in PROJECTS}) == 18
    assert page.cards == len(PROJECTS)
    assert TARGET_COUNT == 18
    assert sum(p['slug']=='tablero' for p in PROJECTS) == 1
    assert all(p['url'] in page.links and p['repo'] in page.links for p in PROJECTS)
    assert all(p['repo'].startswith('https://github.com/Jhuza/') for p in PROJECTS)
    assert not any(url in page.links for url in ('https://imultimod.streamlit.app/', 'https://yolov5cmc.streamlit.app/'))


def test_filters_search_empty_state_and_project_detail():
    app = AppTest.from_file(str(ROOT / "Intro.py")).run(timeout=30)
    app.selectbox[0].select('IoT').run()
    assert parsed(app).cards == 3
    app.selectbox[0].select('Todas').run()
    app.text_input[0].set_value('OCR').run()
    assert parsed(app).cards == 2
    app.text_input[0].set_value('sin coincidencias 123').run()
    assert parsed(app).cards == 0
    assert any('No hay coincidencias' in info.value for info in app.info)
    app.selectbox[1].select('Monitor de sensores').run()
    assert not app.exception
    assert any('cinco segundos' in info.value for info in app.info)
