import re
from datetime import datetime, timedelta
from dateutil.parser import parse


class PostTimeEst(object):
    '''
        Estimate the posted time of headline
    '''
    def __call__(self, postTime, dlTime):
        # check type
        if type(postTime) != str:
            postTime = str(postTime)
        if type(dlTime) != datetime:
            dlTime = parse(dlTime)

        # time calculation
        if 'min' in postTime:
            mn = int(re.findall('\d+', postTime)[0])
            return datetime.strftime(dlTime - timedelta(minutes=mn), "%Y-%m-%d %H:%M:00 %z")
        elif 'hour' in postTime:
            hr = int(re.findall('\d+', postTime)[0])
            return datetime.strftime(dlTime - timedelta(hours=hr), "%Y-%m-%d %H:00:00 %z")
        elif 'yesterday' in postTime:
            return datetime.strftime(dlTime - timedelta(days=1), "%Y-%m-%d 00:00:00")
        else:
            return postTime
