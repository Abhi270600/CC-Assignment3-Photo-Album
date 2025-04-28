import json
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection

# Initialize Lex client
lex_client = boto3.client('lexv2-runtime', region_name='us-east-1')

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

# Lex configuration
BOT_ID = "4H8Q6R6UFR"
BOT_ALIAS_ID = "TSTALIASID"
LOCALE_ID = "en_US"


def lambda_handler(event, context):
    # Extract all slots with resolved values

    print("Event:", event)
    user_query = event["queryStringParameters"]["q"]
    print("User query:", user_query)


    lex_response = lex_client.recognize_text(
        botId=BOT_ID,
        botAliasId=BOT_ALIAS_ID,
        localeId=LOCALE_ID,
        sessionId="1234",
        text=user_query
    )

    print("Lex response:", lex_response)

    # Get interpreted values (normalized)
    slot_info = lex_response.get('sessionState', {}).get('intent', {}).get('slots', {})
    print("Slot info:", slot_info)

    extracted_labels = []

    for slot_name, slot_data in slot_info.items():
        if slot_data and 'value' in slot_data:
            slot_label = slot_data['value']['interpretedValue']

            if slot_label:
                extracted_labels.append(slot_label)

    print("All labels:", extracted_labels)

    image_metadata = []

    for label in extracted_labels:
        query = {
            "query": {
                "match": {
                    "labels": label
                }
            }
        }

        try:
            response = es.search(index="photos", body=query)
            hits = response['hits']['hits']

            if hits:
                for hit in hits:
                    if all(hit['_source']['objectKey'] != item['objectKey'] for item in image_metadata):
                        image_metadata.append(hit['_source'])

        except Exception as e:
            print("ElasticSearch error:", str(e))
            return {"statusCode": 500, "body": "Search failed"}

    print("Image metadata:", image_metadata)

    # Prepare HTTP response
    return {
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'statusCode': 200,
        'body': json.dumps(image_metadata)
    }

