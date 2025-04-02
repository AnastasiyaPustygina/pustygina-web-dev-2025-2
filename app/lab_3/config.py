from datetime import timedelta

class Config:
    SECRET_KEY = 'supersecretkey'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)