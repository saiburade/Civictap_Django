# CivicTap — Django + SQLite

CivicTap is a civic issue reporting application rebuilt from the original JSP/Java project using:

- Python
- Django
- SQLite
- HTML/CSS/JavaScript
- Django ORM
- Django sessions
- Server-rendered Django templates

**No REST API, Django REST Framework, React, Node.js, or external SMS API is used.**

## Features

### Citizen
- Phone-based signup
- Demo password verification
- Phone-based login with demo password
- Session authentication
- Civic issue reporting
- Image upload
- Public issue feed
- Issue status tracking
- Profile editing
- Feedback with rating
- Help / Privacy / About pages

### Admin
- Django authentication
- Dashboard statistics
- View/search users
- View/search issues
- Update issue status
- Delete issues
- Delete users
- View/search feedback

## Local setup

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Create database:
```bash
python manage.py migrate
```

Create admin:
```bash
python manage.py createsuperuser
```

Run:
```bash
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

## password

user name : admin
Password : 12345

## Media uploads

Issue images are stored under `media/issues/`.

## Deployment

The project includes a `render.yaml` and is suitable for a normal Python/Django host such as Render. SQLite is intentionally retained because it was requested for this version. For production-scale deployment, PostgreSQL would normally be preferable.

## Original-to-Django mapping

| Original Java/JSP | Django |
|---|---|
| JSP pages | Django templates |
| JDBC | Django ORM |
| Java session | Django session |
| MySQL | SQLite |
| Tomcat | Gunicorn/Django |
| Java file upload | Django `ImageField` |
| Manual admin session | Django authentication |
