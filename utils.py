import urllib2
import os, json
import website.wsgi
import datetime
from mathtutor.models import Result
from parserclasses import ResponseParser

# ADD ADDITIONAL QUERY PARAM FOR SITE
URL = 'https://mathgame-chicago.herokuapp.com/results?site=tutor'


def get_response():
    req = urllib2.Request(URL)
    req.add_header("Authorization", "Token {}".format(os.environ.get("MATHGAME_TOKEN")))
    response = urllib2.urlopen(req)
    if response.code == 200:
        return response
    else:
        return False

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

