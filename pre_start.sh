#!/usr/bin/env/bash

# Let DB start
python ./backend_pre_start.py

# Run migrations
alembic upgrade head

# create initial data
python ./initial_data.py