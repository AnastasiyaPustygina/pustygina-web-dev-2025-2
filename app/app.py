from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app.lab_1.app import app as lab1_app
from app.lab_2.app import app as lab2_app
from app.lab_3.app import app as lab3_app

application = DispatcherMiddleware(lab1_app, {
    '/lab2': lab2_app,
    '/lab3': lab3_app,
})

# Это нужно только для локального запуска
if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True)
