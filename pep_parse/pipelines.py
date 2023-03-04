# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv

from scrapy.exceptions import DropItem
from datetime import datetime as dt
from collections import defaultdict

from pep_parse.settings import BASE_DIR, RESULTS_DIR


DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:

    def open_spider(self, spider):
        self.result = defaultdict(int)

    def process_item(self, item, spider):
        if 'status' not in item:
            raise DropItem('"status" отсутствует')
        status = item['status']
        self.result[status] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / RESULTS_DIR
        results_dir.mkdir(exist_ok=True)
        time = dt.now().strftime(DATETIME_FORMAT)
        filename = f'status_summary_{time}.csv'
        total = sum(self.result.values())
        with open(results_dir / filename,
                  mode='w',
                  encoding='utf-8') as f:
            csv.writer(f,
                       dialect=csv.unix_dialect,
                       quoting=csv.QUOTE_NONE
                       ).writerows([(
                                    'Статус', 'Количество'),
                                    *self.result.items(),
                                    ['Total', total]])
