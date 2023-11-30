#!/bin/bash

sleep 10
celery -A backend worker -l INFO