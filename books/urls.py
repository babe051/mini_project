from django.urls import path
from . import views

# urlpatterns = [
#     path("", views.home, name="home"),
#     path("register/", views.register, name="register"),
#     path("login/", views.login, name="login"),
#     path("", views.book_list, name="book_list"),
#     path("create/", views.book_create, name="book_create"),
#     path("<int:book_id>/edit/", views.book_update, name="book_update"),
#     path("<int:book_id>/delete/", views.book_delete, name="book_delete"),
#     path(
#         "user/emprunts/", views.user_emprunts, name="user_emprunts"
#     ),  # Update this line
#     path("new/", views.create_emprunt, name="create_emprunt"),
#     path("<int:emprunt_id>/return/", views.return_book, name="return_book"),
#     path("admin/", views.admin_emprunts, name="admin_emprunts"),
#     path(
#         "admin/<int:emprunt_id>/approve-reject/",
#         views.approve_reject_emprunt,
#         name="approve_reject_emprunt",
#     ),
#     path("admin/overdue/", views.overdue_emprunts, name="overdue_emprunts"),
# ]
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('books/', views.book_list, name='book_list'),
    path('logout/', views.logout, name='logout'),
    path("create/", views.book_create, name="book_create"),
    path("<int:book_id>/edit/", views.book_update, name="book_update"),
    path("<int:book_id>/delete/", views.book_delete, name="book_delete"),
    path("user/emprunts/", views.user_emprunts, name="user_emprunts"),
    path("new/", views.create_emprunt, name="create_emprunt"),
    path("<int:emprunt_id>/return/", views.return_book, name="return_book"),
    path("admin/", views.admin_emprunts, name="admin_emprunts"),
    path(
        "admin/<int:emprunt_id>/approve-reject/",
        views.approve_reject_emprunt,
        name="approve_reject_emprunt",
    ),
    path("admin/overdue/", views.overdue_emprunts, name="overdue_emprunts"),
]

