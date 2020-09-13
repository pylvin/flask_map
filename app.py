from flask import Flask, render_template, redirect, request, url_for, flash
from database.models import Geolocation
from database.sqlite import Sqlite
from forms import createForm, updateForm
from utility import Paginate, removekey

app = Flask(__name__)
app.config['SECRET_KEY'] = "f0ee25b4-cd48-4b26-9fe4-1e33cf28ff05"

# Context Proccessors
@app.context_processor
def counter():
    def _counter(current_page, pages_count):
        if current_page == 1:
            current_page = 2
        if current_page >= pages_count and pages_count > 2:
            current_page -= 1
        if pages_count == 1 or pages_count == 2:
            return range(1, pages_count+1)
        return range(current_page-1, current_page+2)
    return dict(counter=_counter)

# Главная страница
@app.route('/', methods=["GET", "POST"])
def index():
    context = {}
    form = createForm()
    if request.method == "POST" and form.validate_on_submit():
        data = form.data
        Sqlite().create(Geolocation,
                        longtitude=data["longtitude"], latitude=data["latitude"], id=data["id"],
                        name_geolocation=data["name_geolocation"], hashtag1=data["hashtag1"],
                        hashtag2=data["hashtag2"])
        flash("Локация добавлена", "success")
        return redirect('/items')
    context['form'] = form
    return render_template('index.html', **context)

# Страница локаций
@app.route('/items', methods=["GET"])
def items():
    context = {}
    query = Sqlite().query_all(Geolocation)
    page = abs(int(request.args.get("page"))) if request.args.get("page") is not None else 1
    paginator = Paginate(query, page, 5)
    pages_count = paginator.pages_count()
    current_page = page
    has_next = paginator.has_next()
    context["items"] = paginator.paginate()
    context["pages_count"] = pages_count
    context["current_page"] = current_page
    context["has_next"] = has_next
    if page > pages_count or page <= 0:
        return redirect('/items')
    return render_template('items.html', **context)

# Страница редактирования
@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    context={}
    form = updateForm(obj=Sqlite().query(Geolocation, id=id))
    if request.method=="POST":
        try:
            data = removekey(form.data, "csrf_token")
            Sqlite().update(Geolocation, id, **data)
            flash("Данные обновлены", "success")
            return redirect(url_for('items'))
        except:
            flash("Данные неверны", "danger")
            return redirect(url_for('items'))
    context['form'] = form
    return render_template('update.html', **context)

# Endpoint удаления
@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    if request.method == "POST":
        Sqlite().delete(Geolocation, id)
        return redirect('/items')

if __name__ == '__main__':
    app.run(debug=True)
