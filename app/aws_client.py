import boto3
from app.config import AWS_REGION

def get_cloudwatch():
    return boto3.client("cloudwatch", region_name=AWS_REGION)

def get_ec2():
    return boto3.client("ec2", region_name=AWS_REGION)
