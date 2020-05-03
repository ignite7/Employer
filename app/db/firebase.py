"""
File manager to connect with the data base of
firestore.
"""

# Pyrebase libraries
import pyrebase


# Local modulues
from app.config import Config


# Utilities
import pdb


config = { 
  "apiKey": Config.API_KEY,
  "authDomain": Config.AUTH_DOMAIN,
  "databaseURL": Config.DATABASE_URL,
  "storageBucket": Config.STORAGE_BUCKET,
  "serviceAccount": Config.GOOGLE_AUTH_APP
}


class CrudDB(object):
    """
    Main class manager to intialize the connection
    with firebase.
    """
    
    def __init__(self, info):
        """
        Method manager to initialize the data base
        connection.
        """
        
        self.info = info
        
        self.firebase = pyrebase.initialize_app(config)
        
        self.database = self.firebase.database()
    
    def create(self):        
        self.database.child('employers').child(self.info['id']).set({
            'name': self.info['name'],
            'surname': self.info['surname'],
            'email': self.info['email'],
            'country': self.info['country'],
            'city': self.info['city'],
            'age': self.info['age'],
            'address': self.info['address'],
            'job': self.info['job'],
            'text': self.info['text']
        })
        
    def read(self):
        doc = self.database.child('employers').child(self.info['id']).get().val()
        
        return doc
        
    def update(self):
        self.database.child('employers').child(self.info['id']).update({
            'name': self.info['name'],
            'surname': self.info['surname'],
            'email': self.info['email'],
            'country': self.info['country'],
            'city': self.info['city'],
            'age': self.info['age'],
            'address': self.info['address'],
            'job': self.info['job'],
            'text': self.info['text']
        })
        
    def delete(self):
        self.database.child('employers').child(self.info['id']).remove()
        
        
class Authentication(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        
    def signup(self):
        self.user = self.auth.create_user_with_email_and_password(self.email, self.password)
        
        self.user = self.auth.send_email_verification(self.user['idToken'])
        
        
    def login(self):
        self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        
        check_email_verified = self.auth.get_account_info(self.user['idToken'])
        
        if check_email_verified['users'][0]['emailVerified'] == False:
            return 'email_no_verified'
        
        else:
            return self.user
    
    def logout(self):
        self.user = self.auth.signOut()
        
        return self.user
    