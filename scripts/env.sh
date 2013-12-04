#!/bin/bash

echo "输入域名eg：baidu.com"
read SERVER_NAME
#当前脚本所在的目录

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CURRENT_USER=$(whoami)

#当前脚本所在目录的上级目录
DIR="$(cd .. && pwd)"

echo $CURRENT_DIR--$DIR

#unix socket 文件
SOCKFILE=$DIR/run/gunicorn.sock


#升级系统
#apt-get -y update
#apt-get -y upgrade

# 安装python头文件
sudo apt-get install -y python-dev
sudo apt-get install -y nginx

# install lxml
# apt-get install -y python-lxml
sudo apt-get install -y libxml2-dev libxslt-dev
#install pip
sudo apt-get install -y python-pip

# install virtualenvwrapper

echo "正在安装python virtualenv"

sudo pip install virtualenvwrapper

source /usr/local/bin/virtualenvwrapper.sh

echo "创建virtualenv lost"
sudo mkvirtualenv lost
workon lost

echo "python 安装所需要的包"
pip install -r requirements.txt

echo "正在创建nginx配置文件"
sudo cat>$SERVER_NAME<<EOF
  upstream app_server {
    server unix:${SOCKFILE} fail_timeout=0;
  }
  server {

    listen 80;
    
    server_name ${SERVER_NAME}
    client_max_body_size 4G;
    keepalive_timeout 5;

	access_log ${DIR}/log/nginx-access.log;
    error_log  ${DIR}/log/nginx-error.log;

    location /static/ {
        alias ${DIR}/dnovel;
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
        proxy_pass http://app_server;
        break;
      }
    }

  }
EOF
NGINX_FILE=/etc/nginx/sites-enabled/$SERVER_NAME
if [[  -f "$NGINX_FILE" ]]; then
  sudo rm $NGINX_FILE
fi

# echo $CURRENT_DIR/$SERVER_NAME
sudo ln -s $CURRENT_DIR/$SERVER_NAME /etc/nginx/sites-enabled/
sudo service nginx restart

echo "配置supervisor文件"

SUPERVISOR_LOG_DIR=$DIR/log
if [[ ! -d $SUPERVISOR_LOG_DIR ]]; then
  #statements
  sudo mkdir -p $SUPERVISOR_LOG_DIR
fi
SUPERVISOR_LOG=$SUPERVISOR_LOG_DIR/gunicorn_supervisor.log
if [[ ! -f $SUPERVISOR_LOG ]]; then
  #statements
  sudo touch $SUPERVISOR_LOG
fi
sudo cat>${SERVER_NAME}.conf<<EOF
[program:${SERVER_NAME}]
command=sh ${CURRENT_DIR}/init.sh
user=`whoami`
stdout_logfile=${DIR}/log/gunicorn_supervisor.log
redirect_stderr=true
EOF
# # supervisorctl reread
# # supervisorctl update
# # supervisorctl start $SERVER_NAME
echo "supdervisor文件配置成功"

