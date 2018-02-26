[![Build Status](https://travis-ci.org/craiga/edgefolio_test.svg?branch=master)](https://travis-ci.org/craiga/edgefolio_test) [![Requirements Status](https://requires.io/github/craiga/edgefolio_test/requirements.svg?branch=master)](https://requires.io/github/craiga/edgefolio_test/requirements/?branch=master)

# Getting Started

This project uses pipenv to manage its dependencies. To install the project and start Django's development server, run the following commands:

    pipenv install
    pipenv run ./manage.py runserver 0.0.0.0:8000

To upload a spreadsheet, open http://localhost:8000/excel in a web browser. 

Funds and fund returns will be visible through the admin site at http://localhost:8000/admin. To create a user to access the admin site, run the following command:

    pipenv run ./manage.py createsuperuser

# Running Tests

To run tests you need to install development dependencies using the following command:

    pipenv install --dev

Once development dependencies have been installed, you can run tests using the standard Django test runner:

    pipenv run ./manage.py test

You can also check code quality by running pycodestyle, pydocstyle and pylint:

    

# Notes

## Decimal vs. floating point fund returns

It's not entirely clear whether the value of each return should be stored as a floating point number or a decimal number. I'm sure you're aware of the difference between the two, but just to prove that I do as well:

 * **decimal numbers** are guaranteed to always return the same value, but are limited in the precision they can store (eg. 0.0001 will *always* be 0.0001, but 0.0001000001 may not be able to be accurately stored), whereas
 * **floating point numbers** have much greater scope for precision, but using them can result in small changes to their values (eg. 0.0001 may be returned as 0.00010000000000001).

## Importing Time Series

The spec doesn't explicitly state that data from the time series sheet should be imported, but I've assumed that it should.

## Storage of percentage values and calculation of cumulative returns

The spec states the following:

>  for each Fund object, a method returning another pandas time series (still monthly frequency) representing the cumulative returns of the fund based on the returns_series, with a start value of 1. The formula for this is simple: `cumulative_return(month_n) = cumulative_return(month_n-1) * (1 + return_series(month_n))`

It's unclear whether `return_series` should be a logical percentage value (i.e. `0.5` is 50%) or whether 50% should be `50.0` in this formula.

As the latter is true in the data stored in the funds data spreadsheet, I've assumed the latter interpretation.
