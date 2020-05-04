""" 
Main file of the application
"""

# Flask libraries
from flask import render_template, url_for, request, redirect, flash, session
from flask_paranoid import Paranoid


# Local modules
from app import _create_app
from app.db.firebase import CrudDB, Authentication

# Utilities
from werkzeug.exceptions import HTTPException # Handler errors web
import requests
import uuid
import random
import pdb # Tests in mode console, execute: pdb.set_trace() anywhere


# Creation of the application IMPORTANT
app = _create_app() 
paranoid = Paranoid(app) # Session hash


@app.route('/', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def index():
    """ 
    Funtion manager to show the
    home of the app
    """

    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        uid = uuid.uuid4()
        active_session = True
        employer = True
        active_form = True
        
        context = { 
            'uid': uid,
            'employer': employer,
            'active_form': active_form,
            'active_session': active_session
            
        }

        return render_template('index.html', **context)
    

@app.route('/active', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def active():
    """
    Function manager to make alteration in the
    file 'base.html'
    """
    
    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        active_session = True
        
    return render_template('base.html', active_session=active_session)
    
        
@app.route('/validate', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def validate():
    """ 
    Funtion manager to validate the
    information of the form.
    """

    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        if request.method == 'POST':
            info = {key: value for key, value in request.form.items()}
            create = request.form['checkin']
            
            if create:    
                flash('The new employer {} was added with the ID {} successfully!'.format(
                    info['name'], 
                    info['id'])
                ) # Success
            
                CrudDB(info).create()
                
            return redirect(url_for('index'))
                
        else:
            flash('Something was wrong!') # Wrong
            
            return redirect(url_for('index'))


@app.route('/search-by-id', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def search_by_id():
    """
    Funtion manager to search the id of the
    employers by their id.
    """
    
    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        if request.method == 'POST':
            info = {key: value for key, value in request.form.items()}
            checkout = request.form['checkout']

            if checkout:     
                try:
                    data = CrudDB(info).read()

                    flash('The employer {} was checked out successfully!'.format(info['id'])) # Check Out
                    
                    return redirect('checkout/{}/{}'.format(info['id'], data))
                
                except AttributeError:
                    flash('Please check you are writting the ID correctly and without any SPACE.')
        
        active_session = True
                        
        return render_template('search_by_id.html', active_session=active_session)
    
    
@app.route('/checkout/<uid>/<data>', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def checkout(uid, data):
    """
    Funtion manager to show the info of the
    employers checked out.
    """
    
    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        if request.method == 'POST':
            check = [i for i in request.form]
            info = {key: value for key, value in request.form.items()}
            
            update = check[10]; delete = check[10]

            if update == 'update':
                flash('The employer {} was updated successfully!'.format(info['name'])) # Update
            
                CrudDB(info).update()
                
                return redirect(url_for('index'))
            
            elif delete == 'delete':
                flash('The employer {} was deleted successfully!'.format(info['name'])) # Delete
            
                CrudDB(info).delete()
                
                return redirect(url_for('index'))
        
        employer_id = uid  
        dates = data
        active_form = False
        active_session = True
        
        # Change the string
        replacement = dates.replace('[', '')\
            .replace(']', '')\
            .replace('(', '')\
            .replace(')', '')\
            .replace("'", '')
        
        employer = [i.strip(' ') for i in replacement.split(',')]
    
        context = {
            'employer_id': employer_id,
            'employer': employer, 
            'active_form': active_form,
            'active_session': active_session
        }
        
        return render_template('checkout.html', **context)


@app.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    """
    Function manager to show the sign up
    page.
    """
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            Authentication(email, password).signup()
            
            flash('Please check your email and validate your new account!')
            
            return redirect(url_for('login'))
        
        except requests.exceptions.HTTPError:
            flash('Something was wrong with your sing up!')
            
            return redirect(url_for('signup'))
        
    return render_template('signup.html')
        


@app.route('/auth/signin', methods=['GET', 'POST'])
def login():
    """
    Function manager to show the sign in
    page.
    """
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            auth = Authentication(email, password).login()
            
            if auth == 'email_no_verified':
                flash('Please check out if your email account is verified!')
                
                return redirect(url_for('login'))
            
            else:
                session['user_session'] = random.randint(1, 10000)
                
                flash('You are in now!')
                
                return redirect(url_for('index'))
                
        except requests.exceptions.HTTPError:
            flash('Something was wrong with your credentials!')
            
            return redirect(url_for('login'))
        
    return render_template('login.html')


@app.route('/auth/signout', methods=['GET', 'POST'])
@paranoid.on_invalid_session
def logout():
    """
    Function manager to show the sign out
    page.
    """
    
    if not session.get('user_session'):
        flash('Please log in first!')
        
        return redirect(url_for('login'))
    
    else:
        session.pop('user_session')
        session.pop('_paranoid_token')
        
        flash('You are log out now!')
        
        return redirect(url_for('login'))


@app.route('/auth/reset-password', methods=['GET', 'POST'])
def reset_password():
    """
    Function manager to show the form to reset
    the password.
    """
    
    if request.method == 'POST':
        email = request.form['email']
        
        try:
            Authentication(email, 'reset_password').reset_password()
        
            flash('We have send a link to your email for reset the password!')
        
            return redirect(url_for('login'))

        except requests.exceptions.HTTPError:
            flash('Something was wrong with your email, please register first!')
            
            return redirect(url_for('signup'))
        
    return render_template('reset_password.html')


@app.errorhandler(Exception)
def errors(error):
    """
    Function manager to show the error
    page to the users.
    """
    
    code_error = 'Oh no, bad luck!'
    
    if isinstance(error, HTTPException):
        code_error = error
        
    return render_template('errors.html', code_error=code_error)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
    
