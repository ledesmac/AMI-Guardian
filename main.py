import boto3
import datetime
import argparse
from instance import Instance, get_instance_name
from account import Account
from region import Region

def get_image_ages(ami_names):
    ami_ages = {}
    for ami_id, ami_name in ami_names.items():
        if len(ami_name) >= 8:
            if ami_name[-2:] == "-1":
                date_str = f"20{ami_name[-8:-2]}"
            else:
                date_str = f"20{ami_name[-6:]}"
            try:
                days_since = calculate_days_since_date(date_str)
                ami_ages[ami_id] = days_since
                #print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Days Since {date_str}: {days_since} days")
            except ValueError:
                print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Error: Invalid date format in AMI name")
        else:
            print(f"AMI ID: {ami_id}, AMI Name: {ami_name}, Error: AMI name is too short to contain a date")

    return ami_ages

def get_active_instances(region_name='us-east-1', profile_name=None):
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

    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            inst_attributes = Instance(get_instance_name(instance["Tags]"], instance["InstanceId"], instance["ImageId"]))
            instances.append(inst_attributes)

    return instances

def get_ami_names(instances, region, profile =0):
    # Initialize a session using a specific profile
    if profile:
        session = boto3.Session(profile_name=profile, region_name=region)
    else:
        session = boto3.Session(region_name=region)

    # Use the session to create an EC2 client
    ec2 = session.client('ec2')

    # Describe the AMIs to get their names
    ami_names = {}
    ami_ids = set()
    for instance in instances:
        ami_ids.add(instance.get_ami_id())
    
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

    parser = argparse.ArgumentParser(description='Query AMI age in active instances.')
    parser.add_argument('-p','--profiles', type=str, help='Comma-delimited list of AWS profile names to use', required=True)
    parser.add_argument('-r','--regions', type=str, default=['us-east-1'], help='Comma-delimited list of AWS profile names to use', required=False)
    parser.add_argument('-a','--age', type=int, default=30, help='# of days to compare ami age to',required=False)
    
    args = parser.parse_args()
    
    profiles = args.profiles.split(',')
    regions = args.regions.split(',')
    accounts = []
    for profile in profiles:
        account = Account(profile)
        for region in regions:
            instances = get_active_instances (region_name=args.region, profile_name=args.profile)
            ami_names = get_ami_names(instances = instances, region_name=args.region, profile_name=args.profile)
            ami_ages = get_image_ages(ami_names)

            for instance in instances:
                instance.set_age(ami_ages[instance.get_ami_id()])
                instance.set_ami_name(ami_names[instance.get_ami_id()])

            sorted_instances_desc = sorted(instances, key=lambda x: x.age, reverse=True)
            

            inv = Region(name=region, instances=sorted_instances_desc)
            account.add_region(inv)
        
        accounts.append(account)

    
    for account in accounts:
        print(f"Profile: {account.profile}")
        for region in account.get_regions():
            print(f"Region: {region.name}")
            for instance in region.get_instances():
                if instance.get_age() > args.age:
                    print(f"Instance Name: {instance.instance_name}, Instance ID: {instance.instance_id}, AMI ID: {instance.ami_id}, AMI Name: {instance.ami_name}, Age: {instance.age} days")