from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

# Home route: show all notes for the logged-in user
@views.route('/')
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes)

# Add a new note (POST only)
@views.route('/add-note', methods=['POST'])
@login_required
def add_note():
    note_text = request.form.get('note')

    if not note_text or note_text.strip() == "":
        flash("Note cannot be empty.", category='danger')
    else:
        new_note = Note(content=note_text.strip(), user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!", category='success')

    return redirect(url_for('views.home'))

# Delete a note (POST only)
@views.route('/delete-note/<int:id>', methods=['POST'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)

    if note.user_id != current_user.id:
        flash("You don't have permission to delete this note.", category='danger')
    else:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted.", category='success')

    return redirect(url_for('views.home'))
