from django.urls import include, path


from apps.api.views import views


# api
urlpatterns = [

    #signup
    path('signup/', views.signup),

    #signin

    #list
    path('list/', views.list),

    #request-for-cab
    path('request/allocation/', views.allocation),

    #request-for-allocation
    path('request/assignment/', views.assignment),

]
