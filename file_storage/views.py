from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from google.cloud import storage

from .models import File

@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
    
        user_id = request.POST.get('user_id')  # Assuming the user is authenticated
        file = request.FILES.get('file')
        if file:
            # Create a new File instance and save it to the database
            file_instance = File(file=file)
            file_instance.save()

            # Get the default Google Cloud Storage bucket
            client = storage.Client()
            bucket = client.get_bucket('vesta-users-files')

            # Define the path for the uploaded file in Google Cloud Storage
            filename = f"{user_id}/{file_instance.file.name}"

            # Create a Blob object and upload the file to Google Cloud Storage
            blob = bucket.blob(filename)
            blob.upload_from_string(file.read(), content_type=file.content_type)

            # Get the public URL for the uploaded file
            file_url = blob.public_url

            # Update the File instance with the public URL
            file_instance.file_url = file_url
            file_instance.save()

            response_data = {'success': True, 'file_url': file_url}
        else:
            response_data = {'success': False, 'error': 'No file was received.'}
    else:
        response_data = {'success': False, 'error': 'Only POST requests are allowed.'}

    return JsonResponse(response_data)
