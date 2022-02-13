import datetime
from typing import List
import factory
from sqlalchemy.orm import Session
from mdgen import MarkdownPostProvider
from markdown_it import MarkdownIt
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

session: Session = SessionLocal()

md = MarkdownIt()

class HTMLPostProvider(MarkdownPostProvider):
    def html_post(self, **kwargs):
        markdown_post = self.post(**kwargs)
        try:
            return md.render(markdown_post)
        except IndexError:
            print("Md renderer error")
            return "md crashed"


factory.Faker.add_provider(HTMLPostProvider)

class AdvertisementFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Advertisement
        sqlalchemy_session = session
        sqlalchemy_get_or_create = ('id',)

    id = factory.sequence(lambda n: n)

    owner = factory.Faker(
            "random_element", elements=factory.SelfAttribute("..available_user_ids")
        )

    category_id = factory.Faker(
            "random_element", elements=factory.SelfAttribute("..available_category_ids")
        )
    
    date_start = factory.Faker(
            "date_time_between_dates",
            datetime_start=factory.SelfAttribute("..date_min"),
            datetime_end=factory.SelfAttribute("..date_max"),
        )

    date_end = factory.Faker(
            "date_time_between_dates",
            datetime_start=factory.SelfAttribute("..date_start"),
            datetime_end=factory.SelfAttribute("..date_max"),
        )

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("sentence", nb_words=8)
    content = factory.Faker("html_post", size="small")


    views = factory.Faker("random_int", min=factory.SelfAttribute("..views_min"), max=factory.SelfAttribute("..views_max"))

    class Params:
        available_user_ids: List[int] = None
        available_category_ids: List[int] = None
        views_min = 0
        views_max = 200
        date_min: datetime.datetime = None
        date_max: datetime.datetime = None


class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Category
        sqlalchemy_session = session
        sqlalchemy_get_or_create = ('id',)

    id = factory.sequence(lambda n: n)

    @factory.lazy_attribute
    def name(self):
        return str(self.id)

    @factory.lazy_attribute
    def parent_id(self):
        if self.id <= self.root_categories:
            return None
        return self.id // 2

    class Params:
        root_categories = 7