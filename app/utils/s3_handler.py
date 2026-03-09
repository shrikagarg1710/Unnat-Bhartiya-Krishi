import os
import io
import boto3
from typing import List

class S3Handler:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client(service_name="s3", region_name=os.environ.get("AWS_REGION_NAME"), aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"), aws_secret_access_key=os.environ.get("AWS_ACCESS_SECRET_KEY"))
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
    
    def upload_file(self, file) -> bool:
        """Upload file to S3"""
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, file.name)
            return True
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False
    
    def upload_file_bytes(self, file_bytes: bytes, filename: str) -> bool:
        """Upload raw bytes to S3."""
        try:
            self.s3_client.upload_fileobj(io.BytesIO(file_bytes), self.bucket_name, filename)
            return True
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            return False
        
    def list_files(self) -> List[str]:
        """List all files in S3"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            files = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    key: str = obj["Key"]
                    filename = key.split("/")[-1]
                    ext = filename.rsplit(".", 1)[-1].upper() if "." in filename else "UNKNOWN"
                    size_kb = round(obj["Size"] / 1024, 2)
                    files.append({"filename": filename, "ext": ext, "size_kb": size_kb})
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file from S3 by filename."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=filename)
            return True
        except Exception as e:
            print(f"Error deleting from S3: {e}")
            return False