import urllib2
import os, json
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
                print obj
            else:
                blkUpdateList.append(obj)
        print blkUpdateList



if __name__ == "__main__":
    main()

