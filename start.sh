#!/bin/sh
# Author:Chan ovo
# For openwrt
# 如果你需要在其他系统运行，需要修改最后一行为你的crontab的路径
dir=$(pwd)
echo "$dir"
power1=$(ls -l $dir|grep configure.py|awk '{print $1}')
echo "$power1"
power2=$(ls -l $dir|grep submit.py|awk '{print $1}')
echo "$power2"
[ $power1 != "-rwxr-xr-x" ] && chmod a+x $dir/configure.py
[ $power2 != "-rwxr-xr-x" ] && chmod a+x $dir/submit.py
$dir/configure.py
read_crontab=$(crontab -l|grep $dir/submit.py)
[[ "$read_crontab" ]] || echo "0 8,13,19 * * * $dir/submit.py > /dev/null 2>&1 &" >> /etc/crontabs/root
