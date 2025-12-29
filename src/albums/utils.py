import zipfile
import os
from django.core.files.base import ContentFile
from .models import Photo

VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}

def handle_zip_upload(zip_file, album):
    """
    Extracts images from a zip file and creates Photo objects for the given album.
    """
    try:
        with zipfile.ZipFile(zip_file, 'r') as z:
            # Get list of files, sorted to maintain some order
            file_list = sorted(z.namelist())
            
            for i, filename in enumerate(file_list):
                # Skip directories and hidden files
                if filename.endswith('/') or filename.startswith('__MACOSX') or filename.startswith('.'):
                    continue
                
                # Check extension
                ext = os.path.splitext(filename)[1].lower()
                if ext not in VALID_IMAGE_EXTENSIONS:
                    continue
                
                # Read file data
                file_data = z.read(filename)
                
                # Create Photo object
                photo = Photo(album=album, order=i)
                
                # Save image content
                # We use the basename of the file to avoid directory structure issues in the filename
                base_filename = os.path.basename(filename)
                photo.image.save(base_filename, ContentFile(file_data), save=True)
                
    except zipfile.BadZipFile:
        raise ValueError("Invalid zip file")

def handle_folder_upload(files, album):
    """
    Processes a list of uploaded files and creates Photo objects for the given album.
    """
    # Sort files by name to maintain order
    files = sorted(files, key=lambda x: x.name)
    
    for i, file_obj in enumerate(files):
        # Check extension
        ext = os.path.splitext(file_obj.name)[1].lower()
        if ext not in VALID_IMAGE_EXTENSIONS:
            continue
        
        # Create Photo object
        # We use the original filename, but might want to sanitize it
        photo = Photo(album=album, order=i, filename=os.path.basename(file_obj.name))
        photo.image.save(file_obj.name, file_obj, save=True)
