from django.shortcuts import render
import rollbar
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def test_rollbar(request):
    rollbar.report_message('Тест Rollbar из Django', 'info')
    return HttpResponse('Сообщение отправлено в Rollbar')


def test_error(request):
    raise ValueError('Тестовая ошибка для Rollbar')