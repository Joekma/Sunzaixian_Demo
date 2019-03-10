"""sunzaixian URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from api import views_old
from django.views.static import serve
from sunzaixian import settings
from api.views import CourseView,LoginView,ShoppingView,PayView
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^courses/', views_old.Coures.as_view()),
    # url(r'^test1/', views_old.test1),
    # url(r'^test2/', views_old.test2),
    # url(r'^test3/', views_old.test3),
    # url(r'^add_price/', views_old.add_price),
    # 开media的口
    url(r'^media/(?P<path>.*)', serve,{'document_root':settings.MEDIA_ROOT}),

    url(r'^courses/', CourseView.Courses.as_view()),
    url(r'^course/(?P<pk>\d+)', CourseView.Course.as_view()),
    url(r'^login/', LoginView.Login.as_view()),
    url(r'^shoppingcart/', ShoppingView.Shopping.as_view()),
    url(r'^payment/', PayView.Pay.as_view()),

]
