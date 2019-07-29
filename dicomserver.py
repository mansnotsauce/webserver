# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:38:11 2019

@author: MBaer
"""
import pydicom
from pydicom.dataset import Dataset
from pynetdicom import AE, evt, PYNETDICOM_IMPLEMENTATION_UID, PYNETDICOM_IMPLEMENTATION_VERSION
from pynetdicom.sop_class import DigitalMammographyXRayImagePresentationStorage
from pynetdicom.sop_class import DigitalMammographyXRayImageProcessingStorage
from django.contrib.auth.models import User
from aimanager import AIManager

def handle_store(event):
    
    ds = event.dataset
    ds.file_meta = event.file_meta
    manager = AIManager(ds)
    result = manager.run()
    #ds.dcmwrite('C:/Users/MBaer/Desktop/aiservice/itworks', write_like_original=False)   
    return result

handlers = [(evt.EVT_C_STORE, handle_store)]

ae = AE()
ae.add_supported_context(DigitalMammographyXRayImagePresentationStorage)
ae.add_supported_context(DigitalMammographyXRayImageProcessingStorage)
ae.start_server(('127.0.0.1', 11112), evt_handlers=handlers)
