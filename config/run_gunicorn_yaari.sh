set -e
LOGFILE=/home/ubuntu/log/gunicorn/yaari.log
ERRORLOGFILE=/home/ubuntu/log/gunicorn/error_yaari.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=4
# user/group to run as
USER=ubuntu
source /opt/yaari/venv/bin/activate
cd /opt/yaari/yaari
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn yaari.wsgi -w $NUM_WORKERS -c /etc/gunicorn/gunicorn_yaari.conf.py \
  --user=$USER  --log-level=error --error-logfile=$ERRORLOGFILE  --access-logfile=$LOGFILE --access-logformat "%(t)s %(p)s %({Host}i)s %(r)s %(s)s %({X-Request-Id}i)s" 2>>$LOGFILE
