from django.shortcuts import render
from .models import Movie

from django.shortcuts import render
from .models import Movie

def home(request):
    search_term = request.GET.get('searchMovie', '')
    movies_qs = Movie.objects.all()

    if search_term:
        movies_qs = movies_qs.filter(title__icontains=search_term)

    context = {
        "searchTerm": search_term,
        "movies": movies_qs,
    }
    return render(request, "home.html", context)

def signup(request):
    # Soporta GET o POST
    email = request.GET.get('email') or request.POST.get('email') or ''

    return render(request, 'signup.html', {'email': email})



def statistics_view(request):
    # Importar aquí evita que manage.py reviente si aún no está instalado matplotlib
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io
    import base64

    all_movies = Movie.objects.all()

    movie_counts_by_year = {}
    for movie in all_movies:
        year = movie.year if movie.year is not None else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    def sort_key(x):
        if x == "None":
            return 10**9
        try:
            return int(x)
        except:
            return 10**9

    years_sorted = sorted(movie_counts_by_year.keys(), key=sort_key)
    values_sorted = [movie_counts_by_year[y] for y in years_sorted]

    bar_positions = range(len(years_sorted))

    plt.bar(bar_positions, values_sorted, width=0.5, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, years_sorted, rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'statistics.html', {'graphic': graphic})