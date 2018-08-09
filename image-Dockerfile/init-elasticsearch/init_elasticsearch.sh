#!/bin/sh

if [[ ${#INIT_ELASTICSEARCH_HOST} == 0 ]]; then
	INIT_ELASTICSEARCH_HOST=172.17.0.1
fi

if [[ ${#INIT_ELASTICSEARCH_PORT} == 0 ]]; then
	INIT_ELASTICSEARCH_PORT=9200
fi

if [[ ${#INIT_ELASTICSEARCH_RECORDS_TEMPLATE} == 0 ]]; then
	INIT_ELASTICSEARCH_RECORDS_TEMPLATE=emotibot_records_template
fi

if [[ ${#INIT_ELASTICSEARCH_SESSIONS_TEMPLATE} == 0 ]]; then
	INIT_ELASTICSEARCH_SESSIONS_TEMPLATE=emotibot_sessions_template
fi

until curl -sS $INIT_ELASTICSEARCH_HOST":"$INIT_ELASTICSEARCH_PORT &> /dev/null; do echo "Waiting Elasticsearch..." && sleep 3; done

echo "Update 'emotibot-records-*' index template: "$INIT_ELASTICSEARCH_RECORDS_TEMPLATE
curl -sS -XPUT -H "Content-type:application/json" $INIT_ELASTICSEARCH_HOST":"$INIT_ELASTICSEARCH_PORT"/_template/"$INIT_ELASTICSEARCH_RECORDS_TEMPLATE \
	-d @index_templete/records_template.json

echo "\nUpdate 'emotibot-sessions-*' index template: "$INIT_ELASTICSEARCH_SESSIONS_TEMPLATE
curl -sS -XPUT -H "Content-type:application/json" $INIT_ELASTICSEARCH_HOST":"$INIT_ELASTICSEARCH_PORT"/_template/"$INIT_ELASTICSEARCH_SESSIONS_TEMPLATE \
	-d @index_templete/sessions_template.json

echo "\nDone!!"
