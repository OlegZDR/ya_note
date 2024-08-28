"""Файл news/tests/test_content.py."""
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse_lazy

from notes.models import Note


User = get_user_model()

list_url = reverse_lazy('notes:list', None)
url_add = reverse_lazy('notes:add', None)
url_done = reverse_lazy('notes:success', None)
url_home = reverse_lazy('notes:home', None)
url_login = reverse_lazy('users:login', None)
url_logout = reverse_lazy('users:logout', None)
url_signup = reverse_lazy('users:signup', None)

NOTE_TITLE = 'Заголовок'
NOTE_TEXT = 'Текст'
NOTE_SLUG = 'zagzag'
NEW_NOTE_TEXT = 'Новый текст'

form_data = {
    'title': NOTE_TITLE,
    'text': NOTE_TEXT,
    'slug': NOTE_SLUG
}


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
                                       author=cls.author, slug='zag')
        cls.edit_url = reverse_lazy('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse_lazy('notes:delete', args=(cls.note.slug,))
        cls.detail_url = reverse_lazy('notes:detail', args=(cls.note.slug,))
