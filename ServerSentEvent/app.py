from flask import Flask,render_template,Response
from flask_sse import sse
from flask import request, current_app, json, stream_with_context
import queue
app = Flask(__name__)

'''
SSE is a protocal which tells server should keep connection with client while 
client send msg still in a HTTP request
'''

subscribers=[]

q=queue.Queue()
messages=[q.put("data: "+str(i)+'\n\n')for i in range(1000)]

@app.route('/stream')
def stream():

    def generator():
        try:
            while True:
                ret=q.get()
                print(ret)
                yield ret

        except GeneratorExit:
            print('exittttt')
    print()
    response=Response(generator(),mimetype='text/event-stream')

    return response

'''
Cache-Control: no-cache
Connection: keep-alive
'''
@app.route('/')
def index():
    return render_template("index.html")
'''
先访问/路径，建立链接，访问蓝图/stream
另一个页面访问路径/hello 触发服务器向客户端发送消息
'''

# @app.route('/stream')
# def stream():
#     """
#     A view function that streams server-sent events. Ignores any
#     :mailheader:`Last-Event-ID` headers in the HTTP request.
#     Use a "channel" query parameter to stream events from a different
#     channel than the default channel (which is "sse").
#     """
#     channel = request.args.get('channel') or 'sse'
#
#     @stream_with_context
#     def generator():
#         for message in self.messages(channel=channel):
#             yield str(message)
#
#     print()
#     return current_app.response_class(
#         generator(),
#         mimetype='text/event-stream',
#     )


@app.route('/chatroom',methods=['POST','GET'])
def chatroom():
    if request.method=='GET':
        roomname="zhangze123"
        return render_template('chatroom.html',roomname=roomname)


if __name__=='__main__':
    app.run()