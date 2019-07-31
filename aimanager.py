# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 09:47:11 2019

@author: MBaer
"""
import pydicom
import psycopg2
import imf
import os
import django
import numpy as np
import png
#os.environ['DJANGO_SETTINGS_MODULE'] = 'webserver.settings'
#django.setup()
from boards.models import Result
from django.contrib.auth.models import User

class AIManager:
    
    
    def __init__(self, image):
        self.image = image
        
    def run(self):
        results = []
        if self.image.Modality == 'MG':
            result = imf.run()
            if result == 'Fail':
                results.append('Inframammary fold')
            else:
                results.append('Good')
        else:
            #Wrong SOP class
            results.append('Image not valid')
        return results
        
    def save_results(self, results):
        reason = ""
        for result in results:
            reason = reason + result + " "
        users = User.objects.all().filter(username='mattb')
        user = user[0]        
        shape = self.image.pixel_array.shape       
        # Convert to float to avoid overflow or underflow losses.
        image_2d = self.image.pixel_array.astype(float)        
        # Rescaling grey scale between 0-255
        image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0        
        # Convert to uint
        image_2d_scaled = np.uint8(image_2d_scaled)
        imageName = self.image.SOPInstanceUID + '.png'
        destination = '/home/webserver/webserver/media/images/' + imageName
        # Write the PNG file
        with open(destination, 'wb') as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)
        
        result = Result(user=user, img = imageName, sop_instance_uid=self.image.SOPInstanceUID, self.image.Modality, reason)
        result.save()
        #Old way
        #sql = 'INSERT INTO results VALUES(%s, %s, %s)'
        #conn = psycopg2.connect(database='Mammos', user='mbaer')
        #cur = conn.cursor()
        #reason = ""
        #for result in results:
        #    reason = reason + result + " "
        #cur.execute(sql, (self.image.SOPInstanceUID, self.image.Modality, reason))
        #cur.close()
        #conn.commit()
        #conn.close()
