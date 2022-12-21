from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    group_id = Column(Integer, server_default="2", nullable=False)

    group_id = Column(Integer, ForeignKey("UserGroups.id"), nullable=False)


class UserGroup(Base):
    __tablename__ = "UserGroups"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)


class ProjectState(Base):
    __tablename__ = "ProjectStates"

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)


class TaskState(Base):
    __tablename__ = "TaskStates"

    id = Column(Integer, primary_key=True, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    
    state_id = Column(Integer, ForeignKey("ProjectStates.id"), nullable=False)

    state = relationship("ProjectState")


class Task(Base):
    __tablename__ = "Tasks"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    active = Column(Boolean, server_default='TRUE', nullable=False)
    project_id = Column(Integer, ForeignKey("Projects.id", ondelete="CASCADE"), nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    created_by_user_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)  

    state_id = Column(Integer, ForeignKey("TaskStates.id"), nullable=False)

    state = relationship('TaskState')
    owner = relationship('User')

