from app.aws_client import get_ec2
from app.config import INSTANCE_ID

def stop_instance():
    ec2 = get_ec2()
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    print("Instance stopped")
