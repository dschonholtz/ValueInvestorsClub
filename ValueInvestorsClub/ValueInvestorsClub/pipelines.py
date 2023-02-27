# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# This pipeline will dump the associated data into a postgres sql database.

from itemadapter import ItemAdapter
import os
from ValueInvestorsClub.models import Base, Idea, Company, Description, User, Catalysts, Performance
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

class SqlPipeline:
    collection_name = 'scrapy_items'

    def __init__(self, ):
        self.engine = create_engine(f'postgresql+psycopg2://postgres:postgres@localhost/ideas', echo=True)
        Base.Base.metadata.create_all(self.engine)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # Make a idea, catalyst, company, description and user object
        # Then add them to the database
        with Session(self.engine) as session:
            print('Processing item')
            # check if the user already exists
            user = session.query(User.User).filter(User.User.user_link == item['userLink']).first()
            if user is None:
                user = User.User(
                    username=item['username'],
                    user_link=item['userLink']
                )

            # check if the company exists
            company = session.query(Company.Company).filter(Company.Company.ticker == item['ticker']).first()
            if company is None:
                company = Company.Company(
                    ticker=item['ticker'],
                    company_name=item['companyName']
                )
            est_index = item['date'].index('EST')

            new_date = datetime.strptime(item['date'][0:est_index+3], "%B %d, %Y - %I:%M%p %Z")

            idea = Idea.Idea(
                id=str(uuid.uuid4()),
                link=item['link'],
                company_id=company.ticker,
                user_id=user.user_link,
                date=new_date,
                is_short=item['isShort'],
                is_contest_winner=item['isContestWinner'],
            )

            description = Description.Description(
                idea_id=idea.id,
                description=item['description']
            )
            catalysts = Catalysts.Catalysts(
                idea_id=idea.id,
                catalysts=item['catalysts']
            )

            session.add(user)
            session.add(company)
            session.commit()
            session.add(idea)
            session.commit()
            session.add(description)
            session.add(catalysts)
            session.commit()


        return item
