# Scraping and Analyzing the Value Investors Club

This is a project to scrape and analyze the website www.ValueInvestorsClub.com. It is a great website full of thousands of investing ideas that outperform the market on average. This repository briefly scrapes and analyzes them.

# Table Of Contents
- [Scraping and Analyzing the Value Investors Club](#scraping-and-analyzing-the-value-investors-club)
- [Table Of Contents](#table-of-contents)
- [Results](#results)
- [What's next?](#whats-next)
- [Please, don't just clone and scrape!](#please-dont-just-clone-and-scrape)
- [Running this tool](#running-this-tool)
- [connect to the DB image with:](#connect-to-the-db-image-with)
- [Structure:](#structure)
  - [Scraper:](#scraper)
  - [ProcessLinks](#processlinks)
  - [ValueInvestorsClub](#valueinvestorsclub)
    - [ValueInvestorsClub/ValueInvestorsClub/models](#valueinvestorsclubvalueinvestorsclubmodels)
- [Pricing Data](#pricing-data)
- [ValueInvestorsClub Scraper.](#valueinvestorsclub-scraper)

# Results

For a full breakdown of calculated results see the top level pricing.ipynb. It adds the pricing data to the SQL db via SQLAlchemy, then does various forms of analysis on it, some of that analysis is discussed here.

To understand the data, you must understand how the ValueInvestorsClub segments their investment ideas into several trackable buckets, country of origin, short vs long, and contest winners. Where each idea represents a given tradable equity somewhere in the global market. Shorts are ideas where the thesis states the companies stock is expected to go down, and longs expect the company to go up normally on a basic of company value. Contest winners are winners of the ValueInvestorClubs weekly contest. This is decided based on the estimated merit, quality, and thoroughness of the investment pitch.

Some basic stats, I scraped a total of 13656 ideas. Of those, I found matching US companies historical pricing data for 2370. This is because the majority of the ideas pitched are international. 

We can see the annualized median returns of all groups of investment ideas below.

![Returns over various time periods for shorts, longs and contest winners](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/AllReturns.png?raw=true)

If we look at the median returns for all time frames and broken out across all groups of ideas, we see that the long contest winners aggressively are piled onto so much that the share price moves a disproportionate amount within the first weeks and month of an idea being posted. This seems to suggest that the ValueInvestorsClub moves the market. Also, since a contest winner is announced every week, there may be disproportionate alpha in investing in contest winners the second they are announced completely naively, and then selling one to two weeks or months later.

Many of the associated tickers stop being actively traded on account of going private, going bankrupt, getting acquired or some other reason for being de-listed.

We can see the percentage of companies that become de-listed x days after an idea is posted in this plot:

![Percentage of companies that are de-listed, x days after an idea is posted.](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/PercentNone.png?raw=true)

It is interesting to see long positions get de-listed significantly more often than shorts. Presumably, this is because the long companies are attractive companies to acquire and the acquisition rate + going private rate is substantially higher than the number of companies going bankrupt. Therefore, these attractive companies get bought up and disappear at a higher rate than the companies which are recommended to be shorted by value investor club investors.

There are extreme outliers that skew various average returns, but generally, medians seem representative of the various distributions fairly well.

 Below are a few examples:

![Five year performance distribution, non-annualized](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/FiveYearLongPerf.png?raw=true)

The above is the non-annualized total 5 year change in stock price for all of the companies that have data for them. Note the few outliers far out on the right tail.

![Five year short performance graph](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/FiveYearShortPerf.png?raw=true)

The above is the non-annualized percentage change in stock price for short positions. This is not profit! As short positions want values less than one. We'll look at percentage gain later. We know a decent number of these companies would have gone under and have been de-listed so this number will be artificially high. You also can see a stock really hurt our average that had 2500% gains. 

![Six Month Long Contest Winner Performance](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/SixMonthLongContestPerf.png?raw=true)

The above is the non-annualized 6 month change in price of contest winners. You can see heavy impact of outliers and the fact that we have very sparse data for contest winners.

![Returns over various time periods for shorts, longs and contest winners](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/SixMonthShortContestPerf.png?raw=true)

Similarly, we can see the non-annualized change in price of shorts over the same time period. This is one of the few places where shorts successfully get a negative change in share price.

We can see the stark difference in performance when comparing the median performance of all long ideas compared to the median performance of all short ideas across various time intervals from when the idea was originally posted.

![Returns over various time periods for shorts, longs and contest winners](https://github.com/dschonholtz/ValueInvestorsClub/blob/main/pics/ShortAndLongReturns.png?raw=true)

The biggest takeaways from this data are the shorts only win when using the best ideas, contest winners, and even then they only return alpha for the first six months. It also suggests that the ValueInvestorsClub is moving the market, and that the best gains may be found investing quickly for very short periods of time rather than investing for long periods of time.

Specifically! It may be possible to get a 30% annualized return by simply buying all long ideas the second they are published and then selling a single week later.

This of course would need to be checked more thoroughly and isn't financial advice :)
None of this is backtested and there are more interesting things to find! But it is a solid start for a weeks worth of work.


# What's next?
- You should hire me! I love doing this kinda stuff and am looking to do more of it in a more formal workflow.
- I have access to quantopedia and have been chatting with Systemic Alpha here at Northeastern with the goal of properly backtesting some of this data to see how off my numbers are.
- Attempt to do classification of ideas as contest winners, and then to see if we could generate high returns by investing in projected contest winners.
- Fine tune a large language model to write ideas based off of the worst 10% of ideas or the best 10% performing ideas.
- Rank investors! There seem to be strong incentives to pump or dump on stocks. It would be interesting to see if there are investors that are intentionally writing bad analysis. It also would be interesting to see if you could follow a subset of authors and get disproportionate returns. 
- See if the percentage annualized returns change over time. I strongly suspect that the ValueInvestorsClub is moving the market, and that appears to be supported by the high 1-2 week return in contest winners. It would be interesting to see if that happened when the site first launched in 2001 and had a smaller user base.


# Please, don't just clone and scrape!

The ValueInvestorsClub is an amazing website. I don't want folks to scrape it more than necessary potentially causing unnecessary load to their servers. If I find this getting too much traffic I'll be taking the repo private.

Please see connect to the DB image, on how to use the data.

If you have any questions please contact me @ schonholtz {dot} d {at} northeastern {dot} edu


# Development Setup

## Environment Setup
1. Create a Python virtual environment:
   ```bash
   uv venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   # For production
   uv pip install -r requirements.txt
   
   # For development/testing
   uv pip install -r requirements-dev.txt
   ```

4. Start the database:
   ```bash
   docker-compose up -d
   ```

5. Initialize the database:
   ```bash
   ./startScript.sh
   ```

## Running the Application
- API Server: 
  ```bash
  python -m api.main
  ```
- Web Interface:
  ```bash
  cd frontend && npm run dev
  ```
- Tests:
  ```bash
  ./run_tests.sh
  ```

## Running the Scraper Tools
- Run scraper to collect links (Make sure to use the virtual environment):
    ```bash
    python scraper.py
    ```
- Process links to remove duplicates:
    ```bash
    python ProcessLinks.py
    ```
- Import data into database:
    ```bash
    scrapy crawl IdeaSpider
    ```

# connect to the DB image with:

`psql -U postgres -h localhost -p 5432`

To get running with this data, I have dumped the data with the command

`pg_dump -U postgres -h localhost -p 5432 ideas > VIC_IDEAS.sql`

Password is just `postgres`

Then you can run `docker-compose up` at the root level of this repo, then connect to the db with:

`psql -U postgres -h localhost -p 5432`

To load the data into your version of postgres after you have gotten postgres running locally, find the data here:

https://drive.google.com/file/d/1XdHbJu35eyJdMoHMyycudDjyCvrEmIBW/view?usp=sharing

Then you can load it into your running psql instance with:

psql -U postgres -h localhost -p 5432 ideas < VIC_IDEAS.sql

I have tested this flow on ubuntu 22.04, but presumably this dump should work any version of postgres and docker.


# Structure:

## Scraper:

This is a simple python file that leverages Selenium. 
It loads the ValueInvestorsClub.com website, selects a starting date, then it clicks the load more button for a pre-determined amount of time. 
After some number of load more clicks, currently 20, it loads all of the links to investment ideas and saves them to a file starting with the given date it started scraping from.

Because the number of ideas on the page eventually becomes very large, it becomes vastly more efficient to save periodically, and to select a new date with only 20 ideas on the page.

It would definitely be possible to have selenium reload the page with a new date every x number of clicks, but currently I just run the script again. 

This generates some repeats, and forces me to watch the script a bit more closely, but since I didn't know what the failure modes were for this site and I can remove duplicates in post, it seemed to make more sense to watch it closely and to watch for failure.

It is worth noting that in order to get IP banned, the IP is rotated with a VPN CLI, and there are fairly long random sleeps between certain numbers of requests.

After running this we get a collection of link text files.

## ProcessLinks

This is a really simple python file that processes all of the link files, removes duplicates and makes a single link file.

## ValueInvestorsClub

This is a scrapy project that the scrapy package auto-builds. 
I have since discovered that the scrapy project does in fact support selenium, but by using selenium just to scrape the links I could run a scrapy request platform headlessly. I did have to continue to rotate IPs and now user agents in order to not get blocked, but ultimately I was still able to scrape all of the associated data.

Because of the way I initially ran this I still ended up with some duplicate data entries in my postgreSQL DB.

I removed those duplicates with a simple SQL query, checking for users who had multiple ideas with the same ticker and same date.

### ValueInvestorsClub/ValueInvestorsClub/models

For ease of imports for right now, I have nested the models for SQL Alchemy in the scrapy project. I may have to break that out into a separate Python project/package eventually.

The ideas table is mapped as:

    id: Mapped[str] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(256))
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.ticker"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_link"))
    date: Mapped[DateTime] = mapped_column(DateTime)
    is_short : Mapped[bool] = mapped_column(Boolean)
    is_contest_winner : Mapped[bool] = mapped_column(Boolean)

Note: The descriptions and catalysts table are effectively part of the ideas table, but they are broken out as their values are huge and would greatly impact performance when querying at scale.

The descriptions table is mapped as:
    idea_id: Mapped[str] = mapped_column(ForeignKey(Idea.id), primary_key=True)
    description: Mapped[str] = mapped_column(String(128000))

The catalysts table is mapped as:
    idea_id: Mapped[str] = mapped_column(ForeignKey(Idea.id), primary_key=True)
    catalysts: Mapped[str] = mapped_column(String(4096))

The companies table is mapped as:
    ticker: Mapped[str] = mapped_column(String(32), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(128))

The performance table is the only table I don't really like.
I didn't want to bring in all of the assiocated data of the 135,000 tickers that exist daily stock data or 
    idea_id: Mapped[str] = mapped_column(ForeignKey("ideas.id"), primary_key=True)
    sameDayClose: Mapped[float] = mapped_column(Float)
    nextDayOpen: Mapped[float] = mapped_column(Float)
    nextDayClose: Mapped[float] = mapped_column(Float)
    oneWeekClose: Mapped[float] = mapped_column(Float)
    twoWeekClose: Mapped[float] = mapped_column(Float)
    one_month_performance: Mapped[float] = mapped_column(Float)
    three_month_performance: Mapped[float] = mapped_column(Float)
    six_month_performance: Mapped[float] = mapped_column(Float)
    one_year_performance: Mapped[float] = mapped_column(Float)
    two_year_performance: Mapped[float] = mapped_column(Float)
    three_year_performance: Mapped[float] = mapped_column(Float)
    five_year_performance: Mapped[float] = mapped_column(Float)

The user table is a mapping of usernames and links to them. Note it is linked to the user_link in the ideas table:
    username: Mapped[str] = mapped_column(String(64))
    user_link: Mapped[str] = mapped_column(String(128), primary_key=True)

# Pricing Data
I downloaded a variety of free daily historical data prices from this site:
https://stooq.com/db/h/

It's great, but I have a problem with resolving exchanges. I didn't capture country of origin data when scraping initially. Huge mistake!

So I had a ticker and a name in my DB, and I had pricing data which had tickers, prices and exchanges.

I can fix this in a couple more days of scraping and updated my DB, but I would rather get done what I can even if it isn't perfect so I don't discover other things like this while sinking more work into a dataset.

I pulled some additional CSV's from here. They have a good mapping of US companies to their associated tickers.
https://datahub.io/core/nyse-other-listings

I pushed that into numpy and lowercased all of the company names and tickers.

Then I went through each idea, found 
Then I checked that at least one of the words 3 or more characters in length is in a company name in the csv and the database. I also checked that the word isn't in a list of extremely common words.

If all of that checks out, then I'll look up each price for each of the days relative to the post day and add the performance metrics.

After that, I can rank investors by US stock performance prediction over various time frames.
# ValueInvestorsClub Scraper.

Data is at the top level. See nested ValueInvestorsClub dir for scrapy dir. Uses SQL Alchemy to save scrapy outputs to sql output.

See top level scraping python for scrapin gof links
