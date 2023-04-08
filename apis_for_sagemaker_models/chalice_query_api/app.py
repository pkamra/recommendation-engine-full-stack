import os
from chalice import Chalice
# Environment Variables
CLUSTERNO = 5
DATABASE = 'default'
# S3 Constant
S3_OUTPUT = 's3://BUCKET_NAME/query-results/'
# Number of Retries
RETRY_COUNT = 10
app = Chalice(app_name='query-athena-boto3')

def dummy():
    import boto3
    """
    Collection of all s3.client() functions.
    The sole purpose is to force Chalice to generate the right permissions in the policy.
    Does nothing and returns nothing.
    """
    try:
        s3 = boto3.client('s3')
        s3.put_object()
        s3.download_file()
        s3.get_object()
        s3.list_objects_v2()
        s3.get_bucket_location()
    except:
        print("Error in s3 premission granting")
    else:
        print("No Error in s3 premission grating")

def glueinitialize():
    import boto3
    try:
        client = boto3.client('glue',region_name='us-east-1')
        client.get_tables( DatabaseName = "default" )
    except Exception as e:
        print("Error in glue premission granting")
        print(e)
    else:
        print("No Error in glue premission granting")
    

@app.route('/', methods=['POST'], content_types=['application/json'], cors=True)
def index():
    import time
    import boto3
    dummy()
    glueinitialize()
    client = boto3.client('athena')
    input_json = app.current_request.json_body['cluster'] 
    CLUSTERNO = float(input_json)
    print("Cluster is :: ")
    print(CLUSTERNO)
    # query variable with two environment variables and a constant
    query = f"""
    SELECT * FROM clusters WHERE cluster ={CLUSTERNO} order by averagerating , numvotes asc limit 10;
    """
    response = client.start_query_execution(
          QueryString=query,
          QueryExecutionContext={ 'Database': DATABASE },
          ResultConfiguration={'OutputLocation': S3_OUTPUT}
    )
    query_execution_id = response['QueryExecutionId']
    # Get Execution Status
    for i in range(0, RETRY_COUNT):
    # Get Query Execution
        query_status = client.get_query_execution(
              QueryExecutionId=query_execution_id
        )
        exec_status = query_status['QueryExecution']['Status']['State']
        if exec_status == 'SUCCEEDED':
            print(f'Status: {exec_status}')
            break
        elif exec_status == 'FAILED':
            raise Exception(f'STATUS: {exec_status}')
        else:
            print(f'STATUS: {exec_status}')
            time.sleep(i)
    else:
        client.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('TIME OVER')
    # Get Query Results
    result = client.get_query_results(QueryExecutionId=query_execution_id)
    print(result['ResultSet']['Rows'])
    # Function can return results to your application or service
    # return result['ResultSet']['Rows']
    return {'results': result['ResultSet']['Rows']}


