import os
from app import app, savvy_collection
from app.Views.views import render
from flask.ext.login import login_required, current_user
from flask import jsonify, request, url_for
from werkzeug import secure_filename
from hashlib import md5
from app.Helpers.Constant import *

@app.route('/deleteJob', methods=['POST'])
@login_required
def deleteJob():
    if request.method == 'POST':
        jobId = request.data
        print(jobId)
        print("testing")
        #file = request.files['attachmentName']
        #if file and allowed_file(file.filename):
#            # Set up upload folder
#            # basedir = os.path.abspath(os.path.dirname(__file__))
##            updir = os.path.join(app.config['basedir'], 'static/images/user/')#

#            # Delete old file
##            delete_file = current_user.get_id().get('dp', None)
##            if delete_file:
#                delete_file = delete_file.split('/', -1)[-1]
#                delete_file = os.path.join(updir, delete_file)
#                if os.path.exists(delete_file):
#                    os.remove(delete_file)#

#            # Get filename
#            filename = secure_filename(file.filename)
#            filename = md5((filename + current_user.get_id().get('username')).encode('utf-8')).hexdigest()#

#            # Upload file to server
#            path = os.path.join(updir, filename)
#            file.save(path)#

#            # Save path to database
#            relative_path = os.path.join(url_for('static', filename='images/user/'), filename)
#            user = {
#                "dp"    : relative_path
#            }
#            savvy_collection.update({"username": current_user.get_id().get('username')},
#                                    {"$set": user})#
#

#            # return information to frontend
           return jsonify(path=relative_path)