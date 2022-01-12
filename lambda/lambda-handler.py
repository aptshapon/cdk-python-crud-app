import boto3
from botocore.exceptions import ClientError
from custom_encoder import CustomEncoder
import json, logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("product-inventory")


def handler(event, context):
    logger.info(event)
    httpMethod = event["httpMethod"]
    path = event["path"]
    # if httpMethod == "GET" and path == "/health":
    #     response = buildResponse(200)
    if httpMethod == "GET" and path == "/product":
        response = getProduct(event["queryStringParameters"]["productId"])
    elif httpMethod == "GET" and path == "/products":
        response = getProducts()
    elif httpMethod == "POST" and path == "/product":
        response = saveProduct(json.loads(event["body"]))
    elif httpMethod == "PATCH" and path == "/product":
        requestBody = json.loads(event["body"])
        response = modifyProduct(
            requestBody["productId"],
            requestBody["updateKey"],
            requestBody["updateValue"],
        )
    elif httpMethod == "DELETE" and path == "/product":
        requestBody = json.loads(event["body"])
        response = deleteProduct(requestBody["productId"])
    else:
        response = buildResponse(404, "Not Found")
    return response


def getProduct(productId):
    try:
        response = table.get_item(Key={"productId": productId})
        if "Items" in response:
            return buildResponse(200, response["Items"])
        else:
            return buildResponse(404, {"Message": f"ProductID: {productId} not found"})
    except:
        logger.exception("Do your custome error handling here!")


def getProducts():
    try:
        response = table.scan()
        result = response["Items"]
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])
        body = {"products": result}
        return buildResponse(200, body)

    except:
        logger.exception("Do your custome error handling here!")


def saveProduct(requestBody):
    try:
        table.put_item(Items=requestBody)
        body = {"Operation": "SAVE", "Message": "SUCCESS", "Item": requestBody}
        return buildResponse(200, body)
    except:
        logger.exception("Do your custom error handling here!")


def modifyProduct(productId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={"productId": productId},
            UpdateExpression=f"set {updateKey} = :value",
            ExpressionAttributeValues={":value": updateValue},
            ReturnValues="Update_New",
        )
        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdatedAttributes": response,
        }
    except:
        logger.exception("Do your custom error handling here!")


def deleteProduct(productId):
    try:
        response = table.delete_item(
            Key={"productId": productId}, ReturnValues="ALL_OLD"
        )
        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "UpdatedAttributes": response,
        }
    except:
        logger.exception("Do your custom error handling here!")


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }
    if body is not None:
        response["body"] = json.dumps(body, cls=CustomEncoder)
    return response
