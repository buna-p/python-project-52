# Менеджер задач (Task Manager)

 — веб-приложение для управления задачами. Позволяет создавать задачи, назначать исполнителей, управлять статусами и метками, а также фильтровать задачи по различным критериям.


### Hexlet tests and linter status:
[![Actions Status](https://github.com/buna-p/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/buna-p/python-project-52/actions)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=buna-p_python-project-83&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=buna-p_python-project-83)


**Демонстрационный сайт** https://python-project-52-eh0n.onrender.com

**Возможности:**

- Регистрация, аутентификация и управление профилем пользователя.
- Создание, просмотр, редактирование, фильтрация и удаление задач.
- Управление статусами задач (CRUD).
- Управление метками (CRUD) с возможностью прикрепления к задачам.
- Интеграция с Rollbar для отслеживания ошибок.

## Работа

**Установка:**
1. Клонируйте репозиторий командой *git clone*.
2. Установите пакет командой *make install*.
3. Настройте переменные окружения.
4. Примените миграции командой *make migrate*.
5. Запустите приложение командой *make dev*.
