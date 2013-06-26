# coding=utf-8
#
# $Id: $
#
# NAME:         seed.py
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
import datetime
import getpass


class SeedError(Exception): pass
class PreseedFileError(SeedError): pass
class OwnerError(SeedError): pass


class Seed(object):
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
        if preseed_file:
            self._file_path = preseed_file

        if autoload and preseed_file:
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

    def _file_exists(self, preseed_file=None):
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

    def to_text(self):
        """
        Converts the preseed data into text, exactly as you would find in a preseed file.

        :return: str containing the preseed data converted to text format

        """
        preseed_txt = ''

        for owner,question_data in self._data.iteritems():
            for question_name,(question_type,question_value) in sorted(question_data.iteritems()):
                preseed_txt += '%s %s %s %s\n' % (owner, question_name, question_type, question_value)

        return preseed_txt
    #---

    def load(self, preseed_file=None):
        """
        Loads a preseed file into the object

        :param preseed_file: Path to the preseed file to parse

        """
        if preseed_file:
            self._file_path = preseed_file

        self._file_exists(self._file_path)


        with open(preseed_file) as preseed_txt:
            for line in preseed_txt:
                if line.startswith('#') or line.startswith('\n'):   # Skip comments and blank lines
                    continue

                question_data = line.strip().split(None, 3)

                try:
                    owner, question_name, question_type, question_value = question_data
                except ValueError:
                    # Leaving the value blank is perfectly valid for some questions
                    owner, question_name, question_type = question_data
                    question_value = ''

                if owner in self._data:
                    self._data[owner].update({question_name: [question_type, question_value]})
                else:
                    self._data[owner] = {question_name: [question_type, question_value]}
    #---

    def save(self, preseed_file=None):
        """
        Saves the preseed data out to an actual file.

        :param preseed_file: The path to the preseed file to write
        :type preseed_file: str

        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        with open(preseed_file, 'w') as preseed_txt:
            preseed_txt.write('# Automatically generated with seedy.preseed on %s by %s\n#\n\n\n' %
                              (now, getpass.getuser()))
            preseed_txt.write(self.to_text())
    #---

    def find_questions_by_owner(self, owner, search, with_data = True):
        """
        Allows finding of questions in the preseed data.  This is VERY simple search, no wildcards just 'is search in
         key'.

        :param owner: The owner of the question
        :type owner: str
        :param search: String to match question keys on
        :type search: str
        :param with_data: Will return the full data of each matched question if ``True``
        :type with_data: bool

        :returns: If with_data is ``True``, a dict of the keys and their associated data
                    else
                    a list of keys which have the search string in them
        :raises: OwnerError

        """
        if owner not in self._data.keys():
            raise OwnerError("Owner '%s' not found" % owner)

        if with_data:
            return {question: data for question, data in self._data[owner].iteritems() if search in question}

        return [question for question in self._data[owner] if search in question]
    #---

    def find_questions(self, search, owner = None, with_data = True):
        """
        Searches for questions within the entire preseed file.  This method will search for matches in all owners'
        questions by default.

        :param owner: The owner of the question, defaults to all owners (``None``)
        :type owner: str
        :param search: String to match question keys on
        :type search: str
        :param with_data: Will return the full data of each matched question if ``True``
        :type with_data: bool

        :returns: dict containing matching questions and data, or if with_data is ``False`` only the questions.

        """
        return_values = {}

        if owner:
            return self.find_questions_by_owner(owner, search, with_data)

        for owner in self._data.iterkeys():
            questions = self.find_questions_by_owner(owner, search, with_data)
            if questions:
                return_values[owner] = questions

        return return_values
    #---
#---