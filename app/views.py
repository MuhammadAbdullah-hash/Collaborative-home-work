from django.http import HttpResponse , HttpResponseRedirect , JsonResponse , QueryDict
from django.shortcuts import render , redirect
from . models import New_user , Question  , Answers
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Create your views here.



class Home_page:

	@method_decorator(csrf_exempt, name='dispatch')
	class Sign_in(View):
		def get(self , request):
			if 'user_id' in request.session :
				return redirect('prof_view/')
			else: 
				return render(request, 'app/register.html')
		
		def post(self , request):
			user = request.POST.get('user')
			user_pass = request.POST.get('pass')

			obj = New_user.objects.filter(name = user , user_pass = user_pass)
			if len(list(obj)) == 0 :  msg = {'user' : user , 'pass' : user_pass , 'flag' : False}
			elif len(list(obj)) == 1 :
				request.session['user_id'] = obj[0].id
				msg = {'user' : user , 'pass' : user_pass , 'flag' : True}
			else :  msg = {'flag' : False}
			return JsonResponse(msg)

	@method_decorator(csrf_exempt, name='dispatch')
	class Sign_up(View):
		def get(self , request):
			return render(request, 'app/signup.html')
		def post(self ,  request):
			user = request.POST.get('username')
			user_pass = request.POST.get('pass')
			user_pass_conf = request.POST.get('conf-pass')
			if  New_user.objects.filter(name = user.strip()).count()  == 0  :
				new_user = New_user(name = user , user_pass = user_pass)
				new_user.save()
				msg = {'msg' : 'Account created Succesfully' , 'flag' : True }
				return JsonResponse(msg)
			else : 
				msg = {'msg' : 'Sorry user name already exist' , 'flag' : False }				
				return JsonResponse(msg)



@method_decorator(csrf_exempt, name='dispatch')
class Prof_view(View):
	def get(self , request):
		if 'user_id' in request.session : 
			curr_user = New_user.objects.get(id = request.session['user_id'])
			quest = [ (j.name , j.body , j.rating , j.id) for j in Question.objects.all()]
			dic={}
			for obj in Question.objects.all():
				if obj.id not in dic.keys():
					ans = Answers.objects.filter( quest_id = obj.id )
					dic.update({
						obj.id : [ (obj.name , obj.body , obj.rating , obj.id),
						[(j.name_ans , j.body , j.rating , j.id) for j in ans] 
					]})
					
			print(dic)

			params = {'user_name' : curr_user.name , "all_quest" : quest , 'example' : dic }
			return render(request, 'app/profile.html' , params)
		else :
			return HttpResponse('SORRY YOU ARE NOT ALLOWED TO VIEW THIS PAGE WITHOUT LOGGIN IN  ')
	
	def post(self , request):
		flag = request.POST.get( 'flag' )
		body , file_path = request.POST.get('body') , request.POST.get('file_path')
		if flag == 'logout' : 
			del request.session['user_id']
			msg = {'msg' : 'yes logging out' , 'flag-return' : flag }

		elif body != None : 
			crr_user = New_user.objects.get(id = request.session['user_id'])
			obj = Question(name = crr_user.name , body = body , file = file_path )
			obj.save()
			msg = {'name': crr_user.name , 'body' : body , 'file_path' : file_path , 'sucess' : True}
		
		return JsonResponse(msg)


	def put(self , request):
		data = QueryDict(request.body)
		body , count  = data.get('body') , data.get('count')
		try : 
			count = int(count)
			obj = Question.objects.get( id=body )
			obj.rating = count
			obj.save()
			msg = {'body' : body , 'count' : count , 'sucess' : True}
		except : msg = {'body' : body , 'count' : count , 'sucess' : False}
		
		return JsonResponse(msg)




@method_decorator(csrf_exempt, name='dispatch')
class Query_ans( View ):
	def get(self , request , ques_id = None) : 
		if 'user_id' in request.session : 
			try : 
				ques_id = int(ques_id)
				query_set = Question.objects.get(id = ques_id)
			except Exception as e : return HttpResponse(f'Following Error occured \n {e}') 
	
			curr_user = New_user.objects.get(id = request.session['user_id'])
			ans_ques = [ (j.name_ans , j.body , j.rating , j.id) for j in Answers.objects.filter( quest_id = ques_id )]
			if len(ans_ques) == 0 : sucess = False
			elif len(ans_ques) > 0 : sucess = True
			params = {'user_name' : curr_user.name , 'question' : query_set.body , 
							'all_quest' : ans_ques ,
							'sucess' : sucess }

			return render(request, 'app/query.html' , params)
		else : return HttpResponse('Sorry you are not allowoed to view this page WITHOUT logging in')	
	
	def post(self , request , ques_id = None):
		flag = request.POST.get( 'flag' )
		body , file_path = request.POST.get('body') , request.POST.get('file_path')
		if flag == 'logout' : 
			del request.session['user_id']
			msg = {'msg' : 'yes logging out' , 'flag-return' : flag }

		elif body != None : 
			crr_user = New_user.objects.get(id = request.session['user_id'])
			new_obj = Answers(name_ans = crr_user.name, quest_id = int(ques_id) , body = body , file = file_path )
			new_obj.save()
			msg = {'body' : body , 'file_path' : file_path , 'id' : new_obj.id , 'sucess' : True}
			
		return JsonResponse(msg)

	def put(self , request , ques_id = None):
		data = QueryDict(request.body)
		body , count  = data.get('body') , data.get('count')
		try : 
			count = int(count)
			obj = Answers.objects.get( id=body )
			obj.rating = count
			obj.save()
			msg = {'body' : body , 'count' : count , 'sucess' : True}
		except : msg = {'body' : body , 'count' : count , 'sucess' : False}
		
		return JsonResponse(msg)
	
