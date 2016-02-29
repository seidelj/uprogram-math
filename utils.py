import urllib2
import os, json
import website.wsgi
import datetime
from mathtutor.models import Result, Constants
from parserclasses import ResponseParser
from django.utils import timezone
import requests, grequests
import Queue

# ADD ADDITIONAL QUERY PARAM FOR SITE
_API_STRING = os.eniron.get("API_STRING")


def get_response():
    req = urllib2.Request(URL)
    req.add_header("Authorization", "Token {}".format(os.environ.get("MATHGAME_TOKEN")))
    response = urllib2.urlopen(req)
    if response.code == 200:
        return response
    else:
        return False

def split_seq_by_length(seq, length):
    newseq = [seq[x:x+length] for x in xrange(0, len(seq), length)]
    return newseq

def get_exceptions(response, **kwargs):
    if response.status_code == requests.codes.ok:
        pass
    else:
        sys.exit("Response is not 200: {}; Q_ID: {}".format(response.text, response.url))

def async_request(routines=6):
    startDate = timezone.make_aware(datetime.now()-timedelta(hours=8))
    StartDate = "&StartDate={}".format(startDate.strftime("%Y-%m-%d %H:%M%S"))
    print ("{}: begin".format(str(datetime.now())))
    api_urls = []
    for q in Quiz.objects.filter(q_group__group=25):
        u = "{}{}{}".format(_API_STRING, q.q_id, StartDate)
        api_urls.append(u)
    print len(api_urls)
    urlList = split_seq_by_length(api_urls, routines)
    qualtricsData = []
    for split in urlList:
        rs = (grequests.get(u, hooks={'response': get_exceptions }) for u in split)
        splitData = grequests.map(rs)
        qualtricsData += splitData

    print "{}: Finished collecting data from qualtrics API".format(str(datetime.now()))

    return qualtricsData

def qual_update_script():

    qualtricsData = async_request(10)

    parseQueue = Queue.Queue()
    data = []
    for i in range(20):
        t = ThreadParse(parseQueue, data)
        t.setDaemon(True)
        t.start()

    for item in qualtricsData:
        parseQueue.put(item)

    parseQueue.join()

    print "{} new results".format(len(data))

    Results.objects.bulk_create(data)
    print "{}: Finished parsing qualtrics data".format(str(datetime.now()))

def get_parent_forms_results():
    urls = []
    for f in Constants.parent_forms:
        url = "{}{}".format(_API_STRING, f['qid'])
        urls.append(url)
    rs = (grequests.get(url, hooks={'response': get_exceptions}) for url in urls)
    qualtricsData = grequests.map(rs)
    print "{}: Finished collecting parent form information from Qualtrics API".format(str(datatime.now()))

    parseQueue = Queue.Queue()
    data = []
    for i in range(5):
        t = ThreadParentFormParse(parseQueue, data)
        t.setDaemon(True)
        t.start()

    for item in qualtricsData:
        parseQueue.put(item)

    parseQueue.join()
    ParentFormResults.objects.bulk_create(data)
    print "{}: Finished parsing parent form results data".format(str(datetime.now()))


def main():
    print "Begin: {}".format(datetime.datetime.now())
    response = get_response()
    if not response:
        print "Response was not 200"
    else:
        blkUpdateList = []
        parser = ResponseParser()
        data = json.loads(response.read())
        for item in data['results']:
            created, obj = parser.parse_response(item)
            if not created:
                pass
            else:
                blkUpdateList.append(obj)
        Result.objects.bulk_create(blkUpdateList)
    print "Finished updating results: {}".format(datetime.datetime.now())


if __name__ == "__main__":
    main()

