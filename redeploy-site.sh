#!/usr/bin/bash
tmux kill-server
cd portfolio-site
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new-session -d -s flask
tmux send-keys -t flask 'source python3-virtualenv/bin/activate' C-m
tmux send-keys -t flask 'flask run --host=0.0.0.0' C-m
