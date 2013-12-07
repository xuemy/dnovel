#!/bin/bash

echo "输入域名eg：baidu.com"
read SERVER_NAME
# ============================================================
#

#当前脚本所在的目录
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CURRENT_USER=$(whoami)

cd $CURRENT_DIR

#当前脚本所在目录的上级目录
DIR="$(cd .. && pwd)"

#unix socket 文件
SOCKFILE=$DIR/run/gunicorn.sock

cd $DIR

virtualenv lost

source ./lost/bin/activate
echo "python 安装所需要的包"
pip install -r requirements.txt -q

#export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

#项目log文件夹
LOG_DIR=$DIR/temp/log

if [[ ! -d $LOG_DIR ]]; then
  mkdir -p $LOG_DIR
fi

#django static root目录
DJANGO_STATIC_DIR=$DIR/temp

# nginx log
NGINX_ERROR_LOG=$LOG_DIR/nginx-error.log

NGINX_ACCESS_LOG=$LOG_DIR/nginx-access.log

# gunicorn log
GUNICORN_ERROR_LOG=$LOG_DIR/gunicorn.error.log

GUNICORN_ACCESS_LOG=$LOG_DIR/gunicorn.access.log

# supervisor log
SUPERVISOR_LOG=$LOG_DIR/supervisor.log

if [[ ! -f $GUNICORN_ACCESS_LOG ]]; then
  touch $GUNICORN_ACCESS_LOG
fi
if [[ ! -f $GUNICORN_ERROR_LOG ]]; then
  touch $GUNICORN_ERROR_LOG
fi
if [[ ! -f $SUPERVISOR_LOG ]]; then
  touch $SUPERVISOR_LOG
fi



# ===========================生成脚本============================

echo "生成运行脚本"
test -d $DIR/conf || mkdir -p $DIR/conf

cd $DIR/conf

cat>run<<EOF
#!/bin/bash
NAME=lost

#django 项目目录
DJANGODIR=${DIR}

#log配置文件所在地(gunicorn)
LOGCONFIG=$CURRENT_DIR/logging.conf

#unix socket 文件
SOCKFILE=${SOCKFILE}  # we will communicte using this unix socket


USER=\`whoami\`
GROUP=\`whoami\`

NUM_WORKERS=4   

                                 
DJANGO_SETTINGS_MODULE=dnovel.settings

DJANGO_WSGI_MODULE=dnovel.wsgi

echo "Starting $NAME as \`whoami\`"


cd \$DJANGODIR
source ./lost/bin/activate
export DJANGO_SETTINGS_MODULE=\$DJANGO_SETTINGS_MODULE
export PYTHONPATH=\$DJANGODIR/lost:\$PYTHONPATH

export DJANGO_SETTINGS_MODULE=\$DJANGO_SETTINGS_MODULE

# Create the run directory if it doesn't exist
RUNDIR=\$(dirname \$SOCKFILE)
test -d \$RUNDIR || mkdir -p \$RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../lost/bin/gunicorn \${DJANGO_WSGI_MODULE}:application \\
  --name \$NAME \\
  --workers \$NUM_WORKERS \\
  --user=\$USER --group=\$GROUP \\
  --bind=unix:\$SOCKFILE \\
  --log-level=debug \\
  --worker-class=egg:gunicorn#gevent
EOF


echo "正在创建nginx配置文件"
cat>$SERVER_NAME<<EOF
  upstream ${SERVER_NAME}app_server {
    server unix:${SOCKFILE} fail_timeout=0;
  }
  server {

    listen 80;
    
    server_name ${SERVER_NAME};
    client_max_body_size 4G;
    keepalive_timeout 5;

	  access_log ${NGINX_ACCESS_LOG};
    error_log  ${NGINX_ERROR_LOG};

    location /static/ {
        root ${DJANGO_STATIC_DIR};
        expires 24h;
    }

    location /media/ {
    	alias ${DIR}/dnovel;
    	expires 30d;
    }

    location / {

      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

      proxy_set_header Host \$http_host;

      proxy_redirect off;

      if (!-f \$request_filename) {
        proxy_pass http://${SERVER_NAME}app_server;
        break;
      }
    }

  }
EOF

echo "配置supervisor文件"

cat>${SERVER_NAME}.conf<<EOF
[program:${SERVER_NAME}]
command=sh ${DIR}/conf/run
user=`whoami`
stdout_logfile=${SUPERVISOR_LOG}
redirect_stderr=true
EOF
echo "supdervisor文件配置成功"

