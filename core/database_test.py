from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, Numeric, Date, DateTime, Time, Interval, Enum, ARRAY, JSON, UUID, LargeBinary, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from enum import Enum as PythonEnum

SQLALCHEMY_DATABASE_URL = "postgeswl://user:password@postgrsserver/db"

# SQLALCHEMY_DATABASE_URL = "sqlite"///./sqlite.db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# CRETES BASE CLASS FOR DECLARING TABLES
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(length=30))
    last_name = Column(String(length=30), nullable=True)
    age = Column(Integer())
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, fisrt_name={self.first_name}, last_name={self.last_name})"

# TO CREATE TABLES AND DATABASE
Base.metadata.create_all(engine)

# CREATES SESSION FROM SESSIONLOCAL FACTORY PATTERN
session = SessionLocal()

# INSERTING DATA
anthon = User(first_name="anthon", age=31)
session.add(anthon)
session.commit()
session.refresh(anthon)

# BULK INSERT
maryam = User(first_name="maryam", age=27)
arousha = User(first_name="arousha", age=6)
users = [maryam, arousha]
session.add_all(users)
session.commit()

# RETRIEVE ALL DATA
all_users = session.query(User).all()
print(all_users)

# RETRIEVE DATA WITH FILTER
filterd_user = session.query(User).filter_by(first_name="ali").one_or_none()
print(filterd_user)

# UPDATE A RECORD OF DATA
anthon.last_name = "Ahmoham"
session.commit()

# DELETE A RECORD OF DATA
session.delete(anthon)
session.commit()

class RelationsTable(Base):
    ___tablename__ = 'relations'

    # One-to-one RELATIONSHIPS
    profile = relationship("Profile", uselist=False, back_populates="users")

    # Ont-to-many RELATIONSHIPS
    addresses = relationship("Address", back_populates="users")

    # Many-to-one RELATIONSHIPS
    orders = relationship("Order", back_populates="users")

    # Many-to-many RELATIONSHIPS
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    # YOU CAN SEE IMPLEMENTATION EXAMPLE OF ALL THEM IN CURRENT CODE BUTTOM PART

class UserType(PythonEnum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class SampleModel(Base):
    __tablename__ = "sample_model"

    id = Column(Integer, primary_key=True)

    string_field = Column(String)
    text_filed = Column(Text)
    boolean_field = Column(Boolean)
    Integer_field = Column(Integer)
    float_field = Column(Float)
    numeric_field = Column(Numeric(10, 2))
    date_field = Column(Date)
    datetime_field = Column(DateTime)
    time_field = Column(Time)
    interval_field = Column(Interval)
    enum_field = Column(Enum(UserType))
    array_field = Column(ARRAY(Integer))
    json_field = Column(JSON)
    uuid_field = Column(UUID)
    foreign_key_field = Column(Integer, ForeignKey('related_table.id'))
    birany_field = Column(LargeBinary)


# ---- ONE TO MANY RALATIONSHIP EXMAPLE ----
'''You place a ForeignKey on the “many” side (the Post table) and use relationship() on both sides to make navigation easy.'''
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    author = relationship("User", back_populates="posts")


# ---- MANY TO ONE RELATIONSHIP EXAMPLE ----
'''Inverse of One-to-Many realtionship.'''
'''You place a ForeignKey on the “many” side (the Post table) and use relationship() on both sides to make navigation easy.'''


# ---- ONE TO ONE RELATIONSHIP EXAMPLE ----
'''A specialized case of One-to-Many where the “many” side is restricted to only one record'''
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    profile = relationship("Profile", back_populates="user")


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="profile", uselist=False)

# ---- MANY TO MANY RELATIONSHIPS EXAMPLE ----
'''Requires an Association Table (or Link Table) because neither side can store a simple foreign key.'''
'''Imagine a library system where one author can write many books, and one book can be written by many authors (co-authored).'''
# The association table
# It has no primary key of its own, just two Foreign Keys
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True),
)

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    
    # link to Author
    authors = relationship("Author", secondary=book_authors, back_populates="books")

class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    # link to Book
    books = relationship("Book", secondary=book_authors, back_populates="authors")

# USAGE EXAMPLE
a1 = Author(name="J.R.R. Tolkien")
a2 = Author(name="Christopher Tolkien")
b1 = Book(title="The Silmarillion")

# Link them naturally
b1.authors.append(a1)
b1.authors.append(a2)

