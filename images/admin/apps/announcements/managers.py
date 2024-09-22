# ruff: noqa: SLF001

from mptt.managers import TreeManager
from mptt.querysets import TreeQuerySet
from parler.managers import TranslatableManager
from parler.managers import TranslatableQuerySet


class CategoryQuerySet(TranslatableQuerySet, TreeQuerySet):
    def as_manager(self, cls):
        # make sure creating managers from querysets works.
        manager = CategoryManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager

    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class CategoryManager(TreeManager, TranslatableManager):
    _queryset_class = CategoryQuerySet
