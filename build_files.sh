#!/bin/bash

# Update package lists
sudo yum update -y

# Install required dependencies
sudo yum install -y python3-pip python3-devel gcc

# Install Python packages
pip3 install -r requirements.txt
