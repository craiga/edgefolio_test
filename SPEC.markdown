The goal is to generate a simple django application with simply SQLite as the database, and with

 * a single Model called Fund, holding the following fields:
   * a unique id
   * a name
   * a strategy, which is a string within a fixed set of possible choices: "Multi Arbitrage", "Fixed Income", "Long Short Equity" or "Event Driven"
   * a region_exposure, which is a string within a fixed set of possible choices: "Global", "US", "Asia"
   * a returns_series, which is a time series of float numbers representing percentage numbers per month, such as for example the series found in the second spreadsheet of [the Excel template attached](spec/funds_data.xls). The way to persist this time series in the database (field(s) type(s) etc.) is left at the choice of the candidate.
 * for each Fund object, a method returning the fund's returns_series as a pandas time series (see pandas library documentation online)
 * for each Fund object, a method returning another pandas time series (still monthly frequency) representing the cumulative returns of the fund based on the returns_series, with a start value of 1. The formula for this is simple: `cumulative_return(month_n) = cumulative_return(month_n-1) * (1 + return_series(month_n))`
 * a way to import such Fund objects by uploading an Excel template (sample provided) via a file upload form on a django web page: the django app should then parse that file and create/update corresponding Fund objects
 * a web page displaying: 
   * the list of funds available in the database as a table with the following columns: fund name, fund strategy, fund region_exposure and the fund's return_series value for the month of June 2017, and ordered by that numeric value in descending order
   * a dropdown selection for filtering the funds displayed in the page by one of the available strategy choices
   * a dropdown selection for filtering the funds displayed in the page by one of the available region_exposure choices
 * a basic [Highchart](https://www.highcharts.com/) line graph displaying one line per fund, where each line is the cumulative_returns time series of the fund. Example of Highcharts line graph available at http://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/demo/line-basic/
 * As a bonus, this page/django view should calculate one additional time series which is the average (equally weighted mean) of all the cumulative_returns time series of all funds available in the page and display that one average series as another line in the same line graph

For inspiration, this exercise basically achieves a simplified version of [the page sketch attached as an image](spec/Screen Shot 2017-08-18 at 19.29.27.png).

![Screen shot of Edgefolio](spec/Screen Shot 2017-08-18 at 19.29.27.png)

As this exercise might be quite long, the candidate is free to skip some of the specifications above, to focus on the other ones, based on what area is more fun/confortable. 

Candidate will judged based on simplicity and cleanliness of the Python code, niceness of the HTML markup and layout, cleverness of the data parsing and manipulation necessary for parsing an input file and persisting the data via the django ORM, as well as making sure the candidate is familiar with scaffolding a simple MVC django app.

The Candidate will not be judged on the design and esthetics of the pages, nor on the way the necessary static assets and dependencies are handled.

The django app can simply be run using the default `manage.py runserver command`.

Please create Github repository for hosting and sharing the code with us.

