import urllib2
import os, json
import website.wsgi
from datetime import datetime, timedelta
from mathtutor.models import Result, Constants, Quiz, ParentFormResult
from parserclasses import ThreadParse, ThreadParentFormParse
from django.utils import timezone
import requests, grequests
import Queue

# ADD ADDITIONAL QUERY PARAM FOR SITE
_API_URL = os.getenv("API_URL")
_USER = os.getenv("USER_ID")
_TOKEN = os.getenv('TOKEN')

API_STRING = _API_URL + "API_SELECT=ControlPanel&Version=2.5&Request=getLegacyResponseData&User=" + _USER
API_STRING = API_STRING + "&Token=" + _TOKEN + "&Format=JSON&SurveyID="

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
    StartDate = "&StartDate={}".format(startDate.strftime("%Y-%m-%d %H:%M:%S"))
    print ("{}: begin".format(str(datetime.now())))
    api_urls = []
    for q in Quiz.objects.filter(q_group__group=25):
        u = "{}{}{}".format(API_STRING, q.q_id, StartDate)
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

    Result.objects.bulk_create(data)
    print "{}: Finished parsing qualtrics data".format(str(datetime.now()))

def get_parent_form_results():
    urls = []
    for f in Constants.parent_forms:
        url = "{}{}".format(API_STRING, f['qid'])
        urls.append(url)
    rs = (grequests.get(url, hooks={'response': get_exceptions}) for url in urls)
    qualtricsData = grequests.map(rs)
    print "{}: Finished collecting parent form information from Qualtrics API".format(str(datetime.now()))

    parseQueue = Queue.Queue()
    data = []
    for i in range(5):
        t = ThreadParentFormParse(parseQueue, data)
        t.setDaemon(True)
        t.start()

    for item in qualtricsData:
        parseQueue.put(item)

    parseQueue.join()
    ParentFormResult.objects.bulk_create(data)
    print "{}: Finished parsing parent form results data".format(str(datetime.now()))


def main():
    qual_update_script()
    get_parent_form_results()

if __name__ == "__main__":
    main()

