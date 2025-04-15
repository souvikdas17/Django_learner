from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router=DefaultRouter()
router.register('employees', views.EmployeeViewSet, basename='employee')
urlpatterns=[
    path('students', views.StudentsView),
    path('students/<int:pk>',views.StudentsDetailView),
    # path('employees/', views.Employees.as_view()),
    # path('employees/<int:pk>', views.EmployeeDetails.as_view()),
    path('', include(router.urls)),
    path('blogs/', views.BlogsView.as_view()),
    path('comments/', views.CommentsView.as_view()),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view()),
    path('comments/<int:pk>/',views.CommentDetailView.as_view()),
    path('register/',views.RegisterUser.as_view()),
]
