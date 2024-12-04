import logging
import csv
import io
    
def get_logger(log_path: str, user: str):
    class CsvFormatter(logging.Formatter):
        def __init__(self):
            super().__init__()
            self.output = io.StringIO()
            self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

        def format(self, record):
            self.writer.writerow([self.formatTime(record), record.levelname, user, record.msg])
            data = self.output.getvalue()
            self.output.truncate(0)
            self.output.seek(0)
            return data.strip()

    logging.basicConfig(level=logging.INFO, filename=log_path, filemode="w")
    logger = logging.getLogger(__name__)
    logger.root.handlers[0].setFormatter(CsvFormatter())

    return logger