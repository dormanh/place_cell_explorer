import boto3
import pandas as pd
import os

from pathlib import Path


ENDPOINT = "https://s3.eu-de.cloud-object-storage.appdomain.cloud"
S3 = boto3.client("s3", endpoint_url=ENDPOINT)
BUCKET = os.environ["AWS_BUCKET"]


def read_parquet_from_bucket(key: str) -> pd.DataFrame:
    """Reads a parquet file from the given s3 bucket."""
    obj = S3.get_object(Bucket=BUCKET, Key=key)
    dfp = Path("_.p")
    dfp.write_bytes(obj["Body"].read())
    df = pd.read_parquet(dfp)
    dfp.unlink()

    return df
