"""Edgefolio forms."""

from django import forms
from django.contrib import messages

import pandas as pd

from edgefolio.models import Fund, FundReturn


class ExcelForm(forms.Form):
    """Excel upload form."""

    excel_file = forms.FileField()

    FUNDS_SHEET = 'Funds Details'
    RETURNS_SHEET = 'Time Series'

    def create_or_update_data(self, request):
        """Create or update data from an Excel file."""
        funds_data = pd.read_excel(self.cleaned_data['excel_file'],
                                   sheet_name=self.FUNDS_SHEET)
        for _, fund_data in funds_data.iterrows():
            self.create_or_update_fund(fund_data, request)

        self.cleaned_data['excel_file'].seek(0)
        returns_data = pd.read_excel(self.cleaned_data['excel_file'],
                                     sheet_name=self.RETURNS_SHEET)
        num_returns = 0
        for month, return_data in returns_data.iterrows():
            num_returns += self.create_or_update_returns(month, return_data)

        msg = 'Processed {} fund {}'.format(
            num_returns, 'return' if num_returns == 1 else 'returns')
        messages.add_message(request, messages.INFO, msg)

    @staticmethod
    def create_or_update_fund(fund_data, request=None):
        """Create or update a fund."""
        name = fund_data['Fund Name']
        fund, created = Fund.objects.get_or_create(name=name)
        strat = next(filter(lambda s: s[1] == fund_data['Strategy Style'],
                            Fund.STRATEGIES))[0]
        fund.strategy = strat
        rexp = next(filter(lambda r: r[1] == fund_data['Region Exposure'],
                           Fund.REGION_EXPOSURES))[0]
        fund.region_exposure = rexp
        fund.full_clean()
        fund.save()

        if request:
            msg = '{} {}'.format('Created' if created else 'Updated', fund)
            messages.add_message(request, messages.INFO, msg)

    def create_or_update_returns(self, month, return_data):
        """Create or update a month of fund returns."""
        num_returns = 0
        for fund_name, percentage in return_data.iteritems():
            if pd.isnull(percentage):
                continue
            self.create_or_update_return(month, fund_name, percentage)
            num_returns += 1

        return num_returns

    @staticmethod
    def create_or_update_return(month, fund_name, percentage):
        """Create or update a fund return."""
        try:
            fund_return = FundReturn.objects.get(fund__name=fund_name,
                                                 month__year=month.year,
                                                 month__month=month.month)
        except FundReturn.DoesNotExist:
            fund_return = FundReturn(fund=Fund.objects.get(name=fund_name))

        fund_return.percentage = percentage
        fund_return.month = month
        fund_return.full_clean()
        fund_return.save()
