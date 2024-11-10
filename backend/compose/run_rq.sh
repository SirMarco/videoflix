#!/usr/bin/env bash
python manage.py rqworker low &
python manage.py rqworker high &
wait
