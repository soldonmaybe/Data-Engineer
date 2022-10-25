# cek package
try:
    from google.cloud import storage
    import urllib.request   
    from urllib.request import Request, urlopen

except Exception as e:
    print('This module is not available{}'.format(e))

# bikin client
storage_client = storage.Client.from_service_account_json('firm-pentameter-363006-e587f51df26f.json')

# bucket
PROJECT_ID = 'firm-pentameter-363006'
BUCKET_NAME = 'wfwijaya-fellowship'
DESTINATION_FILENAME = 'yellow-taxi-trip-data-2019-01.csv'

# source file
SOURCE_FILENAME = f'https://drive.google.com/file/d/1KOrSm7L7ualrexGVG-DKnz-VJZH3XA7d/view?usp=sharing'

# upload file to GCP
def upload_blob(BUCKET_NAME, SOURCE_FILENAME, DESTIONATION_FILENAME):
    #requesting file
    file = urllib.request.urlopen(SOURCE_FILENAME)
    # file = Request.urlopen(SOURCE_FILENAME, headers={'User-Agent': 'Mozilla/5.0'})
    #create bucket
    bucket = storage_client.get_bucket(BUCKET_NAME)
    #destination file name
    blob = bucket.blob(DESTINATION_FILENAME)
    #upload GCP
    blob.upload_from_string(file.read(), content_type='csv')

upload_blob(BUCKET_NAME, SOURCE_FILENAME, DESTINATION_FILENAME)

print('Upload Complete')