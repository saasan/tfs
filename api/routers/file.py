import math
import os
import shutil
import aiofiles
from typing import List
from fastapi import APIRouter, Path, Depends, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
import ulid
import api.cruds.file as file_crud
import api.models.file as file_model
import api.schemas.file as file_schema
from api.db import get_db
from settings import settings


router = APIRouter(
    prefix='/api/files',
    tags=['Files API']
)


def format_bytes(bytes: int) -> str:
    """
    ファイルサイズを読みやすいかたち(KB, MB, ...)にする

    :param bytes: ファイルサイズ(バイト数)
    :return: ファイルサイズを読みやすいかたちにした文字列
    """
    if bytes == 0: return '0 Bytes'

    k: int = 1024
    prefix: tuple[str] = ('Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')

    # bytesが1024の何乗かを求める
    powers: int = math.floor(math.log(bytes, k))
    # 求めた冪乗で割る
    kb: float = bytes / (k ** powers)

    digits: int = 3 if kb < 1000 else 4
    format_str: str = '{kb:.' + str(digits) + 'g} {prefix}'

    return format_str.format(kb=kb, prefix=prefix[powers])


def save_upload_file(upload_file: UploadFile, file_id: str) -> int:
    """
    アップロードされたファイルを保存する

    :param upload_file: アップロードされたファイル
    :param file_id: ファイルのid
    :return: アップロードされたファイルのサイズ(バイト数)
    """
    # 念の為ファイルの先頭へシーク
    upload_file.file.seek(0)

    # 拡張子
    ext: str = os.path.splitext(upload_file.filename)[1]
    # ファイルを保存するパス
    path: str = os.path.join(settings.files_dir, file_id + ext)

    try:
        with open(path, 'wb') as f:
            shutil.copyfileobj(upload_file.file, f)
    finally:
        size: int = upload_file.file.tell()
        upload_file.file.close()

    return size


async def remove_upload_file(file_id: str, filename: str) -> None:
    """
    アップロードされたファイルを削除する

    :param file_id: アップロードされたファイルのid
    :param filename: ファイル名
    """
    # 拡張子
    ext: str = os.path.splitext(filename)[1]
    # ファイルが保存されているパス
    path: str = os.path.join(settings.files_dir, file_id + ext)

    # 非同期で使えるようラップ
    isfile = aiofiles.os.wrap(os.path.isfile)

    # ファイルを削除
    if await isfile(path):
        await aiofiles.os.remove(path)


async def remove_expired_file(db: AsyncSession) -> None:
    """
    期限が過ぎたファイルを削除する
    """
    now: int = ulid.new().timestamp().int
    expiration: int = now - (settings.file_expire_days * 24 * 60 * 60 * 1000)

    files: List[file_model.File] = await file_crud.get_expired_files(db, expiration)

    for file in files:
        # ファイルを削除
        await remove_upload_file(file.id, file.name)
        # DBから削除
        await file_crud.remove_file(db, original=file)


@router.post('/', response_model=file_schema.File)
async def upload_file(
    upload_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # ULID
    new_ulid: ulid.ULID = ulid.new()
    file_id: str = new_ulid.str
    # ファイルを保存
    size: int = save_upload_file(upload_file, file_id)
    human_readable_size: str = format_bytes(size)

    file: file_model.File = file_model.File(
        id=file_id,
        upload_epoch_ms=new_ulid.timestamp().int,
        name=upload_file.filename,
        size=size,
        human_readable_size=human_readable_size
    )

    try:
        result = await file_crud.create_file(db, file)
    except:
        # DBへの追加に失敗したらファイルを削除
        await remove_upload_file(file_id, upload_file.filename)

    return result


@router.get('/', response_model=List[file_schema.File])
async def list_files(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # バックグラウンドで期限が過ぎたファイルを削除
    background_tasks.add_task(remove_expired_file, db)

    return await file_crud.get_files(db)


@router.get('/{file_id}')
async def get_file(
    file_id: str = Path(..., min_length=26, max_length=26, regex='^[A-Z0-9]{26}$'),
    db: AsyncSession = Depends(get_db)
):
    file: file_model.File = await file_crud.get_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail='File not found')

    # 拡張子
    ext: str = os.path.splitext(file.name)[1]
    # ファイルが保存されているパス
    path: str = os.path.join(settings.files_dir, file_id + ext)

    response: FileResponse = FileResponse(
        path=path,
        media_type=settings.download_mimetype,
        filename=file.name
    )

    # 非同期で使えるようラップ
    isfile = aiofiles.os.wrap(os.path.isfile)

    # ファイルを送信
    if await isfile(path):
        return response
    else:
        raise HTTPException(status_code=404, detail='File not found')


@router.delete('/{file_id}', response_model=None)
async def remove_file(
    file_id: str = Path(..., min_length=26, max_length=26, regex='^[A-Z0-9]{26}$'),
    db: AsyncSession = Depends(get_db)
):
    file: file_model.File = await file_crud.get_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail='File not found')

    # ファイルを削除
    await remove_upload_file(file.id, file.name)

    return await file_crud.remove_file(db, original=file)


@router.get('/{file_id}/info', response_model=file_schema.File)
async def get_file_info(
    file_id: str = Path(..., min_length=26, max_length=26, regex='^[A-Z0-9]{26}$'),
    db: AsyncSession = Depends(get_db)
):
    file: file_model.File = await file_crud.get_file(db, file_id=file_id)
    if file is None:
        raise HTTPException(status_code=404, detail='File not found')

    return file
