#!/bin/bash
env | grep ES_SOURCE_IP >> env.txt
env | grep ES_SOURCE_PORT >> env.txt
env | grep LOG_EFFECTIVE_MONTH >> env.txt
env | grep ES_MANAGEMENT_LOG_LEVEL >> env.txt

crond  
touch /var/log/cron.log  
#python dairy.py 
sleep infinity
