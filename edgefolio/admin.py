"""Admin configuration."""

from django.contrib import admin

from edgefolio.models import Fund, FundReturn

admin.site.register(Fund)
admin.site.register(FundReturn)
