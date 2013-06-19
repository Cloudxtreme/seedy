# coding=utf-8
#
# $Id: $
#
# NAME:         file.py
#
# AUTHOR:       Nick Whalen <nickw@mindstorm-networks.net>
# COPYRIGHT:    2013 by Nick Whalen
# LICENSE:
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# DESCRIPTION:
#   Preseed file management
#

import os


class FileError(Exception): pass
class PreseedFileError(FileError): pass


class File(object):
    """
    Encapsulates a preseed file.

    """
    _name = None
    _description = None
    _data = {}
    _file_path = None

    def __init__(self, preseed_file=None, autoload=True):
        """
        Constructor

        """
        if self._file_exists(preseed_file) and autoload:
            self._file_path = preseed_file
            self.load(preseed_file)
    #---

    def __getitem__(self, item):
        """
        Makes the class behave like a dict

        :param item: Item to look up in _data

        :return: Python object
        """
        if item in self._data:
            return self._data[item]
        else:
            raise KeyError(item)
    #---

    def _file_exists(self, preseed_file):
        """
        Validate that the file path stored in the class or passed as an arg is valid

        :param preseed_file: Path to the preseed file

        """
        if not self._file_path:
            if preseed_file and not os.path.exists(preseed_file):
                raise PreseedFileError('Invalid preseed file path: %s' % preseed_file)

        elif not os.path.exists(self._file_path):
            raise PreseedFileError('Invalid preseed file path: %s' % preseed_file)
    #---

    def load(self, preseed_file=None):
        """
        Loads a preseed file into the object

        :param preseed_file: Path to the preseed file to parse

        """
        self._file_exists(preseed_file)

        with open(preseed_file) as preseed_txt:
            for line in preseed_txt:
                owner, question_name, question_type, question_value = line.split(' ', 3)

                self._data[owner][question_name] = [question_type, question_value]

    #---

    def save(self, preseed_file=None):
        """
        Saves the preseed data out to an actual file.

        """

        for owner,question_data in self._data.items():
            for question_name,(question_type,question_value) in question_data.items():
                line = '%s %s %s %s' % (owner, question_name, question_type, question_value)

        with open(preseed_file, 'w') as preseed_txt:
            preseed_txt.write('%s %s %(question_type)s %(question_value)s\n' % (owner, question_data))
    #---

#---