import os
from camera4kivy import Preview
from os.path import dirname, join
from android_permissions import AndroidPermissions

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager

import cloudmersive_barcode_api_client
from cloudmersive_barcode_api_client.rest import ApiException

'''
import time
import json
import urllib.request
from urllib.request import urlopen
'''

class WindowManager(ScreenManager):
    pass

class MainMenu(Screen):
    pass

class CameraMenu(Screen):
    pass

class FilesMenu(Screen):
    
    def show(self):
        '''
        try:
            app_folder = os.path.dirname(os.path.abspath(__file__))
            self.ids.sample.text = app_folder
            dir = '/storage/emulated/0/DCIM/'
            os.chdir(dir)
        except: 
            notification = MyPopup()
            notification.open()
        '''

        try:
            
            import os
            from datetime import datetime
            from os.path import exists, join
            from pathlib import Path
            from threading import Thread
            from camera4kivy.preview_common import PreviewCommon

            from android.storage import app_storage_path, primary_external_storage_path
            from android.runnable import run_on_ui_thread
            from android import mActivity, api_version
            from jnius import autoclass, PythonJavaClass, java_method
            
            GL_TEXTURE_EXTERNAL_OES = autoclass(
                'android.opengl.GLES11Ext').GL_TEXTURE_EXTERNAL_OES
            Environment = autoclass('android.os.Environment')
            CameraX = autoclass('org.kivy.camerax.CameraX')
            if api_version >= 29:
                ContentValues = autoclass('android.content.ContentValues')
                MediaStoreMediaColumns =\
                    autoclass('android.provider.MediaStore$MediaColumns')
                MediaStoreImagesMedia =\
                    autoclass('android.provider.MediaStore$Images$Media')
                FileInputStream = autoclass('java.io.FileInputStream')
                FileUtils        = autoclass('android.os.FileUtils')
            
            #######################################
            # Storage Location
            #######################################

            storage = ''.lower()
            if storage not in ['private', 'shared']:
                storage = 'shared'
            self.private_storage = storage == 'private'
            self.file_storage = self.private_storage or api_version < 29
            
            message = f' api_version: {api_version} \n storage: {storage} \n self.private_storage: {self.private_storage} \n self.file_storage: {self.file_storage} \n app_storage_path(): {app_storage_path()} \n Environment.DIRECTORY_DCIM: {Environment.DIRECTORY_DCIM} \n primary_external_storage_path(): {primary_external_storage_path()} \n join(primary_external_storage_path(),Environment.DIRECTORY_DCIM): {primary_external_storage_path(),Environment.DIRECTORY_DCIM}'
            # self._app_name(): {self._app_name()}
            self.ids.sample.text = message

            # message2 = f'{primary_external_storage_path()}{chr(47)}{Environment.DIRECTORY_DCIM}'
            message2 = '/storage/emulated/0/DCIM/C4K'
            self.ids.sample2.text = message2

            photos_dir = f'{message2}/{datetime.now().strftime("%Y_%m_%d")}'

            os.chdir(photos_dir)
            self.ids.sample2.text = f'{os.getcwd()} ???'

            message3 = '\n'.join(os.listdir(os.getcwd()))
            self.ids.sample3.text = f'{message3}'

            photos = os.listdir(os.getcwd())
            last_photo = photos[len(photos) - 1]
            
            image_file = f'{photos_dir}/{last_photo}'
            self.ids.sample4.text = f'{photos_dir}/{last_photo}'

            # Configure API key authorization: Apikey
            configuration = cloudmersive_barcode_api_client.Configuration()
            configuration.api_key['Apikey'] = 'b03ab10c-1230-4603-86b4-ff651286b21b'

            # create an instance of the API class
            api_instance = cloudmersive_barcode_api_client.BarcodeScanApi(cloudmersive_barcode_api_client.ApiClient(configuration))
            image_file = f'{photos_dir}/{last_photo}'

            
            api_response = api_instance.barcode_scan_image(image_file)
            value = str(api_response)
            values = value.split(',')
            bar_code = values[1]
            bar_code = bar_code.replace("'raw_text': ", '')
            bar_code = bar_code.replace("'", '')
            self.ids.sample5.text = bar_code

            '''
            headers = {
            'X-Cosmos-Token': 'aqmwRtMmeYgiBpNbmdMnyw',
            'Content-Type': 'application/json',
            'User-Agent': 'Cosmos-API-Request'
            }

            bar_code = bar_code.lstrip()
            base_url = 'https://api.cosmos.bluesoft.com.br/gtins/'
            base_url += bar_code
            base_url += '.json'
            request = urllib.request.Request(base_url, None, headers)
            response = urllib.request.urlopen(request)
            data_content = json.loads(response.read())
            print(json.dumps(data_content, indent=4))
            '''

        except:
            notification = MyPopup()
            notification.open()

class MyPopup(Popup):
    pass
    
class MyApp(App):

    def build(self):
        return Builder.load_file('screen.kv')
    
    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None

if __name__ == '__main__':
    MyApp().run()