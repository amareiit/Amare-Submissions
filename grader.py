# Module 09 Autograder
import boto3
import json
import requests
import hashlib
import sys
import datetime
import time
from tqdm import tqdm

# Assignment grand total
grandtotal = 0
totalPoints = 10
assessmentName = "module-09-assessment"

tag = "module-09"

# Function to print out current points progress
def currentPoints():
  print("Current Points: " + str(grandtotal) + " out of " + str(totalPoints) + ".")

clientec2 = boto3.client('ec2', region_name='us-east-2')
clientelbv2 = boto3.client('elbv2', region_name='us-east-2')
clientasg = boto3.client('autoscaling', region_name='us-east-2')

responseELB = clientelbv2.describe_load_balancers()

print('*' * 79)
print("Begin tests for Module-09 Assessment...")
print('*' * 79)

# ---------------- VPC ----------------
print("Testing VPC...")
vpcs = clientec2.describe_vpcs(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['Vpcs']

print("Found:", len(vpcs))
if len(vpcs) == 1:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- SG ----------------
print("\nTesting Security Group...")
sgs = clientec2.describe_security_groups(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['SecurityGroups']

print("Found:", len(sgs))
if len(sgs) == 1:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- HTTP ----------------
print("\nTesting HTTP 200...")
if len(responseELB['LoadBalancers']) == 1:
  dns = responseELB['LoadBalancers'][0]['DNSName']
  print("URL:", "http://" + dns)

  for i in tqdm(range(20)):
    time.sleep(1)

  try:
    res = requests.get("http://" + dns)
    if res.status_code == 200:
      grandtotal += 1
      print("PASS")
    else:
      print("FAIL - status:", res.status_code)
  except:
    print("FAIL - no response")
else:
  print("FAIL - no ELB found")

currentPoints()

# ---------------- EC2 ----------------
print("\nTesting EC2 Instances...")
instances = clientec2.describe_instances(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)

count = sum(len(r['Instances']) for r in instances['Reservations'])

print("Found:", count)
if count == 3:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- IGW ----------------
print("\nTesting Internet Gateway...")
igw = clientec2.describe_internet_gateways(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['InternetGateways']

print("Found:", len(igw))
if len(igw) == 1:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- SUBNETS ----------------
print("\nTesting Subnets...")
subnets = clientec2.describe_subnets(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['Subnets']

print("Found:", len(subnets))
if len(subnets) == 3:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- ROUTE TABLES ----------------
print("\nTesting Route Tables...")
rts = clientec2.describe_route_tables(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['RouteTables']

print("Found:", len(rts))
if len(rts) == 3:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- DHCP ----------------
print("\nTesting DHCP Options...")
dhcp = clientec2.describe_dhcp_options(
    Filters=[{'Name': 'tag:Name', 'Values': [tag]}]
)['DhcpOptions']

print("Found:", len(dhcp))
if len(dhcp) == 1:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- ASG ----------------
print("\nTesting Auto Scaling Group...")
asg = clientasg.describe_auto_scaling_groups()

asg_count = 0
for g in asg['AutoScalingGroups']:
  for t in g.get('Tags', []):
    if t['Value'] == tag:
      asg_count += 1

print("Found:", asg_count)
if asg_count == 1:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- ROUTE → IG ----------------
print("\nTesting Route Table attached to IG...")
attached = False

for rt in rts:
  for route in rt['Routes']:
    if 'GatewayId' in route and route['GatewayId'].startswith('igw'):
      attached = True

print("Attached:", attached)
if attached:
  grandtotal += 1
  print("PASS")
else:
  print("FAIL")
currentPoints()

# ---------------- FINAL ----------------
print('*' * 79)
print("Final Score:", grandtotal, "/", totalPoints)

# Write results
f = open('module-09-results.txt', 'w')

dt = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
resultToHash = (assessmentName + str(grandtotal/totalPoints) + dt)

h = hashlib.new('sha256')
h.update(resultToHash.encode())

resultsdict = {
  'Name': assessmentName,
  'gtotal': grandtotal/totalPoints,
  'datetime': dt,
  'sha': h.hexdigest()
}

json.dump(resultsdict, f)
f.close()

print("Results file generated.")