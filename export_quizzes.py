import website.wsgi
import csv
from django.conf import settings
import os

from mathtutor.models import Quiz

filename = "quizzes.csv"

with open(os.path.join(settings.BASE_DIR, filename), 'w') as f:
    writer = csv.writer(f, csv.excel)
    headers = ['quiz_id', 'name','site']
    writer.writerow(headers)
    for q in Quiz.objects.all():
        row = [q.q_id,q. q_name, q.site]
        writer.writerow(row)
