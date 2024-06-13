import os.path
import pandas as pd
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def pushToSheets(animeList):
  creds = None
  # CODE EXTRACT FROM GOOGLE BEGINS #
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          r"C:\Users\Ade\Desktop\Personal\Python\Project Portfolio\secrets\anime_data_secret.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  # CODE EXTRACT FROM GOOGLE ENDS #
      
  try:
    service = build("sheets", "v4", credentials=creds)

    # create new spreadsheet
    currentTimeStamp = time.localtime()
    sheetName = "animeList" + str(time.strftime('%Y%m%d:%H%M',currentTimeStamp))
    spreadsheet = {"properties": {"title": sheetName}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )

    spreadsheetId = spreadsheet.get("spreadsheetId")
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")

    # add row data to spreadsheet
    dataFrame = pd.DataFrame(data=animeList)
    columnTitles = dataFrame.keys().tolist()
    arrayOfValues = dataFrame.values.tolist()
    
    # prepend column titles to arrayOfValues so the titles are added first in the sheet
    completeValues = [columnTitles, *arrayOfValues]

    body = {"values": completeValues}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheetId,
            range="A1",
            valueInputOption="USER_ENTERED",
            body=body,
        )
        .execute()
    )

    print(f"{result.get('updatedCells')} cells updated.")
    return result
  
  except HttpError as err:
    print(err)
