from flask import Flask, render_template, request
import boto3
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'automated-reciepts-mahesh'
S3_FOLDER = 'incoming/'
AWS_REGION = 'us-east-1'

# Initialize S3 client (Ensure AWS credentials are configured)
s3 = boto3.client('s3', region_name=AWS_REGION)

@app.route('/', methods=['GET', 'POST'])
def upload():
    messages = []
    if request.method == 'POST':
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                s3.upload_fileobj(file, S3_BUCKET, f'{S3_FOLDER}{filename}')
                messages.append(f"✅ '{filename}' uploaded successfully!")
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
