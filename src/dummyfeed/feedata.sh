#!/bin/sh
#
# This script will create a new session and will feed it with dummy data
#

SESSION=$1

if [ -z $SESSION ]
then
	echo "USAGE $0 <session>"
	exit 1
fi

IP=`cat pi.ip`

# create a new session
curl -X POST -H "Content-Type: application/json" -d "{ \"name\": \"${SESSION}\" }" "http://${IP}:3000/Session/"

# feed session with dummy data
for i in {1..100}
do
	let time=200+${i}*100000
	let level=${i}
	content="{ \"updates\" : [ { \"measureName\": \"Sound\", \"value\": ${level}, \"timeStamp\" : ${time}, \"description\" : \"dummy description\" } ] }"
	echo $content
	curl -X POST -H "Content-Type: application/json" -d "$content" "http://${IP}:3000/Session/${SESSION}/Update"
done

for i in {101..150}
do
	let time=200+${i}*100000
	let level=200-${i}
	content="{ \"updates\" : [ { \"measureName\": \"Sound\", \"value\": ${level}, \"timeStamp\" : ${time}, \"description\" : \"dummy description\" } ] }"
	echo $content
	curl -X POST -H "Content-Type: application/json" -d "$content" "http://${IP}:3000/Session/${SESSION}/Update"
done

echo "done"


