# Простая реферальная система
Этот проект реализует простую реферальную систему с авторизацией по номеру телефона. Основные функции включают регистрацию пользователей, аутентификацию с помощью 4-значного кода, а также реферальную систему, где пользователи могут генерировать и использовать инвайт-коды. В этом README.md описаны функциональные возможности, API эндпоинты и инструкции по настройке.

## Основные возможности
* Авторизация по номеру телефона

  - Пользователь вводит свой номер телефона.
Имитация отправки 4-значного кода авторизации (задержка на сервере 1-2 секунды).
  - Пользователь вводит полученный код для завершения процесса входа.
  - Если пользователь новый, его данные записываются в базу данных.
- Профиль пользователя

  - При первой авторизации пользователю присваивается случайно сгенерированный 6-значный инвайт-код (цифры и символы).
  - В профиле пользователя есть возможность ввести чужой инвайт-код. Если код существует, он привязывается к профилю пользователя.
  - Один пользователь может активировать только один инвайт-код. Если инвайт-код уже активирован, он отображается в профиле пользователя.
  - В профиле также отображается список номеров телефонов пользователей, которые ввели инвайт-код текущего пользователя.
## API Эндпоинты
### 1. Запрос на отправку кода авторизации
* URL: /api/user/auth/
* Метод: POST
* Описание: Отправляет 4-значный код авторизации на указанный номер телефона.
* Параметры запроса:
  * phone_number (string): Номер телефона пользователя.
* Пример ответа:
```json
{
  "detail": "Код отправлен."
}
```
### 2. Подтверждение кода авторизации
* URL: /api/user/auth/
* Метод: POST
* Описание: Проверяет введенный пользователем код и возвращает токены для аутентификации.
* Параметры запроса:
  * phone_number (string): Номер телефона пользователя.
  * verification_code (string): Код авторизации.
* Пример ответа:
```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```
### 3. Запрос профиля пользователя
* URL: /api/user/me/
* Метод: GET
* Описание: Возвращает данные профиля текущего пользователя.
* Заголовки:
  * Authorization: Bearer JWT_ACCESS_TOKEN
* Пример ответа:
```json
{
  "phone_number": "+71111111111",
  "invite_code": "C5MMZT",
  "invited_by": "B2XNYT",
  "referrals": ["+72222222222", "+73333333333"]
}
```
### 4. Ввод инвайт-кода
* URL: /api/user/set-referral/
* Метод: POST
* Описание: Позволяет пользователю ввести чужой инвайт-код.
* Заголовки:
  * Authorization: Bearer JWT_ACCESS_TOKEN
* Параметры запроса:
  * invite_code (string): Инвайт-код другого пользователя.
* Пример ответа:
```json
{
  "detail": "Реферальный код успешно активирован."
}
```
## Установка и настройка
### Клонирование репозитория:

```bash
git clone git@github.com:FairuzovR/Course_final_work.git
```
### Установка зависимостей:

```bash
pip install -r requirements.txt
```
### Применение миграций:

```bash
python manage.py makemigrations user
python manage.py migrate
```
### Запуск сервера:

```bash
python manage.py runserver
```
## Тестирование API
Для тестирования API, создана Postman коллекция со всеми необходимыми запросами. Импортируйте коллекцию и отправляйте запросы.
## Запуск в контейнерах
Заполнить файл .env, указать DB_HOST=db
Перейти в каталог с файлами
```bash
cd TB4
```
Запустить оркестрацию контейнеров
```bash
docker compose up -d
```
Применить миграции 
```bash
docker compose exec app python manage.py migrate
```