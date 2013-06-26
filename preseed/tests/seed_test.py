# coding=utf-8
#
# $Id: $
#
# NAME:         seed_test.py
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
#   Tests the preseed package's Seed class
#

import pytest
import mock
import os
import getpass

from preseed import seed


class Test___init__(object):
    """
    Tests the __init__ method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        reload(seed)
        seed.Seed.load = mock.MagicMock()

        self.file_path = '/tmp/some/preseed.file'
    #---

    def test_LoadsFileIfProvidedAndAutoLoadEnabled(self):
        """
        Tests that the initializer will load a provided preseed file if autoload is ``True``.

        """
        self.pfile = seed.Seed(self.file_path)
        self.pfile.load.assert_called_once_with(self.file_path)
    #---

    def test_DoesNotAttemptToLoadFileIfNotProvidedAndAutoLoadEnabled(self):
        """
        Tests that the initializer will not attempt to load a preseed file if none is provided, and if autoload is ``True``.

        """
        self.pfile = seed.Seed()

        desired_called = False
        assert self.pfile.load.called == desired_called
    #---

    def test_DoesNotAttemptToLoadFileIfProvidedAndAutoLoadDisabled(self):
        """
        Tests that the initializer will not attempt to load a preseed file if provided, and if autoload is ``False``.

        """
        self.pfile = seed.Seed(self.file_path, autoload=False)

        desired_called = False
        assert self.pfile.load.called == desired_called
    #---

    def test_SavesFilePathIfProvidedAndAutoLoadDisabled(self):
        """
        Tests that the initializer will save a provided preseed file path but not load it if autoload is ``False``.

        """
        self.pfile = seed.Seed(self.file_path, autoload=False)

        desired_called = False
        assert self.pfile.load.called == desired_called

        assert self.pfile._file_path == self.file_path
    #---
#---

class Test___getitem__(object):
    """
    Tests the __getitem__ method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.owner = 'd-i'
        self.test_key = 'pkgsel/include'
        self.preseed_data = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
            },

            'bob': {
                'barker': ['string', 'woof']
            }
        }

        self.pfile = seed.Seed()
        self.pfile._data = self.preseed_data.copy()
    #---

    def test_FetchesProperItemFromDict(self):
        """
        Tests that the method fetches the proper dictionary key + data from the _data dict.

        """
        assert self.pfile[self.owner] == self.preseed_data[self.owner]
    #---

    def test_ItemDataIsCorrect(self):
        """
        Tests that the data in the item that was fetched is as expected.

        """
        assert self.pfile[self.owner][self.test_key] == self.preseed_data[self.owner][self.test_key]
    #---

    def test_RaisesKeyErrorOnDNE(self):
        """
        Tests that if the key is does not exist in the dictionary, the method will raise KeyError

        """
        with pytest.raises(KeyError):
            no = self.pfile['pants']
    #---
#---

class Test__file_exists(object):
    """
    Tests the _file_exists method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.pfile = seed.Seed()
    #---

    def test_RaisesPreseedFileErrorIfFileDNE_Parameter(self):
        """
        Tests that the method raises PreseedFileError if the file does not exist.  This tests the method parameter.

        """
        with pytest.raises(seed.PreseedFileError):
            self.pfile._file_exists('/tmp/bob132413gb')
    #---

    def test_RaisesPreseedFileErrorIfFileDNE_Instance(self):
        """
        Tests that the method raises PreseedFileError if the file does not exist.  This tests the instance variable.

        """
        self.pfile._file_path = '/tmp/bob132413gb'
        with pytest.raises(seed.PreseedFileError):
            self.pfile._file_exists()
    #---

    def test_DoesNotRaiseErrorIfFileExists_Parameter(self):
        """
        Tests that the method does not raise an error if the file exists.  This tests the method parameter.

        """
        self.pfile._file_exists('/bin/sh')
    #---

    def test_DoesNotRaiseErrorIfFileExists_Instance(self):
        """
        Tests that the method does not raise an error if the file exists.  This tests the instance variable.

        """
        self.pfile._file_path = '/bin/sh'
        self.pfile._file_exists()
    #---

#---

class Test_to_text(object):
    """
    Tests the to_text method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.preseed_data = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
            }
        }
        self.preseed_string = 'd-i pkgsel/include string vim openssh-server python-pip python-software-properties salt-minion rng-tools\n' \
            'd-i pkgsel/language-packs multiselect \n' \
            'd-i pkgsel/update-policy select none\n' \
            'd-i pkgsel/updatedb boolean true\n' \
            'd-i pkgsel/upgrade select safe-upgrade\n'


        self.pfile = seed.Seed()
        self.pfile._data = self.preseed_data.copy()
    #---

    def test_ConvertsDataToString(self):
        """
        Tests that the method properly converts the preseed data to a string

        """
        preseed_text = self.pfile.to_text()
        assert preseed_text == self.preseed_string
    #---

#---

class Test_load(object):
    """
    Tests the load method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        reload(seed)    # Clears mocks that may exist from the last test

        self.preseed_fixture = '%s/fixtures/good_preseed.fixture' % os.path.dirname(__file__)
        self.bad_preseed_fixture = '%s/fixtures/bad_preseed.fixture' % os.path.dirname(__file__)

        self.pfile = seed.Seed()
    #---

    def test_ChecksForFileExistence(self):
        """
        Tests that the method checks to make sure the file exists

        """
        # seed = reload(seed)
        seed.Seed._file_exists = mock.MagicMock()

        self.pfile = seed.Seed()

        self.pfile.load(self.preseed_fixture)
        self.pfile._file_exists.assert_called_once_with(self.preseed_fixture)
    #---

    def test_RaisesValueErrorOnInvalidFormat(self):
        """
        Tests that the method will raise a ValueError when the preseed format is invalid

        """
        with pytest.raises(ValueError):
            self.pfile.load(self.bad_preseed_fixture)
    #---

    def test_IgnoresComments(self):
        """
        Tests that the method ignores lines prefixed with #

        """
        self.pfile.load(self.preseed_fixture)

        assert '#' not in self.pfile._data.keys()
    #---

    def test_IgnoresBlankLines(self):
        """
        Tests that the method ignores blank lines

        """
        self.pfile.load(self.preseed_fixture)

        assert '\n' not in self.pfile._data.keys()
    #---

    def test_LoadsOwners(self):
        """
        Tests that the method properly loads the question owners

        """
        owners = ['d-i', 'bob-barker']
        self.pfile.load(self.preseed_fixture)

        assert self.pfile._data.keys() == owners
    #---

    def test_LoadsQuestionNames(self):
        """
        Tests that the method properly loads the question names

        """
        questions = ['base-installer/kernel/image', 'debian-installer/exit/poweroff', 'console-setup/variantcode',]
        self.pfile.load(self.preseed_fixture)

        assert self.pfile._data['d-i'].keys() == questions
    #---

    def test_LoadsQuestionDataTypesAndData(self):
        """
        Tests that the method properly loads the question data types and data

        """
        question_data = [['string', 'andromeda node'], ['boolean', 'false'],  ['string', '']]
        self.pfile.load(self.preseed_fixture)

        assert self.pfile._data['d-i'].values() == question_data
    #---
#---

class Test_save(object):
    """
    Tests the save method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.test_file = '/tmp/preseed.test'
        self.preseed_data = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
            },
            'bob-barker': {
                'aquestion/yep': ['string', 'no']
            }
        }
        self.preseed_string = '#\n\n\n' \
            'd-i pkgsel/include string vim openssh-server python-pip python-software-properties salt-minion rng-tools\n' \
            'd-i pkgsel/language-packs multiselect \n' \
            'd-i pkgsel/update-policy select none\n' \
            'd-i pkgsel/updatedb boolean true\n' \
            'd-i pkgsel/upgrade select safe-upgrade\n' \
            'bob-barker aquestion/yep string no\n'

        self.pfile = seed.Seed()
        self.pfile._data = self.preseed_data
    #---

    def test_WritesCorrectText(self):
        """
        Tests

        """
        self.pfile.save(self.test_file)

        with open(self.test_file) as preseed_text:
            file_text = preseed_text.read()

        assert file_text.split('\n')[1:] == self.preseed_string.split('\n')

        os.remove(self.test_file)
    #---

#---

class Test_find_questions_by_owner(object):
    """
    Tests the find_questions_by_owner method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.preseed_data = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
                'partman-lvm/confirm': ['boolean', 'true'],
            }
        }
        self.filtered_dict = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
            }
        }
        self.filtered_list = ['pkgsel/include', 'pkgsel/language-packs', 'pkgsel/update-policy', 'pkgsel/updatedb', 'pkgsel/upgrade',]

        self.pfile = seed.Seed()
        self.pfile._data = self.preseed_data.copy()
    #---

    def test_ReturnsEmptyDictForNoMatches(self):
        """
        Tests that the method returns an empty dict when no matches are found.

        """
        questions = self.pfile.find_questions_by_owner('d-i', 'bob')
        assert questions == {}
    #---

    def test_ReturnsEmptyListForNoMatches_WithIncludeDataFalse(self):
        """
        Tests that the method returns an empty list if no matches are found and include_data is set to ``False``.

        """
        questions = self.pfile.find_questions_by_owner('d-i', 'bob', with_data=False)
        assert questions == []
    #---

    def test_ReturnsPopulatedDictIfMatches(self):
        """
        Tests that the method will return a dict in the following format for questions that match the criteria:
            {
                'owner': {
                    'question': ['type', 'value']
                }
            }

        """
        questions = self.pfile.find_questions_by_owner('d-i', 'pkgsel')
        assert questions == self.filtered_dict['d-i']
    #---

    def test_ReturnsPopulatedListIfMatches_WithIncludeDataFalse(self):
        """
        Tests that the method will return a list of only question names if there are matches and include_data is `
        `False``.

        """
        questions = self.pfile.find_questions_by_owner('d-i', 'pkgsel', with_data=False)
        assert sorted(questions) == sorted(self.filtered_list)
    #---

    def test_RaisesOwnerErrorForNonExistentOwners(self):
        """
        Tests that the method will raise an error for owners that do not exist.

        """
        with pytest.raises(seed.OwnerError):
            self.pfile.find_questions_by_owner('bob', '')
    #---
#---

class Test_find_questions(object):
    """
    Tests the find_questions method

    """
    def setup_method(self, method):
        """
        Test setup

        """
        self.preseed_data = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
                'partman-lvm/confirm': ['boolean', 'true'],
            },
            'bob-barker': {
                'aquestion/yep': ['string', 'no'],
                'pkgsel/upgrade': ['select', 'wat'],
            }
        }
        self.owner_filtered_dict = {
            'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
            'pkgsel/language-packs': ['multiselect', ''],
            'pkgsel/update-policy': ['select', 'none'],
            'pkgsel/updatedb': ['boolean', 'true'],
            'pkgsel/upgrade': ['select', 'safe-upgrade'],
        }
        self.filtered_dict = {
            'd-i': {
                'pkgsel/include': ['string', 'vim openssh-server python-pip python-software-properties salt-minion rng-tools'],
                'pkgsel/language-packs': ['multiselect', ''],
                'pkgsel/update-policy': ['select', 'none'],
                'pkgsel/updatedb': ['boolean', 'true'],
                'pkgsel/upgrade': ['select', 'safe-upgrade'],
            },
            'bob-barker': {
                'pkgsel/upgrade': ['select', 'wat'],
            }
        }
        self.filtered_list = ['pkgsel/include', 'pkgsel/language-packs', 'pkgsel/update-policy', 'pkgsel/updatedb', 'pkgsel/upgrade',]

        self.pfile = seed.Seed()
        self.pfile._data = self.preseed_data
    #---

    def test_ReturnsSingleOwnerDataWhenOwnerIsSpecified(self):
        """
        Tests that the method

        """
        filtered_questions = self.pfile.find_questions('pkgsel', 'd-i')

        assert filtered_questions == self.owner_filtered_dict
    #---

    def test_RaisesOwnerErrorForInvalidOwner(self):
        """
        Tests that the method raises OwnerError for an invalid owner

        """
        with pytest.raises(seed.OwnerError):
            self.pfile.find_questions('', 'pants')
    #---

    def test_ReturnsAllMatchingQuestionsForAllOwnersIfOwnerNotSet(self):
        """
        Tests that the method returns all questions that match for all owners, provided owner is not set.

        """
        filtered_questions = self.pfile.find_questions('pkgsel')

        assert filtered_questions == self.filtered_dict
    #---

    def test_ReturnsAnEmptyDictIfNoMatches(self):
        """
        Tests that the method returns an empty dict if there are no matches

        """
        filtered_questions = self.pfile.find_questions('asdfg24')

        assert filtered_questions == {}
    #---
#---