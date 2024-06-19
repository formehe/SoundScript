
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGBLOB

Base = declarative_base()

class Audio_TBL(Base):
    __tablename__ = 'audios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    audio_data = Column(LONGBLOB, nullable=False)

    def __repr__(self):
        return f"<Audios(description={self.description}, audio_data={len(self.audio_data)} bytes)>"