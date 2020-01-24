from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

redalimentar_folder = "RED ALIMENTAR"
datos_folder = "datos"


def authenticate():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    return gauth


def upload_to_drive(directorystr):
    gauth = authenticate()
    drive = GoogleDrive(gauth)
    folders = drive.ListFile({
        'q': "title='" + redalimentar_folder + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()

    for folder in folders:
        if folder["title"] == redalimentar_folder:
            folder_id = folder["id"]
            folders = drive.ListFile({
                'q': "title='" + datos_folder + "' and mimeType='application/vnd.google-apps.folder' and trashed=false and parents='" + folder_id + "'",
            }).GetList()

    for folder in folders:
        if folder["title"] == datos_folder:
            date_name = os.path.basename(directorystr)
            date_folder = drive.CreateFile({
                "title": date_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [{"id": folder["id"]}],
            })
            date_folder.Upload()
            date_folder_id = date_folder["id"]
            data_tuples = list(os.walk(directorystr))
            if len(data_tuples) > 0:
                first_layer = data_tuples[0]
                region_ids = []
                for region_string in first_layer[1]:
                    region_folder = drive.CreateFile({
                        "title": region_string,
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": [{"id": date_folder_id}],
                    })
                    region_folder.Upload()
                    region_ids.append(region_folder["id"])

                rest_of_walk = data_tuples[1:]

                region_counter = 0
                for folderName, subfolders, filenames in rest_of_walk:
                    for filename in filenames:
                        #create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        with open(filePath, "r") as file:
                            file_drive = drive.CreateFile({
                                "title": "{}".format(os.path.basename(file.name)),
                                "parents": [{"id": region_ids[region_counter]}],
                            })
                            file_drive.SetContentString(file.read())
                            file_drive.Upload()
                    region_counter += 1
