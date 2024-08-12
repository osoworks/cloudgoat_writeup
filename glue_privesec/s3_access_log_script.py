import boto3
import json
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    try:
        # S3 버킷의 모든 객체 나열
        response = s3.list_objects_v2(Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5')
        
        # 객체 목록을 JSON으로 변환
        objects_json = json.dumps([{
            'Key': obj['Key'],
            'LastModified': obj['LastModified'].isoformat(),
            'Size': obj['Size']
        } for obj in response.get('Contents', [])], default=str)
        
        # JSON을 base64로 인코딩
        encoded_json = base64.b64encode(objects_json.encode()).decode()
        
        # 결과를 S3에 저장 (파일 이름으로 인코딩된 내용 사용)
        s3.put_object(
            Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5',
            Key=f's3_log_{encoded_json[:250]}.txt',  # 파일 이름 길이 제한으로 인해 처음 250자만 사용
            Body='S3 log stored in filename'
        )
        
        print("S3 log saved in filename")
        return {
            'statusCode': 200,
            'body': json.dumps('S3 log saved to S3')
        }
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        # 오류 메시지를 S3에 저장
        s3.put_object(
            Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5',
            Key=f'error_log_{base64.b64encode(error_message.encode()).decode()[:250]}.txt',
            Body='Error log stored in filename'
        )
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }

if __name__ == "__main__":
    lambda_handler({}, None)

