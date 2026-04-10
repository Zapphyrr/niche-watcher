from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from database import Base


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=False)
    content = Column(Text)
    source = Column(String(50), nullable=False)  # "blog1", "blog2", "blog3", "reddit"
    source_name = Column(String(255))
    likes = Column(Integer, default=0)
    published_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    week = Column(Integer)  # Week number (ISO)
    year = Column(Integer)
    
    def __repr__(self):
        return f"<Post {self.title}>"
