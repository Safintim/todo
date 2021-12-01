import factory


class BaseFactory(factory.Factory):
    class Meta:
        model = dict


class TaskFactory(BaseFactory):
    title = factory.Faker('pystr', max_chars=150)
    description = factory.Faker('text', max_nb_chars=255)
    list_id = None


class TaskListFactory(BaseFactory):
    title = factory.Faker('pystr', max_chars=150)
