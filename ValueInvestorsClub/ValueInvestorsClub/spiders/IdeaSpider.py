"""
The following inserts all scraped links into a postgres sql database. 
Unfortunately, this creates some duplicates.
To view those we make a query that selects duplicate ideas where the user, ticker and date are all the same.

select * from ideas full outer join companies full outer join where date in (select date from ideas group by id having count(*) > 1);
"""


import scrapy
from ValueInvestorsClub.items import ValueinvestorsclubItem
import subprocess

def rotate_ip():
    command = "protonvpn-cli c -r"
    command = command.split()
    # run the above command and then print the output
    try:
        output = subprocess.check_output(command)
    except subprocess.CalledProcessError as e:
        print('There was an error', e, '\nTrying again.')
        try:
            disconect_out = subprocess.check_output("protonvpn-cli d".split())
            print('disconnect_out: ' + str(disconect_out))
            output = subprocess.check_output(command)
            print(output)
        except subprocess.CalledProcessError as e2:
            print('Second time means it ain\'t gonna work', str(e2), '\nKilling.')
            raise e2
    print('Rotating IP')
    print(output)

class IdeaSpider(scrapy.Spider):
    name = 'IdeaSpider'
    allowed_domains = ['valueinvestorsclub.com']

    def load_idea_links(self):
        # load the idea links from the file
        idea_links = []
        with open('/home/douglas/InvestClub/idea_links_no_duplicates.txt', 'r') as f:
            for line in f:
                idea_links.append(line.strip())
        return idea_links

    def start_requests(self):
        idea_links = self.load_idea_links()
        # every 20 links rotate the ip.
        count = 0
        for link in idea_links[13860:]:
            count += 1
            if count % 10 == 0:
                rotate_ip()
            yield scrapy.Request(link, self.parse)

        # yield scrapy.Request("https://www.valueinvestorsclub.com/idea/InPost/5698302853", self.parse)

    def parse(self, response):
        # get the link with authors username and the link to the authors page
        # get the company name
        # get the company ticker
        # get the date
        # get the idea description
        # get the idea catalysts
        # get if the user is short
        # get if the post is contestWinner

        # The idea name and ticker are in a div with a class: idea_name
        # in that is a span with class vich1. There is top level text with the company name.
        # The ticker is in a span nested inside of that span

        # the current page that is being scraped
        link = response.url

        company_name = response.xpath("//div[@class='idea_name']/span[@class='vich1']/text()").get()
        company_ticker = response.xpath("//div[@class='idea_name']/span[@class='vich1']/span/text()").get()

        # the date is in a div with class "idea_by" and is the text in the first nested div
        date = response.xpath("//div[@class='idea_by']/div/text()").get()
        # the user is in the text of a link in the same idea_by div.
        # The link is the first link in the div
        username = response.xpath("//div[@class='idea_by']/a/text()").get()
        # also get the actual link to the username from that link tag
        username_link = response.xpath("//div[@class='idea_by']/a/@href").get()

        # get the long description and catalyst texts by first getting the entire div with id description
        # store all of the text between the h4 tag that says description and the other h4 tag that says catalyst
        description = response.xpath("//div[@id='description']/descendant-or-self::*/text()").getall()
        description = '\n '.join(description)
        description = description.split('Catalyst')
        catalysts = description[-1]
        description = "Catalyst".join(description[:-1])
        # if len(description) < 128:
        #     description = response.xpath("//div[@id='description']/h4[text()='Description']/following-sibling::text()").getall()
        #     description = '\n'.join(catalysts)
        #     description = description.strip()
        # trim leading and trailing whitespace
        description = description.strip()
        # get the catalysts by getting the entire div with id description
        # store all of the text after the h4 tag that says catalyst
        # if len(catalysts) < 128:
        #     catalysts = response.xpath("//div[@id='description']/h4[text()='Catalyst']//text()").getall()
        #     catalysts = '\n'.join(catalysts)
        catalysts = catalysts.strip()

        # check if this is a short position. a span with class "label label-short" signifies it.
        short = response.xpath("//span[@class='label label-short']").getall()
        if len(short) == 0:
            short = False
        else:
            short = True

        contest_winner = response.xpath("//span[@class='label label-success']").getall()
        if len(contest_winner) == 0:
            contest_winner = False
        else:
            contest_winner = True


        yield ValueinvestorsclubItem(
            ticker=company_ticker,
            link=link,
            companyName=company_name,
            date = date,
            username=username,
            userLink=username_link,
            isShort=short,
            isContestWinner=contest_winner,
            description=description,
            catalysts=catalysts
        )


