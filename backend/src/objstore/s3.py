from typing import BinaryIO, List

import boto3
from botocore.exceptions import ClientError

from src.config import ObjectStore
from src.errors import BioValidatorInternalError
from src.objstore.base import BaseStore


def _create_s3_resource(object_store_config: ObjectStore) -> None:
    aws_access_key_id=object_store_config.AWS_ACCESS_KEY_ID.get_secret_value()
    aws_secret_access_key=object_store_config.AWS_SECRET_ACCESS_KEY.get_secret_value()
    custom_url = object_store_config.CUSTOM_S3_URL
    if custom_url is None:
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        s3_resource = session.resource("s3")

    else:
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=custom_url,
        )
    return s3_resource

class S3Store(BaseStore):
    def __init__(self, object_store_config: ObjectStore):
        self._s3_resource = _create_s3_resource(object_store_config)

        self._bucket_name = object_store_config.BUCKET_NAME
        self._bucket = self._s3_resource.Bucket(self._bucket_name)

    def init(self) -> None:
        try:
            self._s3_resource.meta.client.head_bucket(Bucket=self._bucket_name)
        except ClientError as err:
            if err.response["Error"]["Code"] == "404":
                self._bucket = self._s3_resource.create_bucket(Bucket=self._bucket_name)
            else:
                raise BioValidatorInternalError(f"{str(err)}") from err

    def object_exists(self, path: str) -> bool:
        s3_object = self._bucket.Object(str(path))
        try:
            s3_object.load()
        except ClientError as exc:
            if exc.response["Error"]["Code"] == "404":
                return False
            raise exc
        return True

    def upload_object(self, content: BinaryIO, path: str):
        s3_object = self._bucket.Object(str(path))
        response = s3_object.put(Body=content)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise BioValidatorInternalError(
                f"Object with key {path} could not be put in store, code: {response['ResponseMetadata']['HTTPStatusCode']}"
            )

    def download_object(self, path: str) -> None | bytes:
        if not self.object_exists(path):
            return None

        s3_object = self._bucket.Object(str(path))
        return s3_object.get()["Body"].read()


    def list_objects(
        self, path: str
    ) -> List[str]:
        objects = self._s3_resource.list_objects_v2(Bucket=self._bucket_name, Prefix=path)
        object_keys = [obj["Key"] for obj in objects["Contents"]]
        return object_keys

    def list_basename(self, path: str):
        result = self._s3_resource.list_objects_v2(
            Bucket=self._bucket_name, Prefix=path, Delimiter="/"
        )
        return [
            obj.get("Prefix").split("/")[-2] for obj in result.get("CommonPrefixes")
        ]
