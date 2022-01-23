from typing import Any
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
    file_expire_days: int = 1
    # ドキュメントの自動生成を有効化
    enable_docs: bool = False

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        fastapi_kwargs: dict[str, Any] = {
        }
        if not self.enable_docs:
            fastapi_kwargs.update({
                'docs_url': None,
                'openapi_url': None,
                'redoc_url': None
            })
        return fastapi_kwargs

    class Config:
        env_prefix = 'TFS_'


settings = Settings()
