from django.db import models
from users.models import Settings


# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

def logo_upload_path(instance, filename):
    pass

class Logo(models.Model):
    image = models.ImageField(upload_to='logos')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name
    
    def save(self, *args, **kwargs):
        settings = kwargs.pop('settings', 0)
        if settings :
            # Fetch the related Settings instance from the settings parameter
    
            # Get the user from the related Settings instance
            user_id = settings.user.id
            # Construct the path using the user_id and current timestamp
            upload_path = f'{user_id}/{self.image.name}'
            print(upload_path)
            self.image.name = upload_path
        super().save(*args, **kwargs)