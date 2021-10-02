from pydantic import BaseSettings


class Settings(BaseSettings):
    # ページのタイトル
    page_title: str = '一時ファイル置き場'
    # 接続するDBのURL
    async_db_url: str = 'mysql+aiomysql://root@db:3306/tfs?charset=utf8mb4'
    db_url: str = 'mysql+pymysql://root@db:3306/tfs?charset=utf8mb4'
    # ファイルを保存するディレクトリ
    files_dir: str = '/var/lib/tfs'
    # ファイルダウンロード時のMIMEタイプ
    download_mimetype: str = 'application/octet-stream'
    # ファイルの保存日数
    expiration_days: int = 1

    class Config:
        env_prefix = 'TFS_'


settings = Settings()
