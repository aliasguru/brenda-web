#!/bin/bash

echo updating AWS instances
read -p 'Shall I download the latest index.json file from Amazon? (y/n) ' download

echo installing dependecies for evaluation
sudo apt install pip
sudo apt install pandas

if [ $download = "y" ]; then
    rm index.json
    wget https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json .
else
    echo skipping download
fi

echo Parsing the list
sudo python2.7 aws_instance_parser.py