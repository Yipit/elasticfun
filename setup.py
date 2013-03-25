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

from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name="elasticfun",
        license="GPL",
        version='0.0.1',
        description=u'ElasticSearch Query functionality using Django',
        long_description=open('README.md').read(),
        author=u'Lincoln de Sousa, Nitya Oberoi',
        author_email=u'lincoln@yipit.com, nitya@yipit.com',
        url='https://github.com/Yipit/elasticfun',
        include_package_data=True,
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
        )
    )
