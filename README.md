# AWS Lambda Layer Generator

AWS Lambda function uses only built-in libraries. In order to import 3rd-party libraries, one has to upload .zip file containing the desired libraries.
To learn more, visit [AWS Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) documentation.

This layer, depending on the size, can either be uploaded directly to the Lambda creation Layer or to S3 bucket.


## Dependencies

1. Docker
2. Zip
3. Python 3.6 or higher

## Google Analytics API Libraries Layer Creation

In this example, we are installing the following python libraries;

- oauth2client
- google-api-python-client
- pandas

1. Place the *service_account.json* in the parent directory. 
2. Edit the *create_layer.sh* for the desired libraries as well as for the appropriate python version.

3. Run the executable;

`sudo ./create_layer.sh`

4. Once done, upload the zip file, *layer.zip* to S3 bucket or directly to the Lambda Layer.
5. Copy and paste the *lambda_function.py* and change the values of the variables. This function reads a new object in a specified S3 prefix and uploads it to GA via Management API

## References:
1. [GA API CONNECT](https://serhiipuzyrov.com/2020/11/how-to-import-cost-data-into-google-analytics-using-python-and-api/)
2. [Lambda function import 3rd-party packages](https://dev.to/mmascioni/using-external-python-packages-with-aws-lambda-layers-526o)
3. [GA Management, Import Data API](https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/uploads/uploadData)
4. [GA Management, Sample Service Applications API](https://developers.google.com/analytics/devguides/config/mgmt/v3/quickstart/service-py)
