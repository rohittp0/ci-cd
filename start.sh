PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:$PATH

cd /home/user/ci-cd || exit 1
source venv/bin/activate

fuser -k 8000/tcp
gunicorn --bind=:8000 --log-level debug --workers=3 ci_cd.wsgi --daemon
celery multi start w1 -A ci_cd -l INFO --pidfile=/home/user/celery/ci.pid --logfile=/home/user/celery/ci.log

deactivate
