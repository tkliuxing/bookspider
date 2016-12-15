#!/bin/bash

./manage.py collectstatic --noinput && ./manage.py assets build
