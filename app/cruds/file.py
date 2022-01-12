from typing import List, Tuple, Optional
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
import models.file as file_model


async def create_file(db: AsyncSession, file: file_model.File) -> file_model.File:
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file


async def get_files(db: AsyncSession, expiration: int) ->  List[file_model.File]:
    result: Result = await db.execute(
        select(file_model.File)
            .filter(file_model.File.upload_epoch_ms >= expiration)
            .order_by(file_model.File.id)
    )
    all: List[Tuple[file_model.File]] = result.all()

    # タプルのリストが返されるのでフラットにする
    return [item for l in all for item in l]


async def get_file(db: AsyncSession, file_id: str) -> Optional[file_model.File]:
    result: Result = await db.execute(
        select(file_model.File).filter(file_model.File.id == file_id)
    )
    file: Optional[Tuple[file_model.File]] = result.first()

    # 要素が一つであってもタプルで返されるのでので１つ目の要素を取り出す
    return file[0] if file is not None else None


async def remove_file(db: AsyncSession, original: file_model.File) -> None:
    await db.delete(original)
    await db.commit()


async def get_expired_files(db: AsyncSession, expiration: int) ->  List[file_model.File]:
    result: Result = await db.execute(
        select(file_model.File).filter(file_model.File.upload_epoch_ms < expiration)
    )
    all: List[Tuple[file_model.File]] = result.all()

    # タプルのリストが返されるのでフラットにする
    return [item for l in all for item in l]
