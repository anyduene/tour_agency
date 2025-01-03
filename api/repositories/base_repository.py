from django.core.exceptions import ObjectDoesNotExist

class BaseRepository:
    def __init__(self, model):
        self.model = model

    def get(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return None

    def all(self):
        return self.model.objects.all()

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance):
        if instance:
            instance.delete()
            return True
        return False
