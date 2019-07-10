import json
import os
import boto3


def invoke_lambda(function_name):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=function_name
    )

    return response


def code_deploy_event_status(depId, eventId, status):
    client = boto3.client('codedeploy')
    response = client.put_lifecycle_event_hook_execution_status(
        deploymentId=depId,
        lifecycleEventHookExecutionId=eventId,
        status=status
    )

    return response


def test_oleoleole_version_pre_traffic(event, context):
    current_function_version = os.getenv("CurrentFunctionVersion")
    pre_test_rsp = invoke_lambda(current_function_version)
    deployment_id = event['DeploymentId']
    life_cycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    ret = pre_test_rsp['Payload'].read()
    data = json.loads(ret)
    body = json.loads(data['body'])

    try:
        assert data['statusCode'] == 200
        assert body['version'] == os.getenv("APP_VERSION")
        code_deploy_event_status(deployment_id, life_cycle_event_hook_execution_id, 'Succeeded')
    except AssertionError:
        code_deploy_event_status(deployment_id, life_cycle_event_hook_execution_id, 'Failed')


def test_oleoleole_version_post_traffic(event, context):
    deployment_id = event['DeploymentId']
    life_cycle_event_hook_execution_id = event['LifecycleEventHookExecutionId']

    # code_deploy_event_status(deployment_id, life_cycle_event_hook_execution_id, 'Failed')
    code_deploy_event_status(deployment_id, life_cycle_event_hook_execution_id, 'Succeeded')

