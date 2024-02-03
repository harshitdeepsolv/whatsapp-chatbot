from google.cloud import storage
import os
from time import time


# Your Google Cloud Storage credentials (download JSON from GCP Console)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/harshitsingh/Documents/Developer/vocal-spirit-407819-9e41c2b936a3.json'

# Path to the local audio file
local_audio_path = '/Users/harshitsingh/Documents/Developer/WhatsApp-Chatbot/output.ogg'

# Google Cloud Storage bucket name
gcs_bucket_name = 'twilio_space'

def upload_to_gcs(local_path, gcs_bucket, gcs_blob_name):
    """Uploads a file to the GCS bucket and returns the public URL."""
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_blob_name)

    # Upload the file
    blob.upload_from_filename(local_path)

    # Make the blob publicly accessible with uniform bucket-level access
    blob.make_public()

    # Return the public URL
    return blob.public_url


# # Generate a unique GCS blob name based on the current timestamp
# gcs_blob_name = f'audio_uploaded.ogg'
#
# # Upload the audio file to GCS and get the public URL
# gcs_audio_url = upload_to_gcs(local_audio_path, gcs_bucket_name, gcs_blob_name)
#
#
#
# print(f"GCS Audio URL: {gcs_audio_url}")
