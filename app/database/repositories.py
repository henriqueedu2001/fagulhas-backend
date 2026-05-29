from datetime import datetime
from typing import *
from app.database.database_manager import Database


class Repository:
    def __init__(self, db: Database):
        self.db = db


    def create_work(self, title: str, date: datetime, category: str, synopsis: str, edition_number: int, idiom: str, isbn: str, pages_num: int, tags: List[str], filenames: Dict):
        # creating the work entity in the work table
        create_work_query = """
            INSERT INTO work(title, date, category)
            VALUES(%s, %s, %s)
        """

        self.db.execute(create_work_query, (title, date, category))
        work_id = self.db.cursor.lastrowid

        # creating the edition in the edition table
        create_edition_query = """
            INSERT INTO edition(work_id, edition_number, idiom, title, date, synopsis,  isbn, pages_num, views, likes, shares)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        work_id
        if not edition_number: edition_number = 1
        if not idiom: idiom = 'PT-BR'
        if not isbn: isbn = None
        views, likes, shares = 0, 0, 0
        
        self.db.execute(create_edition_query, (work_id, edition_number, idiom, title, date, synopsis, isbn, pages_num, views, likes, shares))
        edition_id = self.db.cursor.lastrowid

        # creating the tags in the tags table
        create_tags_query = """
            INSERT INTO tags(work_id, tag_name)
            VALUES(%s, %s)
        """

        tags = [(work_id, tag) for tag in tags]

        self.db.execute_many(create_tags_query, tags)

        # saving the file paths in the database
        create_files_query = """
            INSERT INTO files(work_id, edition_id, filepath, category)
            VALUES(%s, %s, %s, %s)
        """

        print(filenames)
        for key, value in filenames.items():
            filepath = value
            file_category = key
            if filepath is not None:
                self.db.execute(create_files_query, (work_id, edition_id, filepath, file_category))

        # committing to the database       
        self.db.commit()

        return work_id, edition_id