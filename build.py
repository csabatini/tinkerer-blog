import os
import re

preamble = """Sitemap
=======

.. toctree::
    :hidden:

    404.rst

.. toctree::
    :maxdepth: 1


"""

years = []
posts = []

for d in os.listdir('.'):
    if re.match(r'\d{4}$', d):  # let's assume a 4-digit number is a year
        years.append(d)

for y in years:
    for p in os.walk(y):
        if p[1] == []:
            # build name, stripping .rst from filename
            for title in p[2]:
                posts.append(p[0] + '/' + title[:-4])


# sort posts alphabetically by the first character of their filename
posts = sorted(posts, key=lambda p: int(
    p[:4] + p[5:7] + p[8:10]), reverse=True)

try:
    os.remove('master.rst')
except OSError:
    pass
f = open('master.rst', 'w')

f.write(preamble)
for p in posts:
    f.write('    ' + p + '\n')

for page in sorted(os.listdir('pages')):
    f.write('    pages/' + page + '\n')
f.close()
