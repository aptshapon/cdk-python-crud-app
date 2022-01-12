#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_python_crud.cdk_python_crud_stack import CdkPythonCrudStack


app = cdk.App()
CdkPythonCrudStack(app, "cdk-python-crud")

app.synth()
