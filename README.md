# Running this tool
- Run scraper after updating the date that is currently hardcoded into it. TODO MAKE IT A COMMAND LINE PARAM IF PUBLIC. Make sure to use the venv
    - python3 scraper.py
    - It will run for 200 clicks for 20 ideas per click. That's 4000 ideas. It may be worth making this a bit more command line driven.
- Run process links to remove duplicate links
    - python3 ProcessLinks.py
- To dump those ideas into the DB run the spider which you do as with any scrapy project:
    - scrapy crawl IdeaSpider

# connect to the DB image with:

`psql -U postgres -h localhost -p 5432`

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
I didn't want to bring in all of the assocated data of the 135,000 tickers that exist daily stock data or 
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

I can fix this in a couple more days of scraping and updated my DB, but I would rather get done what I can even if it isn't perfect so I don't discover other things like this while sinking more work into a dataset.

Some CSV's from here. They have a good mapping of US companies and their names to tickers.
https://datahub.io/core/nyse-other-listings

I pushed that into numpy and lowercased all of the company names and tickers.

Then I'll go through each company and find a company ticker that exists in one of my US csvs.
Then I'll check the first word in company name exists somewhere in the associated ticker list from companies CSV.

If all of that checks out, then I'll look up each price for each of the days relative to the post day and add the performance metrics.

After that, I can rank investors by US stock performance prediction over various time frames.
