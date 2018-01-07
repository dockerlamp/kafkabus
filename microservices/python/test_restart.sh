#!/bin/sh

echo 'restarting producer app...'
echo 'killing current producer...'
killall python simple_producer.py
echo 'starting producer app...'
python simple_producer.py
echo 'started producer app...'
