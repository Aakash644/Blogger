from django.shortcuts import render
from pyrebase import pyrebase 
import os 
from distutils.log import debug
from fileinput import filename
from werkzeug.utils  import secure_filename 

firebaseConfig = {
    "apiKey": "AIzaSyCiDJ61Z2YZgXFTC9KCtRXmjKXxKmZGwGc",
    "authDomain": "instant-grove-373708.firebaseapp.com",
    "projectId": "instant-grove-373708",
    "storageBucket": "instant-grove-373708.appspot.com",
    "messagingSenderId": "292404888439",
    "appId": "1:292404888439:web:22859bda3270414347d772",
    " measurementId": "G-3CW5VS1MBC",
    "databaseURL": "https://instant-grove-373708-default-rtdb.asia-southeast1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(firebaseConfig)
db=firebase.database()
auth=firebase.auth()
storage=firebase.storage()
# try:
#    email=input("enter your email")
#    password=input("enter your password")
#    auth.sign_in_with_email_and_password(email,password)
# except:
#     print("invalid user or password")

# signup
# email=input("enter your email")
# password=input("enter your password")
# confirm_password=input("enter your password again")
# if(password==confirm_password):
#     auth.create_user_with_email_and_password(email,password)
# else:
#     print("Both passwords are different.\n")


# storage
# filename=input("enter the filename:")
# cloudfilename=input("enter the cloud filename:")
# storage.child(cloudfilename).put(filename)

# data = {
#     "name": "Aakash",

#     "gender": "male",
#     "dob": "25/03/2002",
#     "email": "aakshkr10@gmail.com"
# }
# db.child("user").child("user1").set(data)


from flask import  *
app=Flask(__name__,template_folder="templates",static_folder="templates/img")
app.config['UPLOAD_FOLDER'] = "C:\\Users\\Acer\\Desktop\\New folder (4)\\templates\\img"
@app.route('/home',methods=['GET','POST'])
def home(): 
  blogs=db.child("blogs").get()
  blogs1=blogs.val()   
  bloglist=[]
  for blog in blogs1:
    bloglist.append(blog) 
  return render_template("index.html",blogs1=blogs1,bloglist=bloglist)

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/pricing')
def pricing():
  return render_template("price.html")

@app.route('/contact')
def contact():
  return render_template("contact.html")

@app.route('/signin',methods=['GET','POST'])
def signin():
  status=""
  if(request.method=='POST'):
    email=request.form.get("email")
    password=request.form.get("password")
    return redirect("/addblog/admin")
  return render_template("signin.html",status=status)

@app.route('/signup',methods=['GET','POST'])
def signup():   
  status=""
  if(request.method=='POST' and request.form.get("email")!="" and request.form.get("password")!="" and request.form.get("fname")!="" and request.form.get("lname")!="" and request.form.get("date")!="" and request.form.get("inlineRadioOptions")!=""):
    email=request.form.get("email")
    password=request.form.get("password")
    dob=request.form.get("date")
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    gender=request.form.get("inlineRadioOptions")
    user=fname+" " +lname 
    
    data={"user":user,"dob":dob,"email":email,"password":password,"gender":gender}
  
    auth.create_user_with_email_and_password(email,password) 
    user_number=len(db.child("users").get().val())
    user_number+=1
    user_data=db.child("users").child(user_number).set(data) 
    status="Account created Successfully" 
    return redirect("/addblog/admin")

  return render_template("signup.html",status=status)

@app.route('/add/<user>',methods=['GET','POST'])
def add(user):  
  status=""
  if(request.method=='POST'  and request.form.get("title")!="" and request.form.get("author")!="" and request.form.get("content")!="" ): 
    title=request.form.get("title")
    author=request.form.get("author")
    content=request.form.get("content") 
    desc=request.form.get("desc")   
    f = request.files['file'] 
    print(f)
    # f.save(f.filename) 
    data={"title":title,"author":author,"content":content,"desc":desc}
    print(data)
    db.child("blogs").child(title).set(data)
    status="Blog added successully" 
    
  return render_template("add.html",status=status)

@app.route('/addblog/<user>',methods=['GET','POST'])
def addblog(user):
  status=""  
  
 
  
  #firebase doesn't give us the secondary access i.e we as grandfather cannot cannot access my nephew data
  blogs=db.child("blogs").get()
  blogs1=blogs.val()   
  bloglist=[]
  for blog in blogs1:
    bloglist.append(blog) 
  #blogs authors    
 
  authorlist=[] 
  blog1=bloglist[0]
  
  for blog2 in bloglist:
    blog3=db.child("blogs").child(blog2).child("author").get() 
    authorlist.append(blog3.val())  
  userindex=[]
  for i in range(0,len(authorlist)): 
    userindex.append(i) 
  userblog=[bloglist[i] for i in userindex]
  

  
  return render_template("crud.html",user=user,status=status,blogs1=blogs1,userblog=userblog)

@app.route("/blogread/<title>",methods=["POST","GET"])
def blogread(title): 
  status=""
  blogs1=db.child("blogs").get()
  bloggs1=blogs1.val()   
  bloglist=[]
  for blog in bloggs1:
    bloglist.append(blog) 
  blogs=db.child("blogs").child(title).get() 
  blog1=blogs.val() 
  #retrieve comments 
  try:
    comment=db.child("blogs").child(title).child("comment").get()
    comments=comment.val()
  except:
    pass
  if(request.method=="POST" ):
    name=request.form.get("name")
    comment=request.form.get("comment") 
    print(name)
    db.child("blogs").child(title).child("comment").set({"name":name,"comment":comment}) 
    status="Comment posted successfully"

  return render_template("blog1.html",blog1=blog1,bloggs1=bloggs1,comments=comments,bloglist=bloglist,status=status) 

@app.route("/delete/<title>/<user>",methods=["POST","GET"])
def delete(title,user): 
  blogs=db.child("blogs").child(title).get() 
  blog=blogs.val() 
  status=""

  if(request.method=="POST" ):
    
    db.child("blogs").child(title).remove()
    status="deleted successfully"
  return render_template("delete.html",blog=blog,user=user, status=status)
  

@app.route("/update/<title>",methods=["POST","GET"])
def update(title):  
  status=""
  if(request.method=='POST' ):  
    to_update=request.form.get("update") 
    content=request.form.get("content")
    data={to_update:content}  
    db.child("blogs").child(title).update(data)  
    status="Blog updated successfully"
    
  return render_template("update.html",title=title,status=status)
app.run(debug = True)
  