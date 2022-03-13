from werkzeug.utils import secure_filename
from config import s3_client


def upload_file(file, bucket, folder):
    filename = secure_filename(file.filename)
    directory = folder + "/" + file.filename
    print(bucket)
    try:
        s3_client.upload_fileobj(
            file,
            bucket,
            directory
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return file.filename


def list_files(bucket):
    contents = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            # print(item)
            contents.append(item)
    except Exception as e:
        pass
    return contents


def show_image(bucket):
    # location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': bucket, 'Key': item['Key']},
                                                             ExpiresIn=100)
            # print("[DATA] : presigned url = ", presigned_url)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[DATA] : The contents inside show_image = ", public_urls)
    return public_urls
