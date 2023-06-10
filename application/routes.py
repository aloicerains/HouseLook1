from application import application, login_manager
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user
import os
import uuid
from controllers import house_add, houses_get, house_get, room_add, house_add_room, authenticate, create_admin
from datetime import datetime
from functools import wraps
from models import User

STATIC_PATH = os.path.join(application.root_path, 'static')
IMAGES_PATH = os.path.join(STATIC_PATH, 'images')

YEAR = datetime.utcnow().year

def check_img_path():
    """checks if images path exists"""
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)


def get_img_url(input_image):
    unique_filename = str(uuid.uuid4())
    filename, extension = os.path.splitext(input_image.filename)
    new_filename = unique_filename + extension
    filepath = os.path.join(IMAGES_PATH, new_filename)
    input_image.save(filepath)
    image_url = url_for('static', filename=f'images/{new_filename}')
    return image_url



#
# def require_authentication(view_func):
#     @wraps(view_func)
#     def wrapper(*args, **kwargs):
#         if session.get('authenticated'):
#             # If the user is authenticated, call the original function
#             return view_func(*args, **kwargs)
#         else:
#             # If the user is not authenticated, redirect to the login page
#             return redirect(url_for('admin_login'))
#     return wrapper


@login_manager.user_loader
def load_user(user_id):
    user = User.objects(id=user_id).first()
    return user


@application.route('/')
def home():
    """Displays the default houses on the page max 10"""
    houses = houses_get()
    active = 'home'
    return render_template('home.html', houses=houses, active=active)


@application.route('/add_house', methods=['GET', 'POST'])
@login_required
def add_house():
    "Get form data"
    if request.method == 'POST':
        house_name = request.form.get('name')
        house_location = request.form.get('location')
        house_image = request.files.get('image')
        check_img_path()

        image_url = get_img_url(house_image)

        result = house_add(house_name, house_location, image_url)
        if result:
            print(f'successfully saved, id {result.id}')

    return render_template('house_upload.html')


@application.route('/house_update/<house_id>', methods=['GET', 'POST'])
@login_required
def house_update(house_id):
    """Updates house details"""
    house = house_get(house_id)
    active='admin'
    if request.method == 'POST':
        house.house_name = request.form.get('name')
        house.house_location = request.form.get('location')
        house_image = request.files.get('image')
        check_img_path()
        house.house_image = get_img_url(house_image)
        house.save()
        return redirect(url_for('home'))
    else:
        return render_template('update_house.html', house=house, active=active)


@application.route('/add_room/<house_id>', methods=['GET', 'POST'])
@login_required
def add_room(house_id=None):
    """Get form data"""
    house = house_get(house_id)
    active='admin'
    if request.method == 'POST':
        room_type = request.form.get('room-type')
        room_price = request.form.get('room-price')
        room_vacancies = request.form.get('room-vacancies')
        room_images = request.files.getlist('room-images')
        img_urls = []
        for img in room_images:
            image_url = get_img_url(img)
            img_urls.append(image_url)

        room = {
            "room_type": room_type,
            "room_price": room_price,
            "room_vacancies": room_vacancies,
            "room_images": img_urls
        }
        new_room = room_add(**room)
        house_add_room(house, new_room)
        # create a response indicating successful update
    return render_template('room_upload.html', house=house, active=active)


@application.route('/room_view/<house_id>', methods=['GET'])
@login_required
def room_view(house_id):
    """Handles the admin room view"""
    active='admin'
    house = house_get(house_id)
    return render_template('admin_room_view.html', house=house, active=active)


@application.route('/delete_room/<house_id>/<room_type>', methods=['GET'])
@login_required
def room_delete(house_id, room_type):
    """Deletes a given room"""
    house = house_get(house_id)
    for room in house.house_rooms:
        if room.room_type == room_type:
            house.house_rooms.remove(room)
            break

    house.save()
    return render_template('admin_room_view.html', house=house)


@application.route('/delete_house/<house_id>', methods=['GET'])
@login_required
def house_delete(house_id):
    """Deletes a single house from database"""
    house = house_get(house_id)
    house.delete()
    return redirect(url_for('home'))


@application.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    houses = houses_get()
    active='admin'
    return render_template('admin_house_view.html', houses=houses, active=active)


@application.route('/view_room/<house_id>', methods=['GET', 'POST'])
def view_room(house_id=None):
    """Views rooms within a given house"""
    house = house_get(house_id)
    rooms = house.house_rooms
    if rooms:
        return render_template('listing-rooms.html', rooms=rooms)
    return render_template('no-room-listing.html')


@application.route('/search', methods=['GET', 'POST'])
def search():
    """Searches a house based on location"""
    if request.method == 'POST':
        location = request.form.get('location')
        houses = houses_get(location)
        if houses:
            return render_template('home.html', houses=houses)
        else:
            return render_template('no-house-listings.html')
    return redirect(url_for('home'))


@application.route('/about', methods=['GET'])
def about():
    """About page"""
    active='about'
    return render_template("about.html", active=active)


@application.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Login"""
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        # check user
        user = authenticate(email, password)
        if user:
            login_user(user)
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password!')
    return render_template('login2.html')

@application.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@application.context_processor
def inject_now():
    """adding variables to the template context"""
    def get_current_year():
        return datetime.now().year
    return {'current_year': get_current_year}

