#  SPDX-License-Identifier: GPL-3.0+
#
# Copyright © 2020 T. Beck.
#
# This file is part of CBSplot.
#
# CBSplot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CBSplot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CBSplot.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

setup(
        name='CBSplot',
        version='0.2.1',
        description='Plot routine for cbsmodel',
        url='http://github.com/TB-IKP/CBSplot',
        author='Tobias Beck',
        author_email='tbeck@ikp.tu-darmstadt.de',
        #license=None,
        python_requires='>=3',
        packages=['CBSplot'],
        install_requires=['numpy','matplotlib','uncertainties'],
)
