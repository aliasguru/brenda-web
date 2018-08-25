sudo apt install pip
sudo apt install pandas
rm index.json
wget https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json .

sudo python2.7 aws_instance_parser.py

