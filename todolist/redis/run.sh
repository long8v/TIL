echo redis-server starting!
redis-server 6001.conf
redis-server 6002.conf
redis-server 6003.conf
tail redis-server.log
bash sen1.sh start
bash sen2.sh start
bash sen3.sh start