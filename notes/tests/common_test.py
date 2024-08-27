"""Файл news/tests/test_content.py."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()

list_url = reverse('notes:list', None)
url_add = reverse('notes:add', None)
url_done = reverse('notes:success', None)
url_home = reverse('notes:home', None)
url_login = reverse('users:login', None)
url_logout = reverse('users:logout', None)
url_signup = reverse('users:signup', None)

NOTE_TITLE = 'Заголовок'
NOTE_TEXT = 'Текст'
NOTE_SLUG = 'zagolovok'
NEW_NOTE_TEXT = 'Новый текст'

form_data = {'title': NOTE_TITLE, 'text': NOTE_TEXT}


class TestNotesMain(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Читатель Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель Неавтор')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(title=NOTE_TITLE, text=NOTE_TEXT,
                                       author=cls.author, slug='zagolovok')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))







        #cls.url_edit = reverse('notes:edit', (cls.note.slug,))
        #cls.url_delite = reverse('notes:delete', (cls.note.slug,))
        #cls.url_detail = reverse('notes:detail', (cls.note.slug,))
