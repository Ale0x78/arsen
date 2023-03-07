import time
import random
from os import mkdir, chdir
from os.path import exists as path_exists
from pymongo.mongo_client import MongoClient

# import check_output
from subprocess import check_output, STDOUT
import uuid
from gridfs import GridFS
from pymongo import MongoClient
import os




from celery import Celery



app = Celery(
    'crawler',
    broker='redis://redis:6379/0',
    # backend='rpc://user:bitnami@rabbitmq',
    CELERYD_CONCURRENCY=1
)

def init():
    print("Initializing")
    if not path_exists("working"):
        mkdir("working")
    chdir("working")

def clean():
    chdir("..")
    check_output(["rm", "-rf", "working"])

def store_files(url, timestamp, output):
    # Connect to MongoDB
    with MongoClient('mongodb://mongo:27017') as mongo_client:
        mongo_db = mongo_client['crawler']
        fs = GridFS(mongo_db)
        # Get all files in the current directory
        files = os.listdir('.')
        inserted = None
        try:
            inserted = mongo_db['meta'].insert_one({
                "url": url,
                "output": output,
                "compressed": False
            })
        except Exception as e:
            error("MongoDB Write", str(e))
            return
        
        uid = inserted.inserted_id
        for file in files:
            if file.endswith('.log') or file.endswith('.har') or file.endswith('.png'):
                with open(file, 'rb') as f:
                    fs.put(f, filename=file, url=url, time=timestamp, uid=uid)

    
def error(context, msg):
    with MongoClient("mongodb://mongo:27017") as client:
        db = client["crawler"]
        db["errors"].insert_one({
            "context": context,
            "msg": msg,
            "time": time.time()
        })

@app.task(name='crawl', queue='my_queue')  # Named task
def crawl(url): # This assumes a valir URL was passed for URL!
    init()
    try:
        stdout = check_output(["node", "../crawler/crawler.js", url], stderr=STDOUT)
        store_files(url, time.time(), stdout.decode("utf-8"))
    except Exception as e:
        error("Exception", str(e))
    finally:
        clean()
        
        
    
    
