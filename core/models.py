from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Name', max_length=255, null=True, blank=True, unique=True)
    parent = models.ForeignKey('self', verbose_name='Parent',
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True,
                               related_name='children')

    def __str__(self):
        return self.name

    def get_all_children(self, container=None, include_self=False):
        if container is None:
            if include_self:
                container = [self]
            else:
                container = []
        result = container
        for child in self.children.all():
            result.append(child)
            if child.children.count() > 0:
                child.get_all_children(result)
        return result