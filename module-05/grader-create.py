import boto3
import requests
import time
from tqdm import tqdm

ec2 = boto3.client('ec2', region_name='us-east-2')

grandTotal = 0

response = ec2.describe_instances()

instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['State']['Name'] == 'running':
            instances.append(instance)

print("*" * 60)
print("Checking instance count...")

if len(instances) == 3:
    print("Correct number of instances (3)")
    grandTotal += 1
else:
    print(f"Expected 3 instances, found {len(instances)}")

print("*" * 60)
print("Checking instance type...")

typeMismatch = False
for i in instances:
    if i['InstanceType'] != "t3.micro":
        typeMismatch = True

if not typeMismatch:
    print("All instances are t3.micro")
    grandTotal += 1
else:
    print("Instance type mismatch detected")

print("*" * 60)
print("Checking tags...")

tagMismatch = False
for i in instances:
    if not any(tag['Value'] == "module-05" for tag in i.get('Tags', [])):
        tagMismatch = True

if not tagMismatch:
    print("Correct tag found")
    grandTotal += 1
else:
    print("Tag mismatch detected")

print("*" * 60)
print("Checking HTTP response...")

for i in tqdm(range(30)):
    time.sleep(1)

httpSuccess = False

try:
    dns = instances[0]['PublicDnsName']
    res = requests.get("http://" + dns)
    if res.status_code == 200:
        print("HTTP 200 OK received")
        httpSuccess = True
        grandTotal += 1
    else:
        print("Incorrect HTTP status:", res.status_code)
except:
    print("Could not connect to instance")

print("*" * 60)
print("FINAL GRADE:", grandTotal, "/ 4")
