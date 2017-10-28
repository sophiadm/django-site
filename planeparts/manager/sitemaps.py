from django.contrib.sitemaps import Sitemap
from .models import PartType

class SiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return PartType.objects.all()
