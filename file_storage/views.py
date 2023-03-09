from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from google.cloud import storage
from users.models import Settings
from .models import File, Logo

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

@csrf_exempt
def upload_logo(request):
    if request.method == 'POST':
        print(request.FILES)
        user_id = request.POST.get('user_id')  # Assuming the user is authenticated
        logo = request.FILES.get('logo')
        print(request.FILES.get('logo'))

        if logo :
            settings_instance = Settings.objects.get(user_id=user_id)
            # Create a new File instance and save it to the database
            logo_instance = Logo(image=logo)
            logo_instance.save(settings = settings_instance)

            # Get the default Google Cloud Storage bucket
            client = storage.Client()
            bucket = client.get_bucket('vesta-users-files')

            # Define the path for the uploaded file in Google Cloud Storage
            
            filename = f"{logo_instance.image.name}"

            print("filename",filename)

            logo.seek(0)
            
            # Create a Blob object and upload the file to Google Cloud Storage
            blob = bucket.blob(filename)
            blob.upload_from_string(logo.read(), content_type=logo.content_type)

            # Get the public URL for the uploaded file
            file_url = blob.public_url

            # Update the File instance with the public URL
            logo_instance.file_url = file_url
            logo_instance.save()

            # add the file to the user settings model
            settings_instance.logo = logo_instance
            settings_instance.save()


            response_data = {'success': True, 'file_url': file_url}

          
            

            response_data = {'success': True, 'logo_url':file_url}
        else:
            response_data = {'success': False, 'error': 'No logo was received.'}
    else:
        response_data = {'success': False, 'error': 'Only POST requests are allowed.'}

    return JsonResponse(response_data)