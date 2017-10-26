from __future__ import unicode_literals
from django.db import models
import bcrypt, re
from datetime import datetime
from time import strftime,localtime

class UserManager(models.Manager):
    def login(self,post):
        username = post['log_username']
        users = self.filter(username = username)
        if users:
            user = users[0]
            if bcrypt.checkpw(post['log_password'].encode(),user.password.encode()):
                return user
        return False

    def regValidation(self, post):
        name = post['name']
        username = post['username']
        password = post['reg_password']
        cpass = post['cpass']

        errors = []

        ##CHECK MOST STRICT VALS FIRST

        ## first name vals
        if len(name) < 1:
            errors.append('Must enter name')
        elif len(name) < 3:
            errors.append('Name must be at least 3 letters')

        ## last name vals
        if len(username) < 1:
            errors.append('Must enter username')
        elif len(username) < 3:
            errors.append('Username must be at least 3 letters')

        ## password vals
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        elif password != cpass:
            errors.append('Passwords must match')

        ## checks whether username has already been registered 
        if not errors:
            users = self.filter(username=username)
            if users:
                errors.append('This username has already been registered')

        return {'status': len(errors) == 0, 'errors':errors} #this says return a dictionary of the "errors" array and a status. If the length of arrays is 0

    def createUser(self,post):
        name = post['name']
        username = post['username']
        password = bcrypt.hashpw(post['reg_password'].encode(), bcrypt.gensalt())
        return self.create(name = name, username = username, password = password)
        ## ^ puts into in database query 'create' and enters everything into database

class ItemManager(models.Manager):
    def itemValidation(self,post):
        name = post['itemName']

        errors = []

        if len(name) == 0:
            errors.append('Must enter item')
        elif len(name) <4:
            errors.append('Item must be more than 3 characters')

        if not errors:
            item = self.filter(name=name)
            if item:
                errors.append('This item has already been listed')
        
        return {'status': len(errors) == 0, 'errors':errors}

    def createItem(self,post, user_id):
        name = post['itemName']
        added_by = User.objects.get(id=user_id)
        return self.create(name = name, added_by=added_by)

    def deleteItem(self, item_id, user_id):
        user = User.objects.get(id=user_id)
        item = Item.objects.get(id = item_id)
        Item.added_items.remove(item)
        return item

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager() ##connects an instance of UserManager to User model overwriting hidden objects key w new one

    def __str__(self):
        return 'Name: {} {}, Username: {}'.format(self.first_name,self.last_name,self.username)


class Item(models.Model):
    name = models.CharField(max_length = 500)
    added_by = models.ForeignKey(User, related_name='added_items', default = '')
    wished_by = models.ManyToManyField(User, related_name="wished_item", default = '')
    created_at = models.DateTimeField(auto_now_add = True)

    objects = ItemManager()

    def __str__(self):
        return 'Name: {}, Add By: {}'.format(self.name,self.added_by)