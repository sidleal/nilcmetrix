# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals, division
from importlib import import_module


class Config(dict):

    """A class for storing configuration parameters. """

    def __init__(self, auto_load=True):
        """Form a config object. If the current directory includes a config.py
        file, it will be automatically loaded if auto_load is True.
        """
        if auto_load:
            try:
                self.from_object('config')
            except ImportError:
                pass

    def from_object(self, module_name):
        """Load a configuration from a module name.

        :module_name: The name of the module where the parameters are defined.
        """
        m = import_module(module_name)

        for var in dir(m):
            if var.isupper():
                self[var] = getattr(m, var)


config = Config()
