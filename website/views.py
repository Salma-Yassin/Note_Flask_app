from flask import Blueprint , render_template, request , flash
from flask_login import login_required, current_user
from .models import Note 
from . import db  
import json
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/' , methods = ['GET','POST'])
@login_required # you can not go to the homepage until you are logged in 
def home(): 
   if request.method == 'POST':
    note = request.form.get('note') # Gets the note from html
    
    if len(note) < 1:
      flash('Note is too short!',category = 'error')
    else:
      new_note = Note(data = note , user_id = current_user.id)
      db.session.add(new_note) # adding note to the database
      db.session.commit()
      flash('Note added!',category = 'session')
   return render_template('home.html' , user = current_user) # check if the logged in user is authenticated 


@views.route('/delete-note' , methods = ['POST'])
def delete_note():
  note = json.loads(request.data) # this function expects a JSON from the index.js file
  noteId = note['noteId']
  note=Note.query.get(noteId)

  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
  return jsonify({})  
