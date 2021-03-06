#coding:utf-8
import os
import subprocess
import time
import datetime
import dateutil.relativedelta
import logging
import threading

def identifyFileExist(filepath):
    if not os.path.exists(filepath):
        print filepath,'does not exists , stop testing........'
        exit(1)

env_load_file="/code/env.txt"
identifyFileExist(env_load_file)
f_jmx = open("%s"%env_load_file)
jmx_content=f_jmx.readline()
while jmx_content:
    if not jmx_content.find("ES_SOURCE_IP")==-1:
        source_es_ip=jmx_content.split("=")[1]
        source_es_ip=source_es_ip.strip('\n')
    if not jmx_content.find("ES_SOURCE_PORT")==-1:
        source_es_port=jmx_content.split("=")[1]
        source_es_port=source_es_port.strip('\n')
    if not jmx_content.find("LOG_EFFECTIVE_MONTH")==-1:
        str_effmonth=jmx_content.split("=")[1]
        str_effmonth=str_effmonth.strip('\n')
    if not jmx_content.find("ES_MANAGEMENT_LOG_LEVEL")==-1:
        log_level=jmx_content.split("=")[1]
        log_level=log_level.strip('\n')
    jmx_content=f_jmx.readline()

f_jmx.close()

logger = logging.getLogger('mylogger')  
logger.setLevel(logging.DEBUG) 
fh = logging.FileHandler('test.log')  
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
fh.setFormatter(formatter)  
ch.setFormatter(formatter) 
logger.addHandler(fh)  
logger.addHandler(ch)  

def backup_index(source_ip ,source_port ,index):
    logger.debug("Using function backup_index........")
    logger.debug("source_ip = "+source_ip)
    logger.debug("source_port = "+source_port)
    logger.debug("index = "+index)
#    os.system("touch /elasticsearch-backup/"+index+".json")
    os.system("elasticdump  --input=http://"+source_ip+":"+source_port+"/"+index+" --output=/elasticsearch-backup/"+index+".json")
    logger.info("Finishing to dump elasticsearch data(index) , index : "+index)
    logger.info("dump data was store in /elasticsearch-backup/"+index+".json")

def delete_index(source_ip ,source_port ,index):
    logger.info("Using function delete_index........")
    logger.debug("source_ip = "+source_ip)
    logger.debug("source_port = "+source_port)
    logger.debug("index = "+index)
    os.system("rm -rf /curator/delete_index_copy.yaml")
    os.system("rm -rf /curator/curator_copy.yaml")
    os.system("cp /curator/curator.yaml /curator/curator_copy.yaml")
    os.system("cp /curator/delete_index.yaml /curator/delete_index_copy.yaml")
    os.system("sed -i 's/<INDEX_NAME>/"+index+"/g' /curator/delete_index_copy.yaml")
    os.system("sed -i 's/<IP_ADDRESS>/"+source_ip+"/g' /curator/curator_copy.yaml")
    os.system("sed -i 's/<ES_PORT>/"+source_port+"/g' /curator/curator_copy.yaml")
    os.system("curator --config /curator/curator_copy.yaml /curator/delete_index_copy.yaml" )
    logger.info("Finishing to remove elasticsearch index , index : "+index)

def get_yesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday

now = datetime.datetime.now()
print "Running time : " + str(now)
#logger.info("Running time : "+now)

now2 = datetime.date.today()
print "Running date : " + str(now2)
#logger.info("Running date : "+now2)

#env_object = os.environ
#log_level = env_object.get('ES_MANAGEMENT_LOG_LEVEL')
#source_es_ip = env_object.get('ES_SOURCE_IP')
#source_es_port = env_object.get('ES_SOURCE_PORT')
logger.info("Getting elasticsearch IP address : %s"%source_es_ip)
effmonth = int(str_effmonth)
logger.info("Setting effictive range for data in elasticsearch : %s"%effmonth)
filernow = now + dateutil.relativedelta.relativedelta(months=-effmonth)
short_date = str(filernow).split()[0]
yestday_date = str(get_yesterday())

logger.info("If index-name contain  %s , this index will be delet"%short_date)
logger.info("If index-name contain  %s , this index will be backup"%yestday_date)

cmd_curl = "curl '%s:9200/_cat/indices?v&h=i' > /tmp/list.txt"%source_es_ip
logger.info("Getting tje index list from elasticsearch , ip : %s"%source_es_ip)
logger.info("List in : /tmp/list.txt")
handle = subprocess.call(cmd_curl, shell=True, stdout=subprocess.PIPE)
#handle = subprocess.Popen(cmd_curl, shell=True, stdout=subprocess.PIPE)
logger.info("Updating index-files : /tmp/list.txt")
#print handle.communicate()[0]
fp = open('/tmp/list.txt', "r") 
line = fp.readline()
while line:
#    print line
    if line.find(short_date)==-1:
#        print "%s not contain %s"%(line,short_date)
        logger.debug("%s not contain %s"%(line,short_date))
    else:
        line = line.strip('\n')
        print "%s contain %s , this index ready to delete ........"%(line,short_date)
        logger.debug("%s contain %s"%(line,short_date))
        logger.info("Starting to remove elasticsearch data ......")
        delete_index(source_es_ip ,source_es_port , line)
    if line.find(yestday_date)==-1:
#        print "%s not contain %s"%(line,yestday_date)
        logger.debug("%s not contain %s"%(line,yestday_date))
    else:
        line = line.strip('\n')
        print "%s contain %s , this index ready to backup ........"%(line,yestday_date)
        logger.debug("%s contain %s"%(line,yestday_date))
        logger.info("Starting to backup elasticsearch data ......")
        backup_index(source_es_ip,source_es_port,line)
    line = fp.readline()
fp.close()

#os.system("sleep 5s")
