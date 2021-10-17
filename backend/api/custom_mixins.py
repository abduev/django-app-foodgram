from django.db import transaction
from rest_framework import mixins


class AtomicCreateModelMixin(mixins.CreateModelMixin):
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AtomicUpdateModelMixin(mixins.UpdateModelMixin):
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class AtomicDestroyModelMixin(mixins.DestroyModelMixin):
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class AtomicModelViewSetMixin(AtomicUpdateModelMixin,
                              AtomicCreateModelMixin,
                              AtomicDestroyModelMixin):
    pass
