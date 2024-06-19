from sqlalchemy import create_engine,exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import reflection
from dao.audio_tbl import *
from config.secret import secret

class Audio_DAO:
    def __init__(self, config:secret) -> None:
        DATABASE_URL = """mysql+pymysql://{}:{}@{}/{}?connect_timeout=10""".format(
                            config.get("mysql", "user_name"),
                            config.get("mysql", "passwd"),
                            config.get("mysql", "host_name"),
                            config.get("mysql", "db_name"))
        
        self.engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle = -1)
        
        if not reflection.Inspector.from_engine(self.engine).has_table("audios"):
            Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        
    def add_audio(self, description, audio_data):
        try:
            new_content = Audio_TBL(description=description, audio_data=audio_data)
            self.session.add(new_content)
            self.session.commit()
            return True
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()
        
        return False

    def get_audio(self, content_id):
        try:
            return self.session.query(Audio_TBL).filter(Audio_TBL.id == content_id).first()
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()

    def get_audio_by_description(self, description):
        try:
            return self.session.query(Audio_TBL).filter(Audio_TBL.description == description).first()
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()

    def update_audio(self, content_id, new_description=None, new_audio_data=None):
        try:
            content = self.session.query(Audio_TBL).filter(Audio_TBL.id == content_id).first()
            if content:
                if new_description:
                    content.description = new_description
                if new_audio_data:
                    content.audio_data = new_audio_data
                self.session.commit()
                return True
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()
        return False

    def delete_audio(self, content_id):
        try:
            content = self.session.query(Audio_TBL).filter(Audio_TBL.id == content_id).first()
            if content:
                self.session.delete(content)
                self.session.commit()
                return True
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()
        return False
    
    def get_all_audio_by_description(self, description):
        try:
            if description == "*":
                return self.session.query(Audio_TBL.id, Audio_TBL.description).all()
            else:
                return self.session.query(Audio_TBL.id, Audio_TBL.description).filter(Audio_TBL.description.like('%' + description + '%')).all()
        except exc.OperationalError as e:
            self.engine.dispose()  # 释放连接
            self.session = self.Session()