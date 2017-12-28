import os
import re
from subprocess import Popen, PIPE

preamble = """Sitemap
=======

.. toctree::
    :hidden:

    404.rst

.. toctree::
    :maxdepth: 1


"""


def create_sitemap() -> None:
    """Generate the master.rst index of all pages and posts"""
    years = []
    posts = []
    for d in os.listdir('.'):
        # let's assume a 4-digit number is a year
        if re.match(r'\d{4}$', d):
            years.append(d)

    for y in years:
        for p in os.walk(y):
            if p[1] == []:
                # build name, stripping .rst from filename
                for title in p[2]:
                    posts.append(p[0] + '/' + title[:-4])

    # sort posts alphabetically
    posts = sorted(posts, key=lambda p: int(
        p[:4] + p[5:7] + p[8:10]), reverse=True)

    f = open('master.rst', 'w')

    f.write(preamble)
    for p in posts:
        f.write('    ' + p + '\n')

    for page in sorted(os.listdir('pages')):
        f.write('    pages/' + page + '\n')
    f.close()


def build_site() -> None:
    """Build the static site using tinkerer CLI"""
    with Popen(["tinker", "--build"], stdout=PIPE, bufsize=1,
               universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')


def fix_http_urls() -> None:
    """Replace HTTP urls in tinkerer's CSS with HTTPS"""
    with open('blog/html/_static/flat.css', 'r') as f:
        fixed_lines = [l.replace('http://', 'https://') for l in f]

    with open('blog/html/_static/flat.css', 'w') as f:
        f.write(''.join(fixed_lines))


if __name__ == '__main__':
    create_sitemap()
    build_site()
    fix_http_urls()
