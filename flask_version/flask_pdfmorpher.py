from flask import Flask, render_template, request, send_file
import PyPDF2
import os
from werkzeug.utils import secure_filename
#from pdfmorpher import *


app = Flask(__name__)
#app.secret_key = 's_k'
#app.config['UPLOAD_FOLDER_ext'] = 'C:/Users/ralfk/Documents/Development/pdfmorpher/flask_version/tmp/extract'
app.config['UPLOAD_FOLDER_ext'] = os.path.abspath('tmp/extract')
#app.config['UPLOAD_FOLDER_mer'] = 'C:/Users/ralfk/Documents/Development/pdfmorpher/flask_version/tmp/merge'
app.config['UPLOAD_FOLDER_mer'] = os.path.abspath('tmp/merge')

flag_del_ext = False
flag_del_mer = False

@app.route('/')
def home():
    
    return render_template("start.html")

@app.route('/extract')
def extract_page():         
    
    return render_template("extract.html")
        
@app.route('/extract/selpages', methods=['GET', 'POST'])
def extract_selpages():  

    global pdfReader, file, filename_ext_in
    #filename_ext_in = request.args['inpath_ex']
        
    file = request.files.get("inpath_ex")
    filename_ext_in = file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER_ext'], filename_ext_in)
   
    #file = request.files.get("inpath_ex")
    file.save(filepath)    
    
    #pdfReader = PyPDF2.PdfReader(file,strict=False)   
    pdfReader = PyPDF2.PdfReader(filepath,strict=False)       
    lastpage=len(pdfReader.pages)
    
    return render_template("extract_selpages.html", page2=lastpage)
 
@app.route('/extract/forward')
def extract_pdf():
    
    global flag_del_ext
    
    startp = request.args.get("page1")
    endp = request.args.get("page2")   
    pdfWriter = PyPDF2.PdfWriter()    

    for pageNum in range(int(startp)-1,int(endp)):
        pageObj = pdfReader.pages[pageNum]             
        pdfWriter.add_page(pageObj)        
    
    filename_ext_out = 'Extracted_' + startp + '-' + endp + '_' + filename_ext_in
    filepath = os.path.join(app.config['UPLOAD_FOLDER_ext'], filename_ext_out) 
    pdfOutFile = open(filepath, 'wb')    
    
    pdfWiter = pdfWriter.remove_links()
    pdfWriter.write(pdfOutFile)
    pdfOutFile.close()  
    
    flag_del_ext = True
    return send_file(filepath, as_attachment=True)
    # return render_template("start.html")
    
    
@app.route('/merge')
def merge_page():
    
    return render_template("merge.html")

@app.route('/merge/forward', methods=['GET', 'POST'])
def merge_pdf():
    
    global flag_del_mer
    
    file1 = request.files.get("inpath_me1")
    filename_mer_in1 = file1.filename
    filepath1 = os.path.join(app.config['UPLOAD_FOLDER_mer'], filename_mer_in1)    
    file1.save(filepath1)   
    
    print(filename_mer_in1)
    
    file2 = request.files.get("inpath_me2")
    filename_mer_in2 = file2.filename
    filepath2 = os.path.join(app.config['UPLOAD_FOLDER_mer'], filename_mer_in2)    
    file2.save(filepath2) 
    
    pdfReader1 = PyPDF2.PdfReader(filepath1,strict=False)
    pdfReader2 = PyPDF2.PdfReader(filepath2,strict=False)    
    pdfWriter = PyPDF2.PdfWriter()
    
    for pageNum in range(len(pdfReader1.pages)):
        pageObj = pdfReader1.pages[pageNum]
        pdfWriter.add_page(pageObj)

    for pageNum in range(len(pdfReader2.pages)):			
        pageObj = pdfReader2.pages[pageNum]
        pdfWriter.add_page(pageObj)
        
    filename_mer_out = 'Merged_' + os.path.splitext(filename_mer_in1)[0] + '_' + filename_mer_in2
    filepath = os.path.join(app.config['UPLOAD_FOLDER_mer'], filename_mer_out) 
    pdfOutFile = open(filepath, 'wb')
    
    pdfWriter.write(pdfOutFile)
    pdfOutFile.close()

    flag_del_mer = True
    return send_file(filepath, as_attachment=True)
    
@app.after_request
def delete_file(response):
    
    global flag_del_ext, flag_del_mer
    
    if flag_del_ext:
        path = app.config['UPLOAD_FOLDER_ext']
        files = os.listdir(path)
        for file in files:
            try:
                os.remove(os.path.join(path, file))
            except: 
                pass
        flag_del_ext = False
        
    if flag_del_mer:
        path = app.config['UPLOAD_FOLDER_mer']
        files = os.listdir(path)
        for file in files:
            try:
                os.remove(os.path.join(path, file))
            except: 
                pass
        flag_del_mer = False     
        
    return response

    
if __name__ == '__main__':    
    app.run(debug=True)