import os
from invoke import task


@task
def runit(ctx):
    print('Migrating db')
    ctx.run("./manage.py migrate")

    print('Collecting static')
    ctx.run("./manage.py collectstatic --noinput")

    uwsgi_command = (
        "uwsgi --module=wsgi:application --master"
        " --http=0.0.0.0:8000"
        " --max-requests=5000"
        " --vacuum"
    )
    if os.getenv("PY_AUTORELOAD"):
        uwsgi_command += " --process=2"
        uwsgi_command += " --py-autoreload 1"
    else:
        uwsgi_command += " --process=5"

    if os.getenv('ENV') == 'dev':
        uwsgi_command += ' --honour-stdin'
    else:
        uwsgi_command += ' --harakiri 30'

    ctx.run(uwsgi_command)
