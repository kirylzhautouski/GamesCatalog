#!/bin/bash

cd gamemuster
celery -A gamemuster.celery worker -l info -B