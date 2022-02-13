import factory
from sqlalchemy.orm import Session
import bcrypt


from sql_app.database import SessionLocal, Base, engine
from sql_app.models import User

Base.metadata.create_all(bind=engine)

session: Session = SessionLocal()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session
        sqlalchemy_get_or_create = ('email',)


    email = factory.Faker('ascii_safe_email')

    @factory.lazy_attribute
    def password(self):
        return bcrypt.hashpw(self.password_unsafe.encode(), bcrypt.gensalt())

    class Params:
        password_unsafe = 'test'
