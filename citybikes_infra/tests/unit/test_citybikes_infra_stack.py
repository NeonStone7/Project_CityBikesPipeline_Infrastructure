import aws_cdk as core
import aws_cdk.assertions as assertions

from citybikes_infra.citybikes_infra.s3_bucket_stack import CitybikesInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in citybikes_infra/citybikes_infra_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CitybikesInfraStack(app, "citybikes-infra")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
