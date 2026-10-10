#!/usr/bin/env python3
"""Text preview of a PNG (or PDF page via pdftoppm) for layout sanity checks when image viewing is unavailable.
usage: python3 tools/qa-ascii.py <cols> <file.png|file.pdf> [page]"""
import sys, subprocess, tempfile, os
from PIL import Image; import numpy as np
cols = int(sys.argv[1]); src = sys.argv[2]; page = int(sys.argv[3]) if len(sys.argv) > 3 else 1
if src.lower().endswith('.pdf'):
    tmp = tempfile.mkdtemp(); subprocess.run(['pdftoppm','-png','-r','40','-f',str(page),'-l',str(page),src,os.path.join(tmp,'p')],check=True)
    src = os.path.join(tmp, sorted(os.listdir(tmp))[0])
im = Image.open(src).convert('RGBA'); W,H = im.size; rows = max(1,int(H/W*cols*0.5))
a = np.array(im.resize((cols,rows)))
print(f"--- {src} {W}x{H}")
for y in range(rows):
    line=''
    for x in range(cols):
        r,g,b,al = a[y,x]
        if al<60: line+=' '
        elif r>170 and g<110 and b<110: line+='R'
        elif r>235 and g>235 and b>230: line+=' '      # white/off-white paper
        elif r>200 and g>200 and b>200: line+='.'      # light grey
        elif r<60 and g<60 and b<60: line+='K'
        elif abs(int(r)-int(g))<30 and g>=r and r<170: line+='#'  # sage / ink
        else: line+='+'
    print(line)
