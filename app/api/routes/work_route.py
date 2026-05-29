from datetime import datetime
from pathlib import Path
from typing import *
from pydantic import BaseModel
from fastapi import APIRouter, Form, HTTPException, UploadFile, File, Depends, Query
from app.modules.file_handler import *
from app.schemas.work_schemas import *
from app.database.database_manager import *
from app.database.repositories import *

router = APIRouter()


@router.post('/work/new')
async def register_work(
    title: str = Form(...),
    date: datetime = Form(...),
    category: str = Form(...),
    synopsis: str = Form(...),
    edition_number: int = Form(...),
    idiom: str = Form(...),
    isbn: Optional[str] = Form(None),
    pages_num: int = Form(...),
    tags: list[str] = Form(...),
    work_pdf: UploadFile = File(None),
    work_txt: UploadFile = File(None),
    work_latex: UploadFile = File(None),
    work_json: UploadFile = File(None),
    work_thumb: UploadFile = File(None),
    db: Database = Depends(get_database)
) -> RegisterWorkResponse:
    """Creates a work in the backend

    Args:
        title (str, optional): Title of the work. Defaults to Form(...).
        date (datetime, optional): Date of the work. Defaults to Form(...).
        category (str, optional): Category of the work (poem, short story etc.). Defaults to Form(...).
        synopsis (str, optional): Synopsis of the work. Defaults to Form(...).
        edition_number (int, optional): The edition number of the work. Defaults to Form(...).
        idiom (str, optional): The idiom of the work. Defaults to Form(...).
        isbn (Optional[str], optional): the ISBN of the work. Defaults to Form(None).
        pages_num (int, optional): The number of the pages of the work. Defaults to Form(...).
        tags (list[str], optional): the work tags. Defaults to Form(...).
        work_pdf (UploadFile, optional): the work pdf file. Defaults to File(None).
        work_txt (UploadFile, optional): the work txt file. Defaults to File(None).
        work_latex (UploadFile, optional): the work latex file. Defaults to File(None).
        work_json (UploadFile, optional): the work json file. Defaults to File(None).
        work_thumb (UploadFile, optional): the work thumb file. Defaults to File(None).
        db (Database, optional): the database. Defaults to Depends(get_database).

    Returns:
        RegisterWorkResponse: _description_
    """
    repo = Repository(db)

    base_filename = f'{date.year}-{date.month:02d}-{date.day:02d} - {title}'

    work_pdf_filepath = f'{base_filename}.pdf' if work_pdf else None
    work_txt_filepath = f'{base_filename}.txt'if work_txt else None
    work_latex_filepath = f'{base_filename}.zip'if work_latex else None
    work_json_filepath = f'{base_filename}.json'if work_json else None
    work_thumb_filepath = f'{base_filename}.{get_file_extension(work_thumb)}' if work_thumb else None

    filenames = {
        'work_pdf': work_pdf_filepath,
        'work_txt': work_txt_filepath,
        'work_latex': work_latex_filepath,
        'work_json': work_json_filepath,
        'work_thumb': work_thumb_filepath,
    }

    work_id, edition_id = repo.create_work(title, date, category, synopsis, edition_number, idiom, isbn, pages_num, tags, filenames)

    if work_pdf: await save_file_from_endpoint(file=work_pdf, filename=work_pdf_filepath)
    if work_txt: await save_file_from_endpoint(file=work_txt, filename=work_txt_filepath)
    if work_latex: await save_file_from_endpoint(file=work_latex, filename=work_latex_filepath)
    if work_json: await save_file_from_endpoint(file=work_json, filename=work_json_filepath)
    if work_thumb: await save_file_from_endpoint(file=work_thumb, filename=work_thumb_filepath)

    return RegisterWorkResponse(work_id=work_id, edition_id=edition_id)