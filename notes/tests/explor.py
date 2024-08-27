

from django.test import Client, TestCase

class TestNotesMain(TestCase):

    @classmethod
    def setUpTestData(cls):
        ............

        

class TestDetailPage(TestNotesMain):

    @classmethod
    def setUpTestData(cls):
        ............

    def test_note_list_not_author(self):
        .................