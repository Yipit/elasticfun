# elasticfun - Copyright (c) 2013  Yipit, Inc
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import os
from setuptools import setup, find_packages


def parse_requirements():
    """Rudimentary parser for the `requirements.txt` file

    We just want to separate regular packages from links to pass them to the
    `install_requires` and `dependency_links` params of the `setup()`
    function properly.
    """
    try:
        requirements = \
            map(str.strip, local_file('requirements.txt'))
    except IOError:
        raise RuntimeError("Couldn't find the `requirements.txt' file :(")

    links = []
    pkgs = []
    for req in requirements:
        if not req:
            continue
        if 'http:' in req or 'https:' in req:
            links.append(req)
            name, version = re.findall("\#egg=([^\-]+)-(.+$)", req)[0]
            pkgs.append('{0}=={1}'.format(name, version))
        else:
            pkgs.append(req)

    return pkgs, links

local_file = lambda f: \
    open(os.path.join(os.path.dirname(__file__), f)).readlines()

install_requires, dependency_links = parse_requirements()

if __name__ == '__main__':

    setup(
        name="elasticfun",
        license="GPL",
        version='0.3.2',
        description=u'ElasticSearch Query functionality using Django',
        long_description=open('README.md').read(),
        author=u'Lincoln de Sousa, Nitya Oberoi',
        author_email=u'lincoln@yipit.com, nitya@yipit.com',
        url='https://github.com/Yipit/elasticfun',
        packages=find_packages(exclude=['*tests*']),
        install_requires=install_requires,
        dependency_links=dependency_links,
        classifiers=(
            'Development Status :: 3 - Alpha',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Operating System :: Microsoft',
            'Operating System :: POSIX',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
        )
    )
