"""Edgefolio models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

import pandas as pd

from model_utils import Choices


class Fund(models.Model):
    """A fund."""

    STRATEGIES = Choices(('multi_arbitrage', _('Multi Arbitrage')),
                         ('fixed_income', _('Fixed Income')),
                         ('long_short_equity', _('Long Short Equity')),
                         ('event_driven', _('Event Driven')))

    REGION_EXPOSURES = Choices(('global_exposure', _('Global')),
                               ('us', _('US')),
                               ('asia', _('Asia')))

    name = models.TextField(unique=True)
    strategy = models.CharField(choices=STRATEGIES, max_length=100)
    region_exposure = models.CharField(choices=REGION_EXPOSURES,
                                       max_length=100)

    def __str__(self):
        """Cast to string."""
        return self.name

    def get_returns(self):
        """Get series of returns."""
        returns = self.returns_series.order_by('month').all()
        return pd.Series((r.percentage for r in returns),
                         index=pd.DatetimeIndex((r.month for r in returns)))

    def get_cumulative_returns(self):
        """Get series of cumulative returns."""
        returns = self.get_returns()
        prev_return = 1
        for month, percentage in returns.items():
            returns[month] = prev_return * (1 + percentage)
            prev_return = returns[month]

        return returns


class FundReturn(models.Model):
    """Return from a fund at the end of a month."""

    MONTH_FORMAT = '%b %Y'

    fund = models.ForeignKey(Fund, on_delete=models.PROTECT,
                             related_name='returns_series')
    month = models.DateField()
    percentage = models.FloatField()

    def __str__(self):
        """Cast to string."""
        return '{} {} at {}'.format(self.fund, self.percentage,
                                    self.month.strftime(self.MONTH_FORMAT))

    def validate_unique(self, exclude=None):
        """Validate uniqueness across fund and month (ignoring day)."""
        if 'fund' not in exclude and 'month' not in exclude:
            other_returns = (FundReturn
                             .objects
                             .exclude(id=self.id)
                             .filter(fund=self.fund,
                                     month__year=self.month.year,
                                     month__month=self.month.month))
            if other_returns.exists():
                msg = _('%s already has a return for %s.')
                msg_params = (self.fund,
                              self.month.strftime(self.MONTH_FORMAT))
                raise ValidationError(msg, params=msg_params)

        return super().validate_unique(exclude)
