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
