from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password
from .models import Books, Emprunt, Users

from django.contrib.auth.hashers import make_password

def no_cache(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return _wrapped_view_func
@no_cache
def home(request):
    if not request.session.get("user_id"):
        return redirect("login")

    if request.session.get("role") == "admin":
        return redirect("admin_emprunts")
    else:
        return redirect("book_list")

@no_cache
def register(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))
        role = "user"

        Users.objects.create(nom=nom, email=email, password=password, role=role)
        return redirect("login")
    error ="il ya une erreur"
    return render(request, "register.html",{'error' : error})


@no_cache
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Users.objects.get(email=email)
            if check_password(password, user.password):
                # Store user data in session
                request.session["user_id"] = user.id
                request.session["role"] = user.role

                # Redirect based on role
                if user.role == "admin":
                    return redirect("book_list")
                elif user.role == "user":
                    return redirect("user_emprunts")
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        except Users.DoesNotExist:
            return render(request, "login.html", {"error": "User does not exist"})

    return render(request, "login.html")



@no_cache
def logout(request):
    request.session.flush()
    cache.clear()
    response = redirect("login")

    return response


@no_cache
def book_list(request):
    if not request.session.get('user_id'):  
        return redirect('login')  
    if request.session.get("role") == "admin":
        books = Books.objects.all()
        return render(request, "books/book_list.html", {"books": books})
    return redirect('login')  

@no_cache
def book_create(request):
    if request.method == "POST":
        Books.objects.create(
            titre=request.POST["titre"],
            auteur=request.POST["auteur"],
            genre=request.POST["genre"],
            annee_publication=request.POST["annee_publication"],
            exemplaires_disponibles=request.POST["exemplaires_disponibles"],
        )
        return redirect("book_list")
    return render(request, "books/book_form.html")

@no_cache
def book_update(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if request.method == "POST":
        book.titre = request.POST["titre"]
        book.auteur = request.POST["auteur"]
        book.genre = request.POST["genre"]
        book.annee_publication = request.POST["annee_publication"]
        book.exemplaires_disponibles = request.POST["exemplaires_disponibles"]
        book.save()
        return redirect("book_list")
    return render(request, "books/book_form.html", {"book": book})

@no_cache
def book_delete(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "books/book_confirm_delete.html", {"book": book})

@no_cache
def user_emprunts(request):
    if not request.session.get('user_id'):  
        return redirect('login')  
    
    user = get_object_or_404(Users, id=request.session['user_id'])  
    emprunts = Emprunt.objects.filter(user=user)  
    
    return render(request, "emprunts/user_emprunts.html", {"emprunts": emprunts})

@no_cache
def create_emprunt(request):
    if not request.session.get('user_id'):
        return redirect('login')  
    
    user = get_object_or_404(Users, id=request.session['user_id'])  
    
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        date_retour_prevue = request.POST.get("date_retour_prevue")

        if not book_id or not date_retour_prevue:
            return render(
                request,
                "emprunts/create_emprunt.html",
                {"error": "Please select a book and provide a return date."},
            )
        book = get_object_or_404(Books, id=book_id)

        
        if book.exemplaires_disponibles > 0:
            Emprunt.objects.create(
                book=book,
                user=user,  
                date_emprunt=now(),
                date_retour_prevue=date_retour_prevue,
            )

            book.exemplaires_disponibles -= 1
            book.save()

            return redirect("user_emprunts")
        else:
            return render(
                request,
                "emprunts/create_emprunt.html",
                {"error": "No copies available for this book."},
            )

    
    books = Books.objects.filter(exemplaires_disponibles__gt=0)
    return render(request, "emprunts/create_emprunt.html", {"books": books})


def return_book(request, emprunt_id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = get_object_or_404(Users, id=user_id)
    emprunt = get_object_or_404(Emprunt, id=emprunt_id, user_id=user)

    if emprunt.date_retour_reelle is None:
        emprunt.date_retour_reelle = now()
        emprunt.save()
        emprunt.book.exemplaires_disponibles += 1
        emprunt.book.save()
    return redirect("user_emprunts")


@no_cache
def admin_emprunts(request):
    if not request.session.get('user_id'):  
        return redirect('login')  
    emprunts = Emprunt.objects.all()
    return render(request, "emprunts/admin_emprunts.html", {"emprunts": emprunts})

@no_cache
def approve_reject_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "approve":
            if emprunt.book.exemplaires_disponibles > 0:
                emprunt.book.exemplaires_disponibles -= 1
                emprunt.book.save()
            else:
                return render(
                    request,
                    "emprunts/approve_reject.html",
                    {"emprunt": emprunt, "error": "No copies available."},
                )
        elif action == "reject":
            emprunt.book.exemplaires_disponibles += 1
            emprunt.delete()
        return redirect("admin_emprunts")
    return render(request, "emprunts/approve_reject.html", {"emprunt": emprunt})

@no_cache
def overdue_emprunts(request):
    if not request.session.get('user_id'):  
        return redirect('login')  
    overdue = Emprunt.objects.filter(
        date_retour_prevue__lt=now(), date_retour_reelle__isnull=True
    )
    return render(request, "emprunts/overdue_emprunts.html", {"overdue": overdue})
