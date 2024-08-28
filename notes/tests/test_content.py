"""Файл news/tests/test_content.py."""
from notes.models import Note
from notes.forms import NoteForm
from .common_test import TestNotesMain, list_url, url_add


class TestDetailPage(TestNotesMain):

    def test_note_list_not_author(self):
        """Заметка неавтора не передается на страницу автора с списком."""
        response = self.auth_client.get(list_url)
        note_count = Note.objects.count()
        # Проверяем, что объект новости находится в словаре контекста
        self.assertIn(self.note, response.context['object_list'])
        self.assertEqual(1, note_count)

    def test_note_list_author(self):
        """Заметка автора передается на его страницу с списком"""
        response = self.auth_client.get(list_url)
        # Проверяем, что объект новости находится в словаре контекста
        self.assertIn(self.note, response.context['object_list'])

    def test_authorized_client_has_form(self):
        """Формы передаются на страницы создания и редактирования заметки"""
        # Авторизуем клиент при помощи ранее созданного пользователя.
        urls = (
            self.edit_url,
            url_add,
        )
        for url in urls:
            with self.subTest(user=self.author, url=url):
                response = self.auth_client.get(url)
                self.assertIn('form', response.context)
                # Проверим, что объект формы соответствует нужному
                # классу формы.
                self.assertIsInstance(response.context['form'], NoteForm)
