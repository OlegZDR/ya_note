"""Файл notes/tests/test_logic.py. YA_NOTE. Тестирование логики."""
from http import HTTPStatus

from django.db.utils import IntegrityError
from pytils.translit import slugify

from notes.models import Note
from .common_test import (
    TestNotesMain, NOTE_TITLE, NOTE_TEXT, url_add, url_done, form_data)


class TestNoteCreation(TestNotesMain):
    """Класс проверки создания заметки."""

    def test_user_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        notes_count_before = Note.objects.count()
        ids = list(Note.objects.values_list('id', flat=True))
        # Совершаем запрос через авторизованный клиент.
        response = self.auth_client.post(url_add, data=form_data)
        # Проверяем, что редирект привёл на страницу с заметкой.
        self.assertRedirects(response, url_done)
        # Считаем количество заметок.
        notes_count = Note.objects.count()
        # Убеждаемся, что есть одна заметка.
        self.assertEqual(notes_count - notes_count_before, 1)
        # Получаем объект заметки из базы.
        note_qs = Note.objects.exclude(id__in=ids)
        note = note_qs.first()
        # Проверяем, что все атрибуты заметки совпадают с ожидаемыми.
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        notes_count_before = Note.objects.count()
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом заметки.
        self.client.post(url_add, data=form_data)
        # Считаем количество комментариев.
        notes_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(notes_count - notes_count_before, 0)


class TestNoteEditDelete(TestNotesMain):
    """Класс проверки редактирования и удаления заметки."""

    def test_author_can_delete_note(self):
        """Автор может удалять заметки."""
        notes_count_before = Note.objects.count()
        # От имени автора комментария отправляем DELETE-запрос на удаление.
        response = self.auth_client.delete(self.delete_url)
        # Проверяем, что редирект привёл к разделу с комментариями.
        # Заодно проверим статус-коды ответов.
        self.assertRedirects(response, url_done)
        # Считаем количество комментариев в системе.
        note_count = Note.objects.count()
        # Ожидаем ноль комментариев в системе.
        self.assertEqual(notes_count_before - note_count, 1)

    def test_author_can_edit_comment(self):
        """Автор может редактировать заметки."""
        notes_count_before = Note.objects.count()
        # Выполняем запрос на редактирование от имени автора комментария.
        response = self.auth_client.post(self.edit_url, data=form_data)
        # Проверяем, что сработал редирект.
        self.assertRedirects(response, url_done)
        note_count = Note.objects.count()
        self.assertEqual(note_count - notes_count_before, 0)
        note = Note.objects.first()
        # Проверяем, что все атрибуты заметки совпадают с ожидаемыми.
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.author, self.author)

    def test_user_cant_delete_comment_of_another_user(self):
        """Неавтор не может удалять и редактировать заметки автора."""
        methods_url_and_data = (
            (self.reader_client.delete, self.delete_url, None),
            (self.reader_client.post, self.edit_url, form_data),
        )
        notes_count_before = Note.objects.count()
        # Выполняем запрос на удаление от пользователя-читателя.
        # response = self.reader_client.delete(self.delete_url)
        for client_method, url, data in methods_url_and_data:
            response = client_method(url, data=data)
        # Проверяем, что вернулась 404 ошибка.
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # Убедимся, что комментарий по-прежнему на месте.
        note_count = Note.objects.count()
        self.assertEqual(note_count - notes_count_before, 0)
        note = Note.objects.first()
        # Проверяем, что все атрибуты заметки совпадают с ожидаемыми.
        self.assertEqual(note.text, form_data['text'])
        self.assertEqual(note.title, form_data['title'])
        self.assertEqual(note.author, self.author)

    def test_not_create_two_nouts_with_equal_slugs(self):
        """Невозможно создать две заметки с одинаковыми slug."""
        # Создаём вторую заметку в БД.
        with self.assertRaises(IntegrityError,
                               msg='Ожидалось два одинаковых slug'):
            slug_old = self.note.slug
            Note.objects.create(
                title=f'{NOTE_TITLE} 2',
                text=f'{NOTE_TEXT} 2',
                author=self.author,
                slug=slug_old,
            )

    def test_slug_generated_automatically(self):
        """Slug формируется автоматически."""
        notes_count_before = Note.objects.count()
        ids = list(Note.objects.values_list('id', flat=True))
        form_data.pop('slug')
        response = self.auth_client.post(url_add, data=form_data)
        self.assertRedirects(response, url_done)
        note_count = Note.objects.count()
        # Проверяем, что даже без slug заметка была создана:
        self.assertEqual(note_count - notes_count_before, 1)
        # Получаем объект заметки из базы.
        note_qs = Note.objects.exclude(id__in=ids)
        note = note_qs.first()
        # Формируем ожидаемый slug:
        expected_slug = slugify(form_data['title'])
        self.assertEqual(note.slug, expected_slug)
