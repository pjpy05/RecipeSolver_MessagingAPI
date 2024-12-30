import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json

class GoogleSheetsClient:
    def __init__(self, auth_json: str, spreadsheet_key: str, sheet_name: str):
        """
        :param auth_json: サービスアカウントJSONそのもの（文字列）
        :param spreadsheet_key: Googleスプレッドシートのキー
        :param sheet_name: 対象のシート名
        """
        self.auth_json = auth_json
        self.spreadsheet_key = spreadsheet_key
        self.sheet_name = sheet_name

        # 認証とシートの初期化
        self.client = self._authorize()
        self.sheet = self._get_worksheet()
        self.drive_service = self._build_drive_service()

    def _authorize(self):
        """Google Sheets APIの認証を行う。"""
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # JSON文字列を辞書に変換
        credentials_info = json.loads(self.auth_json)
        credentials = Credentials.from_service_account_info(credentials_info, scopes=scope)
        return gspread.authorize(credentials)

    def _get_worksheet(self):
        """スプレッドシートとシートを取得する。"""
        try:
            spreadsheet = self.client.open_by_key(self.spreadsheet_key)
            return spreadsheet.worksheet(self.sheet_name)
        except gspread.SpreadsheetNotFound:
            raise Exception(f"スプレッドシートが見つかりません: {self.spreadsheet_key}")
        except gspread.WorksheetNotFound:
            raise Exception(f"シートが見つかりません: {self.sheet_name}")

    def _build_drive_service(self):
        """Google Drive APIのサービスを構築する。"""
        # JSON文字列を辞書に変換
        credentials_info = json.loads(self.auth_json)
        credentials = Credentials.from_service_account_info(credentials_info)
        return build('drive', 'v3', credentials=credentials)
    
    def get_all_data(self) -> pd.DataFrame:
        """
        シート全体のデータを取得し、DataFrameに変換する。

        :return: pandas.DataFrame
        """
        data = self.sheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])

    def find_value_by_user_id_and_column(self, user_id: str, column_name: str):
        """
        # 使用例
        value = obj.find_value_by_user_id_and_column(user_id="1", column_name="name")
        """
        df = self.get_all_data()
        
        # user_idが一致する行を取得
        match = df[df['user_id'] == user_id]
        
        if not match.empty and column_name in df.columns:
            value = match.iloc[0][column_name]
            
            # 空白、未入力、またはNullの場合はNoneを返す
            if pd.isna(value) or (isinstance(value, str) and value.strip() == ''):
                return None
            return value
        return None

    def update_or_insert_row_by_user_id(self, user_id: str, update_data: dict):
        """
        指定したuser_idに該当する行を更新する。
        存在しない場合は新しい行を挿入する。

        :param user_id: 更新対象のユーザーID
        :param update_data: 更新するデータ (列名と値の辞書)
        """
        all_data = self.sheet.get_all_records()  # データ全取得
        for i, row in enumerate(all_data, start=2):  # シート上は2行目以降がデータ
            if row.get('user_id') == user_id:
                # user_idが存在する場合、データを更新
                for col, value in update_data.items():
                    cell = self.sheet.find(col)  # 更新対象の列を検索
                    if cell:
                        self.sheet.update_cell(i, cell.col, value)  # 該当セルを更新
                return

        # user_idが存在しない場合、新しい行を挿入
        headers = self.sheet.row_values(1)  # シートのヘッダーを取得
        new_row = [update_data.get(header, "") for header in headers]  # 新しい行のデータを準備
        self.sheet.append_row(new_row)  # 新しい行を末尾に追加

    """
    # クラスを初期化
    client = GoogleSheetsClient(
        auth_file="path/to/service-account.json",
        spreadsheet_key="your_google_spreadsheet_key",
        sheet_name="your_sheet_name"
    )

    # すべてのデータを取得
    df = client.get_all_data()
    print(df)

    # 特定のuser_idに該当する行を取得
    value = obj.find_value_by_user_id_and_column(user_id="1", column_name="name")

    # 特定のuser_idに該当する行を更新、なければ挿入
    update_data = {
        "user_id": "12345",
        "name": "John Doe",
        "email": "john@example.com"
    }
    sheet_manager.update_or_insert_row_by_user_id("12345", update_data)
    """

    # def duplicate_template(self, template_id: str, new_title: str) -> str:
    #     """
    #     テンプレートを複製して新しいスプレッドシートを作成する。

    #     :param template_id: テンプレートのスプレッドシートID
    #     :param new_title: 新しいスプレッドシートのタイトル
    #     :return: 複製されたスプレッドシートのID
    #     """
    #     copy_body = {'name': new_title}
    #     copied_file = self.drive_service.files().copy(
    #         fileId=template_id, body=copy_body).execute()
    #     return copied_file['id']

    # def share_sheet(self, sheet_id: str, user_email: str, role: str = 'writer'):
    #     """
    #     スプレッドシートを指定したユーザーに共有する。

    #     :param sheet_id: 共有するスプレッドシートのID
    #     :param user_email: 共有相手のメールアドレス
    #     :param role: 権限 ('reader', 'writer', など)
    #     """
    #     permission = {
    #         'type': 'user',
    #         'role': role,
    #         'emailAddress': user_email
    #     }
    #     self.drive_service.permissions().create(
    #         fileId=sheet_id,
    #         body=permission,
    #         fields='id'
    #     ).execute()

    def get_seasonings_sheet(self, sheet_id: str, sheet_name: str):
        """
        指定されたスプレッドシートとシート名にアクセスする。

        :param sheet_id: スプレッドシートのID
        :param sheet_name: シート名
        :return: gspread.Worksheetオブジェクト
        """
        spreadsheet = self.client.open_by_key(sheet_id)
        return spreadsheet.worksheet(sheet_name)

    def insert_seasonings_data(self, sheet_id: str, sheet_name: str, data: list):
        """
        指定されたユーザーシートにデータを書き込む。

        :param sheet_id: スプレッドシートのID
        :param sheet_name: シート名
        :param data: 書き込むデータ（2次元リスト形式）
        """
        sheet = self.get_seasonings_sheet(sheet_id, sheet_name)

        # 現在のシートデータを取得
        existing_data = sheet.get_all_values()

        # 見出し行が既に存在するか確認
        if existing_data and existing_data[0] == data[0]:
            # 見出し行をスキップ
            data_to_append = data[1:]
        else:
            # 見出し行を含めて書き込む
            data_to_append = data

        # 次の空行を計算
        next_row = len(existing_data) + 1

        # 各行を順に書き込む
        for i, row in enumerate(data_to_append):
            sheet.update(f'A{next_row + i}', [row])



    """

    # テンプレートを複製
    new_sheet_id = client.duplicate_template(
        template_id="template_spreadsheet_id",
        new_title="John_Doe_Data"
    )
    print(f"複製されたシートのID: {new_sheet_id}")

    # 新しいシートをユーザーに共有
    client.share_sheet(sheet_id=new_sheet_id, user_email="john.doe@example.com", role="writer")
    print("シートを共有しました。")

    # データの読み取り
    data = client.read_user_data(sheet_id=new_sheet_id, sheet_name="Sheet1")
    print(f"シートのデータ: {data}")

    # データの書き込み
    new_data = [
        ["user_id", "name", "score"],
        ["001", "John Doe", 95]
    ]
    client.write_user_data(sheet_id=new_sheet_id, sheet_name="Sheet1", data=new_data)
    print("データを書き込みました。")
    """