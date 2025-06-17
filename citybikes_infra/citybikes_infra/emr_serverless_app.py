from aws_cdk import (
    aws_iam as iam, 
    aws_ec2 as ec2,
    aws_emrserverless as emr,
    aws_logs as logs,
    Stack,
)
from constructs import Construct

class EmrServerlessStack(Stack):
    def __init__(self, scope: Construct, id:str, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.execution_role = iam.Role(
            self, 'EmrServerlessExecutionRole',
            assumed_by=iam.ServicePrincipal("emr-serverless.amazonaws.com"),
        )

        self.execution_role.add_to_policy(iam.PolicyStatement(
            actions = ['s3:*', 'glue:*'],
            resources = ['*']
        ))

        self.execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
            "CloudWatchLogsFullAccess"
        ))

        # Looks up your account’s default VPC—no need to define a new one.
        vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)

        # create security group
        # allow_all_outbound ensures your EMR Serverless pods can reach S3, Glue, etc
        sg = ec2.SecurityGroup(self, 'EmrSecurityGroup', vpc = vpc,
                               allow_all_outbound=True)
        
        # create cloudwatch log group
        log_group = logs.LogGroup(self, 'EmrServerlessLogGroup',
                                  retention=logs.RetentionDays.ONE_WEEK)
        

        # define the application
        emr_app = emr.CfnApplication(self, 'EmrServerlessApplication',
                                     release_label='emr-7.5.0',
                                     type = 'SPARK',
                                     name = 'EmrServerlessApplication',
                                     # Runs your serverless pods in the VPC’s private subnets, secured by your SG.
                                     network_configuration=emr.CfnApplication.NetworkConfigurationProperty(
                                         subnet_ids= [s.subnet_id for s in vpc.public_subnets],
                                         security_group_ids=[sg.security_group_id]
                                     ),
                                     auto_start_configuration = emr.CfnApplication.AutoStartConfigurationProperty(
                                         enabled = True
                                     ),
                                     auto_stop_configuration = emr.CfnApplication.AutoStopConfigurationProperty(
                                         enabled = True, idle_timeout_minutes=15
                                     ),
                                     # initial_capacity: how much “warm” capacity to keep ready (one driver pod with 2 vCPU/4 GB)
                                     initial_capacity = [
                                         emr.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                                             key = 'Driver',
                                             value = emr.CfnApplication.InitialCapacityConfigProperty(
                                                 worker_count = 1,
                                                 worker_configuration=emr.CfnApplication.WorkerConfigurationProperty(
                                                     cpu = '2 vCPU',
                                                     memory = '4 GB',
                                                     disk = '20 GB'
                                                 )
                                             )
                                         )
                                     ],
                                     # maximum_capacity: hard limits on total resources for any job run.
                                     maximum_capacity=emr.CfnApplication.MaximumAllowedResourcesProperty(
                                         cpu = '6 vCPU',
                                         memory = '12 GB',
                                         disk = '100 GB'
                                     )
                                     
                                     )
        # ensure the role can be assumed by the application
        emr_app.add_depends_on(self.execution_role.node.default_child)