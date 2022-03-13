import os
from flask import request, jsonify, redirect, send_file, Flask, render_template
from config import app

from werkzeug.utils import secure_filename
from models.aws_helper import upload_file

ALLOWED_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}


# function to check file extension
def allowed_image_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGES


@app.route("/api_upload_image", methods=['POST'])
def api_upload_images():
    """if request.method == "POST":
        f = request.files['file']
        if f:
            print(f)
            f.save(secure_filename(f.filename))
            print(secure_filename(f.filename))
            r = upload_file(secure_filename(f.filename), os.environ.get('S3_BUCKET', None))
            if r.status_code == "200":
                return jsonify({'success': True, 'message': r.content})
            return jsonify({'success': False, 'message': "Cannot upload image to AWS"})"""

    file = request.files['file']

    # check whether a file is selected
    if not file or file.filename == '':
        return jsonify({'success': False, 'message': 'No file selected'})

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_image_file(file.filename):
        output = upload_file(file, os.environ.get('S3_BUCKET', None), os.environ.get('USER_IMAGES', None))

        # if upload success,will return file name of uploaded file
        if output:
            # write your code here
            # to save the file name in database
            return jsonify({'success': True, 'message': 'Successfully uploaded image'})

        # upload failed, redirect to upload page
        else:
            return jsonify({'success': True, 'message': 'Failed to upload image'})

    # if file extension not allowed
    else:
        return jsonify({'success': True, 'message': "File type not accepted,please try again."})


@app.route("/upload_image", methods=['POST'])
def upload_images():
    if request.method == "POST":
        f = request.files['file']
        path = os.environ.get('USER_IMAGES', None)
        bucket = os.environ.get('S3_BUCKET', None)
        f.save(os.path.join(path, secure_filename(f.filename)))
        r = upload_file(f"uploads/{f.filename}", bucket)
        """if r.status_code == "200":
            return jsonify({'success': True, 'message': r.content})
        return jsonify({'success': False, 'message': "Cannot upload image to AWS"})"""
        print(r)
        return redirect("/index")


@app.route("/upload_doc", methods=['POST'])
def upload_docs():
    if request.method == "POST":
        f = request.files['file']
        path = os.environ.get('USER_IMAGES', None)
        bucket = os.environ.get('S3_BUCKET', None)
        f.save(os.path.join(path, secure_filename(f.filename)))
        r = upload_file(f"uploads/{f.filename}", bucket)
        if r.status_code == "200":
            return jsonify({'success': True, 'message': r.content})
        return jsonify({'success': False, 'message': "Cannot upload image to AWS"})
