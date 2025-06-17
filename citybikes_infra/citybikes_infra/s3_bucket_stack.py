from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class CitybikesInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.raw_bucket = s3.Bucket(
            self,
            id = 'CitybikesRawDataBucket',
            bucket_name = 'citybikes-raw-data',
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.transformed_bucket = s3.Bucket(
            self, 
            id = 'CitybikesTransformedDataBucket',
            bucket_name = 'citybikes-transformed-data',
            removal_policy=RemovalPolicy.DESTROY,
        )

        
