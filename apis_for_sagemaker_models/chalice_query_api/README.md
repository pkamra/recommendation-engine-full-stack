>>Purpose of this API is to return back the set of data (in this case movies) belonging to a specific cluster


>>pip install chalice
>>chalice new-project query-athena-boto3
>>add requirements.txt and app.py contents to the root of the project
>>create query_results folder in the S3 bucket
>>sed -i s@BUCKET_NAME@<your bucket name>@g app.py
>>chalice deploy
If permissions are not enough while doing "chalice deploy" then there are do options 
either go back to teh AWS console and find the IAM role of the lambda function and add the missing permission or
in the Cloud9 console, go to Settings->AWS Settings ->Turn off AWS manged temporaray credentials
by following teh instructions in https://lightrun.com/answers/aws-chalice-bug-chalice-deploy-fails-to-discover-required-permissions-for-lambda-iam-role about adding the role in the config.json as follows

{
  "version": "2.0",
  "app_name": "example-app",
  "manage_iam_role": false,
  "iam_role_arn": "arn:aws:iam::XXXX:role/service-role/S3_read_access",
  "stages": {
    "dev": {
      "api_gateway_stage": "api"
    }
  }
}


