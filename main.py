import boto3
import datetime
import argparse

def get_active_instances_ami_names(region_name='us-east-1', profile_name=None):
    # Initialize a session using a specific profile
    if profile_name:
        session = boto3.Session(profile_name=profile_name, region_name=region_name)
    else:
        session = boto3.Session(region_name=region_name)

    # Use the session to create an EC2 client
    ec2 = session.client('ec2')

    # Retrieve all running instances
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    # Extract AMI IDs from running instances
    ami_ids = set()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ami_ids.add(instance['ImageId'])

    # Describe the AMIs to get their names
    ami_names = {}
    if ami_ids:
        ami_response = ec2.describe_images(
            ImageIds=list(ami_ids)
        )
        for image in ami_response['Images']:
            ami_names[image['ImageId']] = image['Name']

    return ami_names

def calculate_days_since_date(date_str):
    date_format = "%Y%m%d"
    ami_date = datetime.datetime.strptime(date_str, date_format).date()
    current_date = datetime.date.today()
    delta = current_date - ami_date
    return delta.days

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Query AMI names in active instances.')
    parser.add_argument('--profile', type=str, help='AWS profile name to use', required=False)
    parser.add_argument('--region', type=str, default='us-east-1', help='AWS region name', required=False)
    
    args = parser.parse_args()
    
    ami_names = get_active_instances_ami_names(region_name=args.region, profile_name=args.profile)
    
    for ami_id, ami_name in ami_names.items():
        if len(ami_name) >= 8:
            date_str = ami_name[-8:]
            try:
                days_since = calculate_days_since_date(date_str)
                print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Days Since {date_str}: {days_since} days")
            except ValueError:
                print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Error: Invalid date format in AMI name")
        else:
            print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Error: AMI name is too short to contain a date")