# Social-Media-API

You are tasked with building a RESTful API for a social media platform. The API should allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions

# Features
- Token authentication
- Admin panel /admin/
- Documentation is located at /api/doc/swagger/ and /api/doc/redoc/
- Managing posts & following social media api
- Creating user at /api/users/
- Login user at /api/users/token/
- Managing user at /api/users/me/
- Detail users info at /api/users/{pk}/
- Creating posts at /api/media/posts/
- Detail posts info at /api/media/posts/{pk}/
- Creating followings at /api/users/followings/
- Followings detail at /api/users/followings/{pk}/


# Installing using GitHub
```
git clone https://github.com/Evheniia96/Social-Media-API.git
cd Social-Media-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
# .env file
Open file .env.sample and change environment variables to yours. Also rename file extension to .env

# Run on local server
- Install PostgreSQL, create DB and User
- Connect DB
- Run:
```
python manage.py migrate
python manage.py runserver
```

## Getting access
You can use following:
- superuser:
  - Email: admin@gmail.com
  - Password: 1qazcde3
  - nickname: admin
