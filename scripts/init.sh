#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# =========================系统软件安装=========================
#升级系统
#apt-get -y update
#apt-get -y upgrade

# 安装python头文件
sudo apt-get install -y python-dev nginx libxml2-dev libxslt-dev python-lxml python-pip supervisor virtualenvwrapper



# ========================python 虚拟机安装=====================

source /usr/local/bin/virtualenvwrapper.sh

echo "创建virtualenv lost"
mkvirtualenv lost
workon lost

echo "python 安装所需要的包"

cd $CURRENT_DIR

pip install -r requirements.txt -q
# =============================================================
