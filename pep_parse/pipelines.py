import csv
import datetime as dt

from pep_parse.settings import BASE_DIR, DATETIME_FORMAT


class PepParsePipeline:
    def open_spider(self, spider):
        self.statuses = {}

    def process_item(self, item, spider):
        self.statuses[item['status']] = self.statuses.get(item['status'], 0)+1
        return item

    def close_spider(self, spider):
        now_formatted = dt.datetime.now().strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = BASE_DIR / 'results' / file_name
        total = sum(self.statuses.values())
        with open(file_path, mode='w', encoding='utf-8') as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(('Статус', 'Количество'))
            writer.writerows(self.statuses.items())
            writer.writerow(('Total', total))
