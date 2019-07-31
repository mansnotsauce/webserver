from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from boards.models import Result
from aimanager import AIManager
import os
import pydicom
import numpy as np
import png

@login_required
def home(request):
    allResults = Result.objects.all()
    user = request.user
    filteredResults = allResults.filter(user=user) 
    return render(request, 'home.html', {'results': filteredResults})

@login_required
def userupload(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        tempFile = '/home/webserver/webserver/temp/temp.dcm'
        with open (tempFile, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        image = pydicom.dcmread(tempFile)
        shape = image.pixel_array.shape
        # Convert to float to avoid overflow or underflow losses.
        image_2d = image.pixel_array.astype(float)
        # Rescaling grey scale between 0-255
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
        # Convert to uint
        image_2d_scaled = np.uint8(image_2d_scaled)
        imageName = image.SOPInstanceUID + '.png'
        destination = '/home/webserver/webserver/media/' + imageName
        # Write the PNG file
        with open(destination, 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)
        os.remove(tempFile)
        manager = AIManager(image)
        results = manager.run()
        return render(request, 'home.html')
    return render(request, 'userupload.html')
