# AMIGuardian

## Overview

**AMIGuardian** is a Python script designed to enhance the security of your AWS infrastructure by monitoring and identifying outdated Amazon Machine Images (AMIs) in use. The script leverages the AWS Boto3 SDK to query active EC2 instances, extract the AMI names, and analyze the embedded date in these names. By comparing this date to the current date, AMIGuardian helps ensure that no old images, which may have potential security vulnerabilities, are being utilized.

## Features

- **Active Instance Query**: Retrieves a list of running EC2 instances and their associated AMI IDs.
- **AMI Name Analysis**: Extracts the last 8 characters from the AMI names, interpreting them as dates (in `YYYYMMDD` format).
- **Date Comparison**: Calculates the number of days since the AMI was created to determine the age of the image.
- **Security Insights**: Alerts you if any outdated images are in use, helping you to mitigate security risks associated with old AMIs.

## Requirements

- Python 3.6+
- Boto3 Library
- AWS Credentials configured on your system (using `aws configure`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AMIGuardian.git
   cd AMIGuardian

2. Instsall the required python packages:
   ```bash
   pip install boto3

## Usage

- Run the script with the necessary arguments to query AMI ages in active instances:
   ```bash
   python AMIGuardian.py --profiles <comma-delimited-profile-names> --regions <comma-delimited-region-names> --age <days>

### Arguments

- `--profiles` (`-p`): Comma-delimited list of AWS profile names to use (required).
- `--regions` (`-r`): Comma-delimited list of AWS region names to use (default: 'us-east-1').
- `--age` (`-a`): Number of days to compare AMI age to (default: 30).

### Example

- Querying AMI ages for profiles `myawsprofile1` and `myawsprofile2` in regions `us-west-2` and `us-east-1`, with an age comparison of 30 days:
   ```bash
   python AMIGuardian.py --profiles myawsprofile1,myawsprofile2 --regions us-west-2,us-east-1 --age 30

## Output

The script prints a detailed report including:

- Account profile name
- Region name
- Instance ID
- Instance name
- AMI name
- AMI age in days

### Sample Output
- ```yaml
   Account: myawsprofile1
     Region: us-west-2
      Instance ID: i-0123456789abcdef0, Name: web-server-1, AMI Name: ami-20220101, Age: 180 days
      Instance ID: i-0abcdef1234567890, Name: db-server-1, AMI Name: ami-20210101, Age: 365 days
     Region: us-east-1
      Instance ID: i-0fedcba9876543210, Name: app-server-1, AMI Name: ami-20210601, Age: 240 days
   Account: myawsprofile2
     Region: us-west-2
      Instance ID: i-0abcd1234567890ef, Name: cache-server-1, AMI Name: ami-20220115, Age: 175 days
     Region: us-east-1
      Instance ID: i-0f9876543210abcd, Name: api-server-1, AMI Name: ami-20210505, Age: 255 days


## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


