#!/bin/bash

##########
# SERVICES

# Reload systemd, enable and start the services
echo 'Starting services ...'
sudo systemctl daemon-reload
sudo systemctl restart nginx
sudo systemctl enable nginx

# Enable and start Flask server
sudo systemctl enable wzrd-server
sudo systemctl start wzrd-server

# Enable and start Node app
sudo systemctl enable wzrd-app
sudo systemctl start wzrd-app

# Double checks
sudo systemctl is-active --quiet wzrd-server || sudo systemctl restart wzrd-server;
sudo systemctl is-active --quiet wzrd-app || sudo systemctl restart wzrd-app;
sudo systemctl is-active --quiet nginx || sudo systemctl restart nginx;
