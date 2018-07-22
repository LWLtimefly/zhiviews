# import time
#
# from BestJob.celery import app
#
# @app.task
# def searchJob(uid, id):
#     time.sleep(10)
#     return '{} 用户已抢到{}'.format(uid,id)
#
#
# @app.task
# def buyArt(uid,id):
#     time.sleep(5)
#     return '{} 用户已买到{}'.format(uid,id)