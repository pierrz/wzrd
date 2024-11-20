#!/bin/bash

##########
# SERVICES

# Reload systemd, enable and start the service
echo 'Starting services ...'
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl enable nginx
sudo systemctl enable wzrd-app
sudo systemctl start wzrd-app

# Double checks
sudo systemctl is-active --quiet wzrd-app || sudo systemctl restart wzrd-app;
sudo systemctl is-active --quiet nginx || sudo systemctl restart nginx;
