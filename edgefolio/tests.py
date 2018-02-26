"""Edgefolio tests."""

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase


import factory
import factory.fuzzy
from faker import Faker

from edgefolio.forms import ExcelForm
from edgefolio.models import Fund, FundReturn

fake = Faker()


class FundFactory(factory.django.DjangoModelFactory):
    """Fund factory."""

    name = factory.Faker('company')
    strategy = factory.fuzzy.FuzzyChoice(Fund.STRATEGIES)
    region_exposure = factory.fuzzy.FuzzyChoice(Fund.REGION_EXPOSURES)

    class Meta:
        model = Fund


class FundReturnFactory(factory.django.DjangoModelFactory):
    """FundReturn factory."""

    fund = factory.SubFactory(FundFactory)
    month = factory.Faker('date_object')
    percentage = factory.Faker('pyfloat')

    class Meta:
        model = FundReturn


class FundTestCase(TestCase):
    """Test the Fund model."""

    def test_get_returns(self):
        """Test getting a series of returns."""
        # Create a fund and a number of returns for that fund in sequential
        # months.
        fund = FundFactory()
        start = date(year=2000, month=3, day=15)
        fund_returns = []
        for month in (start + (timedelta(days=30) * n) for n in range(20)):
            fund_returns.append(FundReturnFactory(fund=fund, month=month))

        # Assert that the time series is created as expected.
        returns_series = fund.get_returns()
        self.assertEqual(20, len(fund_returns))
        for fund_return in fund_returns:
            self.assertEqual(fund_return.percentage,
                             returns_series[fund_return.month])

    def test_get_cumulative_returns(self):
        """Test getting cumulative returns."""
        fund = FundFactory()
        march = date(year=2000, month=3, day=31)
        FundReturnFactory(fund=fund, month=march, percentage=2.5)
        april = date(year=2000, month=4, day=30)
        FundReturnFactory(fund=fund, month=april, percentage=1.0)
        may = date(year=2000, month=5, day=31)
        FundReturnFactory(fund=fund, month=may, percentage=-0.75)

        # From my reading of the spec, the expected values are as follows:
        #
        # February (not included) = 1.0
        # March = 1.0 * (1 + 2.5%) = 3.5
        # April = 3.5 * (1 + 1.0%) = 7.0
        # May = 7.0 * (1 + -0.75%) = 1.75
        returns = fund.get_cumulative_returns()
        self.assertEqual(3, len(returns))
        self.assertEqual(3.5, returns[march])
        self.assertEqual(7.0, returns[april])
        self.assertEqual(1.75, returns[may])


class FundReturnTestCase(TestCase):
    """Test the FundReturn model."""

    def test_months_are_unique_per_fund(self):
        """Test there can only be one return for each fund in each month."""
        # Set up a fund and a return.
        fund = FundFactory()
        fund_return = FundReturnFactory(fund=fund,
                                        month=date(year=2000, month=3, day=1))
        fund_return.full_clean()

        # Test that another return in that same month is invalid.
        same_month = date(year=2000, month=3, day=10)
        fund_return = FundReturnFactory.build(fund=fund, month=same_month)
        with self.assertRaises(ValidationError):
            fund_return.full_clean()

        # Test that another return in that same month is valid for a different
        # fund.
        fund_return = FundReturnFactory.build(fund=FundFactory(),
                                              month=same_month)
        fund_return.full_clean()


class ExcelFormTestCase(TestCase):
    """Test ExcelForm."""

    def test_update_fund(self):
        """Test updating a fund with create_or_update_fund."""
        # Create a fund to update
        fund = FundFactory(strategy=Fund.STRATEGIES.multi_arbitrage,
                           region_exposure=Fund.REGION_EXPOSURES.asia)

        # Update the fund via the form.
        form = ExcelForm()
        form.create_or_update_fund({
            'Fund Name': fund.name,
            'Strategy Style': Fund.STRATEGIES[Fund.STRATEGIES.fixed_income],
            'Region Exposure':
                Fund.REGION_EXPOSURES[Fund.REGION_EXPOSURES.global_exposure],
        })

        # Assert the fund was updated.
        fund.refresh_from_db()
        self.assertEqual(Fund.STRATEGIES.fixed_income, fund.strategy)
        self.assertEqual(Fund.REGION_EXPOSURES.global_exposure,
                         fund.region_exposure)

    def test_create_fund(self):
        """Test creating a fund with create_or_update_fund."""
        form = ExcelForm()
        form.create_or_update_fund({
            'Fund Name': 'Global Hyper Megacorp',
            'Strategy Style':
                Fund.STRATEGIES[Fund.STRATEGIES.long_short_equity],
            'Region Exposure': Fund.REGION_EXPOSURES[Fund.REGION_EXPOSURES.us],
        })
        fund = Fund.objects.get(name='Global Hyper Megacorp')
        self.assertEqual(Fund.STRATEGIES.long_short_equity, fund.strategy)
        self.assertEqual(Fund.REGION_EXPOSURES.us, fund.region_exposure)

    def test_update_return(self):
        """Test updating a return with create_or_update_return."""
        # Create a return to update
        fund_return = FundReturnFactory(percentage=0.5,
                                        month=date(year=2000, month=3, day=1))

        # Update the return via the form.
        form = ExcelForm()
        form.create_or_update_return(month=date(year=2000, month=3, day=11),
                                     fund_name=fund_return.fund.name,
                                     percentage=0.7)

        # Assert the return was updated.
        fund_return.refresh_from_db()
        self.assertEqual(0.7, fund_return.percentage)

    def test_create_return(self):
        """Test creating a return with create_or_update_return."""
        fund = FundFactory()
        form = ExcelForm()
        form.create_or_update_return(month=date(year=2000, month=3, day=11),
                                     fund_name=fund.name,
                                     percentage=0.7)
        self.assertEqual(1, fund.returns_series.count())
        fund_return = fund.returns_series.first()
        self.assertEqual(0.7, fund_return.percentage)
        self.assertEqual(2000, fund_return.month.year)
        self.assertEqual(3, fund_return.month.month)
