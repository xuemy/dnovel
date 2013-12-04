#!/bin/bash



NAME="lost"                                  # Name of the application
#当前脚本所在的目录
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#当前脚本所在目录的上级目录
DIR="$(cd .. && pwd)"

#django 项目目录
DJANGODIR=$DIR          # Django project directory


#log配置文件所在地(gunicorn)
LOGCONFIG=$CURRENT_DIR/logging.conf

#unix socket 文件
SOCKFILE=$DIR/run/gunicorn.sock  # we will communicte using this unix socket


USER=`whoami`                                      # the user to run as
GROUP=`whoami`                                     # the group to run as

NUM_WORKERS=4   

                                 
DJANGO_SETTINGS_MODULE=dnovel.settings

DJANGO_WSGI_MODULE=dnovel.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment

cd $DJANGODIR
# source /usr/local/bin/virtualenvwrapper.sh
# mkvirtualenv lost
# workon lo

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /usr/local/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --worker-class=egg:gunicorn#gevent