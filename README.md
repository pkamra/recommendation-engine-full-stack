# recommendation-engine-full-stack



- Diagrammatic flow of our architecture


#1) Login as Admin to the AWS Account in which the setup will be done.
#2) Open Cloud9. Choose a t3.small machine, connectivity via SSM. 
#3) Let's download the code now via 
>>  git clone https://github.com/pkamra/recommendation-engine-full-stack.git
>>  sudo yum install git-lfs
>>  cd recommendation-engine-full-stack
>>  git lfs fetch origin main (Is this needed)
>>  git lfs pull origin

#4) Decompress the zip file representing our raw data as follows
>>  cd data
>>  jar xvf csv_files.zip 

#5) Some cleanup inside the data folder before we upload it to s3.
>>  rm -rf __MACOSX/ csv_files.zip 

This is how my cleaned data folder looks now
>> Admin:~/environment/recommendation-engine-full-stack/data (main) $ ls -la
>> drwxrwxr-x 2 ec2-user ec2-user  55 Apr  7 20:10 csv_files
>> drwxrwxr-x 3 ec2-user ec2-user  68 Apr  7 21:54 kmeans_movieoutput
>> drwxrwxr-x 2 ec2-user ec2-user  25 Apr  7 21:54 localui
>> drwxrwxr-x 2 ec2-user ec2-user  90 Apr  7 21:54 python_notebook


#5) Upload the raw data to s3, so that it can be used by our sagemaker notebook environment
>> Admin:~/environment/recommendation-engine-full-stack/data $ `aws s3 cp --recursive . s3://awesome2023-656151913794/`

#6)On upload to S3 this is how it looks 
![plot](s3structureafterupload.png)

#7)Open Amazon Sagemaker. Click on Sagemaker Studio.Click on Create a Sagemaker domain.Set domain name as awesome2023-recommendation
Choose the default user profile.Create New IAM Role  for permissions associated with teh User Profile. In the popup choose any S3 bucket.Note down the name of the newly created Role.  AmazonSageMaker-ExecutionRole-20230318T214355 

#8)The creation of the new domain will take a few minutes.
<While this is going on we will go over a few slides>
<Creation of the new domain takes about 5 minutes>

#9)Go to user profiles and click on launch->Studio (takes about 4 minutes)

#10)Go to File -> New Terminal
>>sagemaker-user@studio$ aws s3 cp s3://awesome2023-545313841491/python_notebook/AWSWomenInEngineering2023_V1.ipynb .

#11)Double click the jupyter file.It will start the kernel. <takes about 5 mins>


#12)Deployment of the sklearn using the sagemaker migration toolkit since it is a not a native sagemaker endpoint , but a  custom model being deployed in the sagemaker environment.
    -  Open the Cloud9 environment , go to the folder sagemaker-migration-toolkit
    >> pip install wheel
    >> Do steps in README.md 
        >>python setup.py bdist_wheel
        >>pip install dist/sagemaker_migration_toolkit-0.0.1-py3-none-any.whl
        >>Go to IAM and find the IAM role for Sagemaker of the format `arn:aws:iam::<ACCOUNT>:role/service-role/AmazonSageMaker-ExecutionRole-20210412T095523`
        >>run the command `sagemaker_migration-configure --module-name sagemaker_migration.configure`
    >> Go to testing folder 
        >>Download the model.joblib from sagemaker notebook and upload it to your Cloud9 Console.
        >>Go to the testing/sklearn folder and execute `python test.py`
    >>Paste the sagemaker endpoint of sklearn in DEPLOY_INSTRUCTIONS.md and execute the script as follows on the command prompt in cloud 9
        >> `sed -i s@SAGEMAKER-ENDPOINT@sm-endpoint-sklearn-2023-03-23-22-58-49@g localtest.sh`
        >> Execute `sh localtest.sh`
        >>Check if you have got scaled responses in prediction_response.json

#13) Go back to Glue and create a default database before continuing to execute further cells in the Jupyter notebook.
#14) After all cells are executed , let us create the API's using an open source tool called chalice which makes the creation of Lambda and API gateway very easy.
    >> Lets open a brand new Cloud 9 environment (TODO)
    >> Purpose of this API is to take in categories that you are interested in and then call the 2 sagemaker endpoints behind teh scenes and return a cluster number
#15) On the New Cloud 9 Instance do the following
    >> `aws s3 cp --recursive  s3://awesome2023-xxxx/apis_for_sagemaker_models/ .`
    >> `pip install chalice`
    >> `chalice new-project sagemaker-apigateway-lambda-chalice`
    >> To see hidden files in Cloud9 IDE , click on the gear icon and Click on Show environment root and show hidden files
    Then in the .chalice folder config.json file, add "automatic_layer": true, 
    >>add requirements.txt and app.py contents to the root of the project from the chalice_custom_scaling_kmeans_api folder. 
    >> export AWS_DEFAULT_REGION=us-east-1
    >> Create role Cloud9_LambdaExecutionRole with Admin access. this role is mentioned as the lambda execution role in config.json
    >> `chalice deploy`

#16) Test with Postman (Optional)

Post payload is {"startYear":"2015","runtimeMinutes":"100","Thriller":"1","Music":"0","Documentary":"0","Film-Noir":"0","War":"0","History":"0","Animation":"0","Biography":"0","Horror":"0","Adventure":"1","Sport":"0","News":"0","Musical":"0","Mystery":"0","Action":"1","Comedy":"0","Sci-Fi":"1","Crime":"1","Romance":"0","Fantasy":"0","Western":"0","Drama":"0","Family":"0","averageRating":"7","numVotes":"50"}

#17) Execute `chalice new-project query-athena-boto3`
   >> add requirements.txt and app.py contents to the root of the project from the chalice_query_api folder.  
   >>  Update role in config.json for this project
   >>create query_results folder in the S3 bucket
   >>sed -i s@BUCKET_NAME@<your bucket name>@g app.py
   >> Execute `chalice deploy`





