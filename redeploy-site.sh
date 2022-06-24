#!/usr/bin/bash
cd portfolio-site
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip install -r requirements.txt
deactivate
systemctl daemon-reload
systemctl restart myportfolio
