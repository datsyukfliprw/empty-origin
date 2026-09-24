#!/usr/bin/env python3
"""Trace the supplied reference's ink into a native SVG, without invented strokes.

The sample is a phone screenshot, not the original artwork. Preserve its visible
ink silhouette, suppress the paper tone, and exclude only the central numeral.
Each SVG pixel run comes directly from the supplied image, at its native resolution.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'layout_sample.jpeg'
OUTPUT = HERE / 'assets/aperture_from_reference.svg'
# Screenshot coordinates; excludes chapter title and all phone UI.
CROP = (197, 325, 510, 620)
CENTER = (353, 483)
NUMERAL_RADIUS = 76


def main():
    source = Image.open(SOURCE).convert('L')
    pixels = source.load()
    x0, y0, x1, y1 = CROP
    width, height = x1-x0, y1-y0
    paths = {level: [] for level in range(1, 9)}
    count = 0
    def level_at(x, y):
        if (x-CENTER[0])**2+(y-CENTER[1])**2 < NUMERAL_RADIUS**2:
            return 0
        # Background paper is approximately 220–240. Ignore light paper/noise;
        # retain the screenshot's dark ink and antialiased edge pixels.
        value = pixels[x, y]
        if value >= 185:
            return 0
        return min(8, max(1, round((210-value)/190*8)))
    for y in range(y0, y1):
        x = x0
        while x < x1:
            level = level_at(x,y)
            start = x
            x += 1
            while x < x1 and level_at(x,y) == level:
                x += 1
            if level:
                count += x-start
                paths[level].append(f'M{start-x0} {y-y0}h{x-start}v1h-{x-start}z')
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}">',
             '<!-- Traced from layout_sample.jpeg; original irregular ink, no generated geometry. -->']
    for level, segments in paths.items():
        gray = round(255*(1-level/8))
        lines.append(f'<path fill="#{gray:02x}{gray:02x}{gray:02x}" d="{" ".join(segments)}"/>')
    lines.append('</svg>')
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text('\n'.join(lines)+'\n')
    # The Scribus starter must not retain the rejected simplified substitute.
    (HERE/'EMPTY_ORIGIN_SCRIBUS_MASTER_KIT/assets/aperture_ring.svg').write_bytes(OUTPUT.read_bytes())
    metadata = {'source':str(SOURCE.relative_to(HERE.parents[1])),
                'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                'crop_pixels':CROP,'circle_center_pixels':CENTER,
                'numeral_exclusion_radius_pixels':NUMERAL_RADIUS,
                'source_ink_pixels_preserved':count,
                'output_sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                'method':'Direct native-resolution ink trace, eight gray levels; no generated strokes',
                'limitation':'The screenshot is the available source; vector paths preserve its pixel detail, not unavailable original detail.'}
    OUTPUT.with_suffix('.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(OUTPUT)

if __name__ == '__main__':
    main()
