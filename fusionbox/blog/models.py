import datetime
import collections

from django.db import models
from django.core.cache import cache
from django.db.models.signals import post_save
from django_extensions.db.fields import AutoSlugField
from django.utils.datastructures import SortedDict
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User  # NOQA

import tagging
import tagging.fields
import tagging.managers

from ckeditor.fields import RichTextField

from fusionbox import behaviors
from fusionbox.db.models import QuerySetManager

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ['^ckeditor\.fields\.RichTextField'])
add_introspection_rules([], ["^tagging\.fields\.TagField"])


class Blog(behaviors.Timestampable, behaviors.SEO, behaviors.Publishable):
    """
    Base model for blog entries. Uses
    :class:`fusionbox.db.models.QuerySetManager` as as its primary manager.
    """
    slug = AutoSlugField(populate_from='title')
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, related_name='blogs')
    summary = models.TextField()
    body = RichTextField()
    tags = tagging.fields.TagField()
    image = models.ImageField(blank=True, upload_to='blog_icons')

    objects = QuerySetManager()
    tagged = tagging.managers.ModelTaggedItemManager()

    class Meta:
        ordering = ('created_at', )

    def __unicode__(self):
        return self.title

    class QuerySet(behaviors.AdminSearchableQueryset):
        """
        Custom QuerySet class implementing ``publish`` and ``year_month_group``
        queryset methods
        """
        search_fields = ('title', 'summary', 'body', 'tags')

        def published(self):
            """
            duplicated from :class:`fusionbox.behaviors.Publishable` because we
            need a method, not an extra manager
            """
            return self.filter(is_published=True, publish_at__lte=datetime.datetime.now())

        def year_month_groups(self):
            """
            returns a dictionary of year -> (dictionary of month -> list of objects)
            """
            res = collections.defaultdict(lambda: collections.defaultdict(list))
            # this does too many queries, because all the tags are fetched. it
            # should use defer('tags'), but that causes a bug. See the
            # BlogTest.test_year_month_groups for a test that'll fail when
            # defer is used here.
            for obj in self:
                res[obj.publish_at.year][obj.publish_at.month].append(obj)

            sorted_result = SortedDict()
            # defaultdicts don't work right in django templates (.items # resolves as ['items'])
            # so convert to normal dicts
            for k in sorted(res):
                sorted_result[k] = SortedDict([
                    (k_, res[k][k_]) for k_ in sorted(res[k])
                ])
            return sorted_result

    @models.permalink
    def get_absolute_url(self):
        return ('blog:fusionbox.blog.views.detail', (), {'slug': self.slug})


def update_cache_version(*args, **kwargs):
    cache.add('fusionbox.blog.all_blogs.version', 0)
    cache.incr('fusionbox.blog.all_blogs.version')

post_save.connect(update_cache_version, sender=User)
post_save.connect(update_cache_version, sender=Blog)
