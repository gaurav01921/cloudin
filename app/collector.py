import os
import datetime
import pandas as pd
from app.aws_client import get_cloudwatch
from app.config import INSTANCE_ID, CSV_PATH


def collect_metrics():
    cloudwatch = get_cloudwatch()
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": INSTANCE_ID}],
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(minutes=5),
        EndTime=datetime.datetime.utcnow(),
        Period=300,
        Statistics=["Average"]
    )
    datapoints = response["Datapoints"]
    if not datapoints:
        return None

    df = pd.DataFrame(datapoints)
    df.to_csv(CSV_PATH, mode="a", header=not os.path.exists(
        CSV_PATH), index=False)
    return df
