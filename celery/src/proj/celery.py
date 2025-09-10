from celery import Celery

app = Celery('tasks', backend="redis://localhost",
             broker='pyamqp://guest@localhost//',
             include=['proj.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
