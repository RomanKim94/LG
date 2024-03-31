from datetime import datetime

from django.db import models


class TextFile(models.Model):

    def get_file_name(self, filename):
        date = datetime.today().strftime('%Y.%m.%d %H.%M.%S')
        return f'files/{date}_{filename}'

    file = models.FileField(
        verbose_name='Text file',
        upload_to=get_file_name
    )
