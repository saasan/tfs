from pydantic import BaseSettings


class Settings(BaseSettings):
    # ログ出力先などに使用する内部的なアプリ名
    app_name: str = 'tfs'
    # UIに使用するアプリ名
    app_name_ui: str = '一時ファイル置き場'
    # 接続するDBのURL
    async_db_url: str = 'mysql+aiomysql://root@db:3306/tfs?charset=utf8mb4'
    db_url: str = 'mysql+pymysql://root@db:3306/tfs?charset=utf8mb4'
    # ファイルを保存するディレクトリ
    files_dir: str = '/var/lib/tfs'
    # ファイルダウンロード時のMIMEタイプ
    download_mimetype: str = 'application/octet-stream'
    # ファイルの保存日数
    expiration_days: int = 1

settings = Settings()
