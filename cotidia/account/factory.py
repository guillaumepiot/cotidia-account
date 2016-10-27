import uuid
import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'account.User'

    uuid = factory.LazyAttribute(lambda o: uuid.uuid4())
    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
