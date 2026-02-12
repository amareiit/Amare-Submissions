import boto3

ec2 = boto3.client('ec2', region_name='us-east-2')

grandTotal = 0

response = ec2.describe_instances()

instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        if instance['State']['Name'] == 'running':
            instances.append(instance)

if len(instances) == 0:
    print("No running instances found. Destroy successful.")
    grandTotal += 1
else:
    print("Instances still running!")

print("FINAL GRADE:", grandTotal, "/ 1")
