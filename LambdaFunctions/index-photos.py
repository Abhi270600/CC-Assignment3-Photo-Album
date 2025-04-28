import boto3
import json
import urllib
from datetime import datetime
from opensearchpy import OpenSearch, RequestsHttpConnection
import os
import time
import base64

# Initialize clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')

# ElasticSearch configuration
es_endpoint = "search-photos-37ap2zxpgqqsuw4s7xl6oy552m.aos.us-east-1.on.aws"
es_username = "aa12037"
es_password = "Abhikeer@123"

es = OpenSearch(
    hosts=[{'host': es_endpoint, 'port': 443}],
    http_auth=(es_username, es_password),
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)


def lambda_handler(event, context):
    # Get the S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    print("Starting to index photos")
    print("bucket:", bucket)
    print("key:", key)

    # Retrieve the object from S3
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    object_content = s3_object['Body'].read()
    decoded_content = base64.b64decode(object_content)

    rekognition_response = rekognition.detect_labels(
        Image={'Bytes': decoded_content},
        MaxLabels=10,
        MinConfidence=80
    )

    rekognition_labels = [label['Name'] for label in rekognition_response['Labels']]
    print("rekognition_labels:", rekognition_labels)

    # Extract custom metadata labels
    metadata = s3.head_object(Bucket=bucket, Key=key)
    custom_labels = metadata['ResponseMetadata']['HTTPHeaders'].get('x-amz-meta-customlabels', '').split(',')
    print("custom_labels:", custom_labels)
    all_labels = custom_labels + rekognition_labels

    print("all_labels:", all_labels)

    if all_labels:
        # Create document for ElasticSearch
        document = {
            "objectKey": key,
            "bucket": bucket,
            "createdTimestamp": datetime.now().isoformat(),
            "labels": all_labels
        }

        print("Indexing images")

        # Index the document
        es.index(
            index="photos",
            id=key,
            body=document,
            refresh=True
        )

        print("document:", document)
        print("Indexed document:", json.dumps(document))

    # Update the object in S3 with the original content
    time.sleep(10)  # Delay to ensure operations are completed
    s3.delete_object(Bucket=bucket, Key=key)
    s3.put_object(Bucket=bucket, Body=decoded_content, Key=key, ContentType='image/jpg')

    return {
        'statusCode': 200,
        'body': json.dumps('Photo indexed successfully')
    }