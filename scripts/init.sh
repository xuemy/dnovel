#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# =========================系统软件安装=========================
#升级系统
#apt-get -y update
#apt-get -y upgrade

# 安装python头文件
sudo apt-get install -y python-dev nginx libxml2-dev libxslt-dev python-lxml python-pip supervisor



# ========================python 虚拟机安装=====================

cd $CURRENT_DIR
source ../lost/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE

echo "python 安装所需要的包"

pip install -r requirements.txt -q
# =============================================================
