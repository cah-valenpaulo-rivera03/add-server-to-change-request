import os
import dotenv

from config.settings import *

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

class Sharepoint365:
    def auth(self):
        sharepoint_url = SHAREPOINT_SITE_URL
        username = SHAREPOINT_USERNAME
        password = SHAREPOINT_PASSWORD

        client_credentials = UserCredential(username, password)
        conn = ClientContext(sharepoint_url).with_credentials(client_credentials)

        return conn

    def download_file(self, source_directory, file_name):
        conn = self.auth()
        destination_path = os.path.abspath(file_name)
        file_url = "{source_directory}/{file_name}"
        
        with open(destination_path, "wb") as target_file:
            file = conn.web.get_file_by_server_relative_url(file_url)
            file.download(target_file)
            conn.execute_query()

    def list_files(self, source_directory):
        conn = self.auth()
        directory = ctx.web.get_folder_by_server_relative_url(source_directory)
        files = directory.files
        conn.load(files)
        conn.execute_query()

        return files
        