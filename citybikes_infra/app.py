#!/usr/bin/env python3
import os

from aws_cdk import (
    App,
    Environment)

from citybikes_infra.s3_bucket_stack import CitybikesInfraStack
from citybikes_infra.emr_serverless_app import EmrServerlessStack


app = App()

# grab the account & region from your AWS CLI config (or environment)
env = Environment(
    account=os.getenv('CDK_DEFAULT_ACCOUNT'),
    region=os.getenv('CDK_DEFAULT_REGION')
)

CitybikesInfraStack(app, "CitybikesInfraStack", env=env)
EmrServerlessStack(app, 'EmrServerlessStack', env=env)

app.synth()
