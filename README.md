# Curator + Elasticdump + Python + Crontab

說明
------
* docker-compose : 放yaml供使用者快速運行
* image-Dockerfile: build image的相關檔案

實現功能
------
* 自動備份要刪除的index 成json檔 (供後續回復資料用)
* 自動刪除過舊index
* 備份週期以容器內的crond去實現
* 參數設定目前是以"月"為單位清除過去的elasticsearch index

備份資料以elasticdump實現
刪除是以Curator實現
週期是以crontab控制

參數設定
------
* ES_SOURCE_IP : elasticsearch的IP
* ES_SOURCE_PORT : elasticsearch暴露的port
* LOG_EFFECTIVE_MONTH : 數字 , 代表月份 , 例如設為1 , 會清除一個月前的index (清除前先備份)
* ES_MANAGEMENT_LOG_LEVEL : log等級 , 目前未完成 , 可以無視此變數

限制 :
------
* index名稱需包含Timestamp , 例如 : testxxxx-2018-03-21
* 時間的格式 : 年-月-日  , 例如 :2018-03-21

