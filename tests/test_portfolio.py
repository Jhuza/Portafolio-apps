from html.parser import HTMLParser
from pathlib import Path
from streamlit.testing.v1 import AppTest


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.cards = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "a":
            self.links.append(values.get("href"))
        if tag == "article":
            self.cards += 1


def test_nine_projects_resources_and_current_app_links():
    app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "Intro.py")).run(timeout=30)
    assert not app.exception
    html = "\n".join(item.value for item in app.markdown)
    parser = Links()
    parser.feed(html)
    assert parser.cards == 9
    expected = {
        "https://chatpdf-fgtvnhpsz5z4sanjbpjpcu.streamlit.app/",
        "https://visionapp-bacpk6abduty44a9am9lc2.streamlit.app/",
        "https://imultimod.streamlit.app/", "https://traductorw.streamlit.app/",
        "https://yolov5cmc.streamlit.app/", "https://dataagente.streamlit.app/",
        "https://xn3pg24ztuv6fdiqon8qn3.streamlit.app/",
        "https://transcript-whisper.streamlit.app/", "https://vision2-gpt4o.streamlit.app/",
        "https://sites.google.com/view/aplicacionesdeia/inicio",
        "https://github.com/Jhuza/chat_pdf", "https://github.com/Jhuza/vision_app",
    }
    assert expected.issubset(set(parser.links))
    assert "chatpdf-cc.streamlit.app" not in html
