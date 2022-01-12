#!/usr/bin/env python3

import aws_cdk as cdk

from stack import CrudStack


app = cdk.App()
CrudStack(app, "cdk-python-crud")

app.synth()
