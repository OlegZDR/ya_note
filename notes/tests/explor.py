

from django.test import Client, TestCase

class TestNotesMain(TestCase):

    @classmethod
    def setUpTestData(cls):
        ............


class TestDetailPage_1(TestNotesMain):

    @classmethod
    def setUpTestData(self):
        super().setUpTestData()
        ............

    def test_note_list_not_author(self):
        .................


class TestDetailPage_2(TestNotesMain):

    @classmethod
    def setUpTestData(self):
        super().setUpTestData()
        ............

    def test_note_list_author(self):
        .................