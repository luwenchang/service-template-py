#!/usr/bin/env bash

# 功能：一键安装程序运行环境
# 注意事项
#   1. 您应该在执行本脚本前先执行命令 `sudo apt-get -y update && sudo apt-get -y upgrade`
#   2. 您应用 root 角色执行本脚本
#   3. 本脚本执行环境：Ubuntu 16.04

echo "开始更新索引"
sudo apt-get update
echo "索引更新完成"

echo "开始安装程序的基础运行环境必备包"
sudo apt-get install -y python-pip python-dev libmysqlclient-dev git  redis-server

echo "准备创建用户：dev"
useradd -d /home/dev -m dev -s /bin/bash

echo "请为 dev 用户设置密码 "
passwd dev
echo "密码设置成功"


echo "切换 dev 执行命令"
su - dev <<EOF

echo "创建相关目录"
mkdir configs

echo "拉取代码"
git clone https://github.com/luwenchang/service-template-py.git

echo "进入项目目录"
cd service-template-py
echo "切换到指定分支 dev"
git checkout dev


cat /home/dev/service-template-py/tools/deploy_tool/bashrc.txt >> /home/dev/.bashrc

cp /home/dev/service-template-py/tools/deploy_tool/bash_profile.txt /home/dev/.bash_profile


EOF

pip install -r  /home/dev/service-template-py/requirements.txt



