"""Keep delivered artwork responsive and within the portfolio's transfer budget."""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]


def test_card_assets_have_responsive_variants_and_a_transfer_budget():
    projects = json.loads((ROOT/'projects.json').read_text(encoding='utf-8'))
    large_total = 0
    for project in projects:
        for key, width in (('image_small', 640), ('image', 960)):
            path = ROOT/project[key]
            with Image.open(path) as image:
                assert image.format == 'WEBP'
                assert image.width == width
                assert abs(image.width/image.height - 1.75) < 0.01
        large_total += (ROOT/project['image']).stat().st_size
    assert large_total < 1_500_000
    assert (ROOT/'assets/hero/jhg-unlock-scroll.mp4').stat().st_size < 2_000_000
