#    	Download https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json to local directory as index.json
#
#    	Install pandas

import json
import pandas as pd

__output_file__ = '../app/instances.json'
__min_number_of_cores__ = 32
__gpu_only__ = True

f = open("index.json", "r")

raw_data = json.loads(f.read())

lumpy_data = [v for k, v in raw_data["products"].items()]
data = []

for ld in lumpy_data:
	try:
		i = {k: v for k, v in ld["attributes"].items()}
		i["sku"] = ld["sku"]
		i["productFamily"] = ld["productFamily"]
		data.append(i)
	except:
		pass

df = pd.DataFrame(data)

#    	[nan, u'AWS GovCloud (US)', u'Asia Pacific (Mumbai)', u'Asia Pacific (Seoul)', u'Asia Pacific (Singapore)',
#    	u'Asia Pacific (Sydney)', u'Asia Pacific (Tokyo)', u'Canada (Central)', u'EU (Frankfurt)', u'EU (Ireland)',
#    	u'EU (London)', u'South America (Sao Paulo)', u'US East (N. Virginia)', u'US East (Ohio)',
#    	u'US West (N. California)', u'US West (Oregon)']

#TODO: only get us-east-1c instances

df["location"] = df["location"].map({
	"US East (Ohio)": "us-east-2", "US East (N. Virginia)": "us-east-1", "US West (N. California)": "us-west-1",
	"US West (Oregon)": "us-west-2", "Asia Pacific (Mumbai)": "ap-south-1", "Asia Pacific (Seoul)": "ap-northeast-2",
	"Asia Pacific (Singapore)": "ap-southeast-1", "Asia Pacific (Sydney)": "ap-southeast-2",
	"Asia Pacific (Tokyo)": "ap-northeast-1", "Canada (Central)": "ca-central-1", "EU (Frankfurt)": "eu-central-1",
	"EU (Ireland)": "eu-west-1", "EU (London)": "eu-west-2", "South America (Sao Paulo)": "sa-east-1"})

#TODO: filter instance types by  "instanceFamily" : "GPU instance",

if __gpu_only__:
	_instanceData = df[(df["operatingSystem"] == "Linux")
				& (df["location"].notnull())
				& (df["productFamily"] == "Compute Instance")
				& (df["instanceFamily"] == "GPU instance")
				& (df['vcpu'].astype(float) >= __min_number_of_cores__)][["location", "instanceType"]].\
				drop_duplicates().to_json(orient = "records")

else:
	_instanceData = df[(df["operatingSystem"] == "Linux")
				& (df["location"].notnull())
				& (df["productFamily"] == "Compute Instance")
				& ((df['vcpu'].astype(float) >= __min_number_of_cores__)
				| (df['instanceType'].str.contains('p3')))][["location", "instanceType"]].\
				drop_duplicates().to_json(orient = "records")

try:
	_t = open(__output_file__, 'w')
	_t.write(_instanceData)
	print('data written to instances.json')

except Exception as exc:
	print('Failed to write file:', exc)

finally:
	_t.close()
