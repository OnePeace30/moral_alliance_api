from models import Gifts, EventsAnnotated
from util import Database
from database import connection

from sqlalchemy import not_
import logging

logger = logging.getLogger("moral_alliance")


def regenerate_gifts():
    db = Database()
    # gifts = db.session.query(Gifts).filter(Gifts.year != 1)
    # for gif in gifts:
    deleted = []
    with connection() as cursor:
        sqls = [f"""
            SELECT case when rnk <= 4 then country else 'other' end as country, sum(q.sod), q.year, 100.0 * sum(q.sod)/s.sod, q.uni_id--, avg(rnk)
            FROM
                (select country, sum(sum_of_donations) sod, uni_id, year,
                    dense_rank() over (partition by uni_id, year order by sum(sum_of_donations) DESC) as rnk
                from foreign_gifts
                where uni_id is not null and year < 2025
                group by country, uni_id, year
                order by rnk) q
                left outer join (SELECT year, uni_id, sum(sum_of_donations) sod from foreign_gifts group by year, uni_id) s
                    on s.uni_id = q.uni_id and s.year = q.year
            group by case when rnk <= 4 then country else 'other' end, q.uni_id, q.year, s.sod
            order by q.year, q.uni_id
        """,
        f"""
            SELECT case when rnk <= 4 then country else 'other' end as country, sum(q.sod), q.year, 100.0 * sum(q.sod)/s.sod, q.uni_id--, avg(rnk)
            FROM
                (select country, sum(sum_of_donations) sod, uni_id, 1 as year,
                    dense_rank() over (partition by uni_id order by sum(sum_of_donations) DESC) as rnk
                from foreign_gifts
                where uni_id is not null and year < 2025
                group by country, uni_id
                order by rnk) q
                left outer join (SELECT 1 as year, uni_id, sum(sum_of_donations) sod from foreign_gifts group by uni_id) s
                    on s.uni_id = q.uni_id and s.year = q.year
            group by case when rnk <= 4 then country else 'other' end, q.uni_id, q.year, s.sod
            order by q.year, q.uni_id
        """
        ]
        for sql in sqls:
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                gift = db.session.query(Gifts).filter(Gifts.country == row[0], Gifts.year == row[2], Gifts.university_id == row[4]).one_or_none()
                if gift:
                    logger.info(f"update gift {gift.id}")
                    gift.sumofdonations = row[1]
                    gift.percentage = row[3]
                    db.session.commit()
                else:
                    logger.info(f'create new gift for {row[4]} - {row[2]}')
                    new_gift = Gifts(
                        country = row[0],
                        sumofdonations = row[1],
                        year = row[2],
                        percentage = row[3],
                        university_id = row[4],
                    )
                    db.session.add_all([new_gift])
                    db.session.commit()
                    countrys_new = list(map(lambda x: x[0],filter(lambda z: z[2] == row[2] and z[4] == row[4], rows)))
                    logger.info(f'new countrys - {countrys_new}')
                    to_delete_gift = db.session.query(Gifts).filter(Gifts.year == row[2], Gifts.university_id == row[4]).filter(not_(Gifts.country.in_(countrys_new)))
                    deleted.extend([dg.id for dg in to_delete_gift])
                    to_delete_gift.delete()
                    db.session.commit()
    return deleted


def regenerate_events():

    db = Database()

    with connection() as cursor:
        sql = f"""
            select to_char(date, 'Mon YYYY'), to_char(date, 'Mon'), count(*), uni_id  from events
            where uni_id is not null and date is not null
            group by 1, 2,4
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            event = db.session.query(EventsAnnotated).filter(EventsAnnotated.date == row[0], EventsAnnotated.university_id == row[3]).one_or_none()
            if event:
                event.amount = row[2]
                db.session.commit()
            else:
                new = EventsAnnotated(
                    date = row[0],
                    month_label = row[1],
                    amount = row[2],
                    university_id = row[3],
                )
                db.session.add_all([new])
                db.session.commit()



if __name__ == '__main__':
    # regenerate_gifts()
    regenerate_events()