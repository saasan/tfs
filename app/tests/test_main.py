import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import starlette.status
from freezegun import freeze_time
from db import get_db, Base
from main import app


ASYNC_DB_URL = 'sqlite+aiosqlite:///:memory:'


@pytest.fixture
async def async_client() -> AsyncClient:
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest.mark.asyncio
@freeze_time('2021-01-02 03:04:05')
async def test_api_crud(async_client):
    # ULIDの長さ
    ULID_LENGTH: int = 26
    # POSTパラメータの名前
    PARAM_NAME: str = 'upload_file'
    # アップロードするファイルの内容
    FILE_CONTENT: bytes = b'hoge\n\xe3\x81\xbb\xe3\x81\x92\n'
    # アップロードするファイルのidのタイムスタンプ部分
    FILE_ID_TIMESTAMP: str = '01EV0GTN48'
    # ファイルのアップロード時間
    FILE_UPLOAD_EPOCH_MS: int = 1609556645000
    # アップロードするファイル名
    FILE_NAME: str = 'test.txt'
    # アップロードするファイルのサイズ
    FILE_SIZE: int = len(FILE_CONTENT)
    # アップロードするファイルの読みやすいサイズ
    FILE_HUMAN_READABLE_SIZE: str = str(FILE_SIZE) + ' Bytes'
    # アップロードするファイルのMIMEタイプ
    FILE_MIMETYPE: str = 'text/plain'
    # テストのためアップロードするファイル
    FILES = { PARAM_NAME: (FILE_NAME, FILE_CONTENT, FILE_MIMETYPE) }

    # Upload File
    response = await async_client.post('/api/files/', files=FILES)
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj['id']) == ULID_LENGTH
    assert response_obj['id'][:10] == FILE_ID_TIMESTAMP
    assert response_obj['upload_epoch_ms'] == FILE_UPLOAD_EPOCH_MS
    assert response_obj['name'] == FILE_NAME
    assert response_obj['size'] == FILE_SIZE
    assert response_obj['human_readable_size'] == FILE_HUMAN_READABLE_SIZE

    # ファイルのidを保存
    file_id = response_obj['id']

    # List Files
    response = await async_client.get('/api/files/')
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj) == 1
    assert len(response_obj[0]['id']) == ULID_LENGTH
    assert response_obj[0]['id'] == file_id
    assert response_obj[0]['upload_epoch_ms'] == FILE_UPLOAD_EPOCH_MS
    assert response_obj[0]['name'] == FILE_NAME
    assert response_obj[0]['size'] == FILE_SIZE
    assert response_obj[0]['human_readable_size'] == FILE_HUMAN_READABLE_SIZE

    # Get File Info
    response = await async_client.get(f'/api/files/{file_id}/info')
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert len(response_obj['id']) == ULID_LENGTH
    assert response_obj['id'] == file_id
    assert response_obj['upload_epoch_ms'] == FILE_UPLOAD_EPOCH_MS
    assert response_obj['name'] == FILE_NAME
    assert response_obj['size'] == FILE_SIZE
    assert response_obj['human_readable_size'] == FILE_HUMAN_READABLE_SIZE

    # Get File
    response = await async_client.get(f'/api/files/{file_id}')
    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.content == FILE_CONTENT

    # Remove File
    response = await async_client.delete(f'/api/files/{file_id}')
    assert response.status_code == starlette.status.HTTP_200_OK
