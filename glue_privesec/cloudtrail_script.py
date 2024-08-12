import boto3
import json

def process_cloudtrail_logs(bucket_name, log_file_key, output_bucket):
    s3 = boto3.client('s3')

    # CloudTrail 로그 파일 읽기
    log_content = s3.get_object(Bucket=bucket_name, Key=log_file_key)['Body'].read().decode('utf-8')
    log_data = json.loads(log_content)

    # 로그 데이터에서 특정 정보를 추출
    # 예를 들어, 모든 이벤트의 타입을 추출하는 코드:
    event_types = [event['eventName'] for event in log_data['Records']]

    # 추출한 정보를 JSON 형태로 변환하여 저장
    extracted_info = json.dumps(event_types, indent=4)
    s3.put_object(Bucket=output_bucket, Key='extracted_cloudtrail_events.json', Body=extracted_info)

    print("CloudTrail 로그 처리 완료, 결과가 저장되었습니다.")

# 실행할 때 사용할 변수들
bucket_name = 'cg-data-from-web-glue-privesc-cgidfmohi6zro5'
log_file_key = 'cloudtrail_error.txt'  # 처리할 로그 파일
#output_bucket = 'your-output-bucket'  # 결과를 저장할 S3 버킷
output_bucket = 'cg-data-from-web-glue-privesc-cgidfmohi6zro5'  # 이미 접근 가능한 버킷으로 변경


process_cloudtrail_logs(bucket_name, log_file_key, output_bucket)

