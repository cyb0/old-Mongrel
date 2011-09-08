from server import Server
from poller import Poller

app = Server('/tmp/shitland.pid')
print len(app.data)
app.start()
for i in app.data:
    print app.data[i]
# poller = Poller(app.data)
# print len(poller.data)
# for k, v in poller.data.iteritems():
#   print k, v
