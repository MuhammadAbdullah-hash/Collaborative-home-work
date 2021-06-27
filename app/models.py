from django.db import models
from django import forms

# Create your models here.

class New_user(models.Model):
	name = models.CharField(max_length=30 , unique=True , default='' )
	user_pass = models.CharField(max_length=30 , default='')
	is_admin = models.BooleanField(default=False)
	
	@property
	def get_attr(self):
		return f'{self.name} {self.user_pass} {self.is_admin}'
	
	def __str__(self):
		return f'{self.name}'


class Question(models.Model):
	name = models.CharField(max_length=30 , default='')
	body = models.TextField(default='')
	rating = models.IntegerField( default=0 )
	file = models.ImageField(upload_to='app/quest', default="" , blank = True )
	date_created = models.DateField(auto_now_add=True)

	def save(self):
		if New_user.objects.filter(name = self.name).count() == 1 : 
			super().save()
			
		else : 
			raise forms.ValidationError( 'Username downt exist already' )

	def __str__(self):
		return f'{self.name} question-id : {self.id}'


class Answers(models.Model):
	quest_id = models.IntegerField()
	name_ans = models.CharField(max_length=30 , default='') 
	body = models.TextField(default='')
	rating = models.IntegerField( default=0 )
	file = models.ImageField(upload_to='app/quest', default="" , blank = True )
	date_created = models.DateField(auto_now_add=True)

	def save(self):
		lis = [ each_ques.id for each_ques in Question.objects.all() ] 
		if self.quest_id in lis:
			super().save()
		else : 
			raise forms.ValidationError( 'Question with this id doent exist' )


	def __str__(self):
		return f'Q.{self.quest_id} Answer:{self.id}'






