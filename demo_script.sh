#!/bin/sh
trap "exit" INT TERM ERR
trap "kill 0" EXIT

mosquitto & python ./client/client.py 127.0.0.1 1 &
python ./client/client.py 127.0.0.1 2 &
python ./client/client.py 127.0.0.1 3 &
python ./dashboard/dashboard.py 127.0.0.1

wait
