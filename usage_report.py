import website.wsgi
from request.models import Request
from mathtutor.models import Student
import csv

csvFile = open("access.csv", 'w')
writer = csv.writer(csvFile, csv.excel)
columns = [f.name for f in Request._meta.get_fields()]
writer.writerow(columns)
for r in Request.objects.all():
    if r.user_id:
        row = []
        for c in columns:
            row.append(getattr(r, c))
        writer.writerow(row)



