### Requirements 
- Python 
- Google Drive API Credentials (credentials.json)
- Google Drive API Permissions (Note: Please message your gmail)


### Setup
- Add the  `credentials.json` file to the root of the project
- Install requirements: `pipenv install`

### To run
```
python -m scrape --prompt "surrealism art" --end 5 --folder-id 12FolderID12 
```

- Arguments:
    - `--prompt`: Required
    - `--start`: Optional. Starting call index
    - `--end`: Required. Ending call index
    - `--folder-id`: Required. Google Drive ID
    - `--endpoint`: Optional. Default is already provided
    - `--delay`: Optional. Implemented to not overwhelm server

- You will be asked to login into your Google account if it is your first run

### Notes
- Make sure the `--folder-id` is the ID. For example, if the url is `https://drive.google.com/drive/folders/133232ABC?fbclid=ABCDEF`, the ID is only `133232ABC`. Do not include other params
- The endpoint returns 9 images per call. For ~2000 images, this means the `--end` arg should be set to 223
- The local copy of the file is deleted after upload

### Sample Logs
<img width="764" height="520" alt="Screenshot 2025-09-07 at 03 51 45" src="https://github.com/user-attachments/assets/cef8ef56-6c91-47b5-8080-3d9fe9ca13d4" />

