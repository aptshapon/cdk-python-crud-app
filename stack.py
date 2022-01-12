from constructs import Construct
from aws_cdk import Stack, aws_lambda as _lambda, aws_apigateway as _apigw


class CrudStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend = _lambda.Function(
            self,
            "ApiCrudLambda",
            handler="lambda-handler.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
        )

        api = _apigw.LambdaRestApi(self, "product-api",
            handler=backend
        )
        # api.root.add_method("ANY")
        products = api.root.add_resource("products")
        products.add_method("GET")

        product = api.root.add_resource("product")
        product.add_method("GET")
        product.add_method("POST")
        product.add_method("PATCH")
        product.add_method("DELETE")
