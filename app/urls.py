from django.urls import path
from . views import Home_page  , Prof_view , Query_ans

urlpatterns = [
    path(''  , Home_page.Sign_in.as_view() , name = 'sign_in' ),
    path('sign_up/' , Home_page.Sign_up.as_view() , name = 'sign_up' ),
    path('prof_view/' , Prof_view.as_view() , name = 'prof_view'), 
    path('query_ans/<str:ques_id>' , Query_ans.as_view() , name = 'query_ans')

]
