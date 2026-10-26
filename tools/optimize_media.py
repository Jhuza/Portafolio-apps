from pathlib import Path
import json
import subprocess
from PIL import Image
import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root/'projects.json').read_text(encoding='utf-8'))
before = after = 0
for project in catalog:
    original = root/project['image'].replace('-960.webp', '.png')
    before += original.stat().st_size
    with Image.open(original) as source:
        for width in (640, 960):
            target = original.with_name(original.stem+f'-{width}.webp')
            size = (width, round(source.height*width/source.width))
            source.convert('RGB').resize(size, Image.Resampling.LANCZOS).save(target, 'WEBP', quality=82, method=6)
            if width == 960: after += target.stat().st_size
    project['image'] = original.with_name(original.stem+'-960.webp').relative_to(root).as_posix()
    project['image_small'] = original.with_name(original.stem+'-640.webp').relative_to(root).as_posix()
(root/'projects.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for name in ('closed', 'open'):
    with Image.open(root/f'static/hero/{name}.jpg') as image:
        image.save(root/f'static/hero/{name}.webp', 'WEBP', quality=86, method=6)
source = root/'assets/hero/jhg-unlock.mp4'
target = root/'assets/hero/jhg-unlock-scroll.mp4'
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-i', str(source), '-an',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-pix_fmt', 'yuv420p',
                '-g', '6', '-keyint_min', '6', '-sc_threshold', '0', '-bf', '0',
                '-movflags', '+faststart', str(target)], check=True, capture_output=True)
print(json.dumps({'covers_original': before, 'covers_960_webp': after,
                  'video_original': source.stat().st_size, 'video_scroll': target.stat().st_size}))

