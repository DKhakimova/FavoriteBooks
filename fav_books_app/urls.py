from django.urls import path
from . import views

urlpatterns = [
    path('', views.books),
    path('create', views.create),
    path('<int:book_id>/update', views.update),
    path('<int:book_id>/delete', views.delete),
    path('<int:book_id>', views.show),
    path('favorite/<int:book_id>', views.favorite),
    path('unfavorite/<int:book_id>', views.unfavorite)

]