import boto3
import json
import uuid
import zipfile
import os
import shutil
from shutil import copyfile
from dulwich.repo import Repo
from dulwich import porcelain

s3_client = boto3.client('s3')
print (s3_client)

codecommit_client = boto3.client('codecommit')
print (codecommit_client)

def lambda_handler(event, context):
	print ('local repo creation started')
	local_repo = Repo.init('/tmp/css_download', mkdir=True)
	print ('local repo creation successful')
	s3 = boto3.resource('s3')
	print ('local repo creation ended')
	for record in event['Records']:
		bucket = record['s3']['bucket']['name']
		key = record['s3']['object']['key']
		print(key)
		break
	s3local = '/tmp/aws.zip'
	s3final = '/tmp/css_download'
	s3.Bucket(bucket).download_file(key,s3local)
	list=os.listdir('/tmp/')
	print (list)
	zip_ref = zipfile.ZipFile(s3local, 'r')
	zip_ref.extractall(s3final)
	zip_ref.close()
	list=os.listdir('/tmp/css_download/')
	print (list)
	print ('Stage started')
	Repo.stage(local_repo,list)
	print ('Commit started')
	Repo.do_commit(local_repo,b"new commit", committer=b"sandeep <sandeep.s.k@accenture.com>")
	print ('Push started')
	porcelain.push("/tmp/css_download","https://sandeep.s.k-at-574112450463:N2YDDTf+71bXZUNZjiF6YKFDGYXgPsIhI1GxbIVm+Wg=@git-codecommit.us-east-2.amazonaws.com/v1/repos/css-repo","master")
	print ('Push successful')