from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import sys
import numpy as np
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


def test_board_controls_and_export_only_with_drawing():
    canvas=SimpleNamespace(image_data=np.zeros((320,320,4),dtype=np.uint8),json_data={'objects':[]})
    with patch('streamlit_drawable_canvas.st_canvas',return_value=canvas) as component:
        app=AppTest.from_file(str(ROOT/'pages/18_Tablero.py')).run(timeout=30)
        assert not app.exception and not app.get('download_button')
        app.selectbox[0].select('Rectángulo').run()
        app.slider[0].set_value(12).run()
        app.checkbox[0].check().run()
        assert component.call_args.kwargs['drawing_mode']=='rect'
        assert component.call_args.kwargs['stroke_width']==12
        assert component.call_args.kwargs['fill_color']=='#FF8A4C'
        canvas.json_data['objects']=[{'type':'rect','width':20,'height':20}]
        canvas.image_data[10:30,10:30,:]=255
        app.run()
        assert not app.exception
        assert len(app.get('download_button'))==2
        assert any('1 objetos' in item.value for item in app.caption)
