from application import db, app, bcrypt
from application.forms import MusicSearchForm, AlbumForm, AlbumEditForm, RegistrationForm, LoginForm
from flask import flash, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from application.models import Album, Artist, Users
from application.tables import Results

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='about')

@app.route('/index', methods=['GET', 'POST'])
def index():
    search = MusicSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('index.html', form=search)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
            first_name=form.first_name.data, 
            last_name=form.last_name.data, 
            email=form.email.data, 
            password=hashed_pw
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        print(user)
        print(form.remember.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('account'))
    return render_template('login.html', title='Login',form=form)

@app.route('/account', methods=['GET','POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data =current_user.first_name
        form.last_name.data =current_user.last_name
        form.email.data =current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/results')
def search_results(search):
    Lambda = int(Album.query.all()[len(Album.query.all())-1].artist_id)
    zeta = 0
    results = []
    if search.data['search'] == '':
        qry = Album.query
        results = qry.all()
    else:
        if search.data['select'] == 'Artist':
            if len(Artist.query.filter_by(name = search.data['search']).all()) > 0:
                for j in range(10):
                    for i in range(zeta+1,Lambda + 1):
                        if str(Artist.query.get(i)) == str(Artist.query.filter_by(name = search.data['search']).all()[0]):
                            zeta = i
                            qry = Album.query.filter_by(artist_id = zeta)
                            results = results + qry.all()
                            break
        elif search.data['select'] == 'Album':
            qry = Album.query.filter_by(title = search.data['search'])
            results = qry.all()
        else:
            qry = Album.query.filter_by(publisher = search.data['search'])
            results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)

@app.route('/new_album', methods=['GET', 'POST'])
def new_album():
    form = AlbumForm(request.form)
    if request.method == 'POST' and form.validate():
        # save the album
        album = Album()
        save_changes(album, form, new=True)
        flash('Album created successfully!')
        return redirect('/')
    return render_template('new_album.html', form=form)

def save_changes(album, form, new=False):
    artist = Artist()
    artist.name = form.artist.data
    album.artist = artist
    album.title = form.title.data
    album.release_date = form.release_date.data
    album.publisher = form.publisher.data
    album.media_type = form.media_type.data
    if new:
        print(artist)
        db.session.add(album)
    db.session.commit()

@app.route('/item/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db.session.query(Album).filter(Album.id==id)
    album = qry.first()
    if album:
        form = AlbumEditForm(formdata=request.form, obj=album)
        if request.method == 'POST' and form.validate():
            if request.form.get('action') == 'Update':
                save_changes(album, form)
                flash('Album updated successfully!')
                return redirect('/')
            elif request.form.get('action') == 'Delete':
                db.session.delete(album)
                db.session.commit()
                flash('Album deleted successfully!')
                return redirect('/')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

# if __name__ == '__main__':
#     import os
#     if 'WINGDB_ACTIVE' in os.environ:
#         app.debug = False
#     app.run(port=5001)