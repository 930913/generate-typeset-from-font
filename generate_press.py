#!/usr/bin/env python

from subprocess import Popen
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
import string

font = TTFont('/usr/share/fonts/truetype/freefont/FreeSerif.ttf')

cmap = font['cmap']
t = cmap.getcmap(3,1).cmap
s = font.getGlyphSet()
units_per_em = font['head'].unitsPerEm

def getTextWidth(text,pointSize):
   total = 0
   for c in text:
       if ord(c) in t and t[ord(c)] in s:
           total += s[t[ord(c)]].width
       else:
           total += s['.notdef'].width
   total = total*float(pointSize)/units_per_em;
   return total * 1.5

def generate_openscad_script():
  return """$fa = 1;
$fs = 0.4;

scale([-1, 1, 1]) {
    rotate([0, 0, 90])
    translate([0.2, -7, 7 - 0.001])

    linear_extrude(height = 0.5) {

        text(letter, halign = "left", valign = "baseline", font = "Free  Serif", size = 7);
    }

    difference() {
        cube([10, width, 7]);

        rotate([90, 0, 0])
        translate([10.5, 2, -10])
        cylinder(h=20, r=1);
    }
}"""

def generate_type(letter, filename=None):
  Popen(['openscad', '-o', '{}.stl'.format(filename or letter), '-D', 'letter="{}"'.format(letter), '-D', 'width={}'.format(getTextWidth(letter, 7)), '/tmp/generate_type.scad'])

if __name__=='__main__':
    with open('/tmp/generate_type.scad', 'w') as fp:
      fp.write(generate_openscad_script())

    for letter in string.ascii_letters:
      print('Generating {}'.format(letter))
      generate_type(letter)

    generate_type(' ', 'space')
