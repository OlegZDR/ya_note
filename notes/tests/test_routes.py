"""Файл notes/tests/test_routes.py. YA_NOTE. Тесты маршрутов."""
from http import HTTPStatus

from .common_test import (
    TestNotesMain, url_home, url_login, url_logout, url_signup, url_add,
    url_done, list_url
)


class TestRoutes(TestNotesMain):

    def test_pages_availability(self):
        """Доступность страниц для просмотра, редактирования и удаления."""
        urls = (
            (url_home, self.client, HTTPStatus.OK),
            (url_login, self.client, HTTPStatus.OK),
            (url_logout, self.client, HTTPStatus.OK),
            (url_signup, self.client, HTTPStatus.OK),
            (url_add, self.reader_client, HTTPStatus.OK),
            (url_done, self.reader_client, HTTPStatus.OK),
            (list_url, self.reader_client, HTTPStatus.OK),
            (self.edit_url, self.auth_client, HTTPStatus.OK),
            (self.delete_url, self.auth_client, HTTPStatus.OK),
            (self.detail_url, self.auth_client, HTTPStatus.OK),
            (self.edit_url, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.delete_url, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.detail_url, self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for url, user_client, status in urls:
            with self.subTest(url=url, user_client=user_client):
                response = user_client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка редиректов."""
        urls = (
            self.edit_url,
            self.delete_url,
            self.detail_url,
            url_add,
            url_done,
            list_url,
        )
        for url in urls:
            with self.subTest(url=url):
                # Получаем ожидаемый адрес страницы логина,
                # на который будет перенаправлен пользователь.
                # Учитываем, что в адресе будет параметр next, в котором
                # передаётся адрес страницы, с которой пользователь был
                # переадресован.
                redirect_url = f'{url_login}?next={url}'
                response = self.client.get(url)
                # Проверяем, что редирект приведёт именно на указанную ссылку.
                self.assertRedirects(response, redirect_url)
