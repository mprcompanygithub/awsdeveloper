import boto3

def create_ec2_instance(region, instance_params):
    # Define the EC2 client for the specified region
    ec2 = boto3.client('ec2', region_name=region)

    # Launch the EC2 instance in the specified region
    response = ec2.run_instances(**instance_params)

    # Extract the instance ID from the response
    instance_id = response['Instances'][0]['InstanceId']

    # You can add additional logic here, such as tagging the instance

    print(f'EC2 instance {instance_id} created in {region}.')

def lambda_handler(event, context):
    # List of regions where you want to create EC2 instances
    regions = ['us-east-2', 'ap-southeast-1', 'eu-west-1']  # Add more regions as needed

    # Define region-specific configurations (key name, security group, subnet)
    region_configs = {
        'us-east-2': {
            'ImageId': 'ami-0c7f9161f8491665f',
            'KeyName': 'ohiopem',
            'SecurityGroupIds': ['sg-0fb5ba261e5fe8219'],
            'SubnetId': 'subnet-0d6a1241b257778d2'
        },
        'ap-southeast-1': {
            'ImageId': 'ami-0eb4694aa6f249c52',
            'KeyName': 'Singpem',
            'SecurityGroupIds': ['sg-0922ee6402d36751d'],
            'SubnetId': 'subnet-027e495f708c9bab4'
        },
        'eu-west-1': {
            'ImageId': 'ami-013898da85dead62b',
            'KeyName': 'Irepem',
            'SecurityGroupIds': ['sg-0bb1e497ea1806f6d'],
            'SubnetId': 'subnet-09650803d5d229443'
        }
    }

    # Specify the common instance parameters
    common_instance_params = {
        'InstanceType': 't2.micro',       # Replace with your desired instance type
        'MinCount': 1,
        'MaxCount': 1,
    }

    # Iterate over each region and create EC2 instances
    for region in regions:
        instance_params = {**common_instance_params, **region_configs.get(region, {})}
        create_ec2_instance(region, instance_params)

    return {
        'statusCode': 200,
        'body': 'EC2 instances created successfully in multiple regions!'
    }
