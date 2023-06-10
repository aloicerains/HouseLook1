from models import Room, House, User
from mongoengine import ValidationError


def house_add(house_name, house_location, house_image):
    """Add house"""
    house = House(
        house_name=house_name,
        house_location=house_location,
        house_image=house_image
    )
    result = house.save()
    return result

def houses_get(location=None):
    """Gets all the saved houses"""
    # Set the page number and the page size
    # this should be updated
    page_number = 1
    page_size = 10

    # Calculate the number of documents to skip
    skip = (page_number - 1) * page_size

    # Retrieve the records for the current page
    if location:
        house_objs = House.objects(house_location=location)
    else:
        house_objs = House.objects()
    houses = house_objs.skip(skip).limit(page_size)
    return houses


def house_get(house_id: str):
    """Retrieves a single house from database"""
    house = House.objects.get(id=house_id)
    return house


def house_add_room(house: House, room: Room):
    """Adds rooms to the house"""
    try:
        house.house_rooms.append(room)
        house.save()
        print("updated successfully!")
    except ValidationError as e:
        print(f"Update failed: {e}")


def room_add(**kwargs):
    """Add room"""
    room = Room(
        room_type=kwargs['room_type'],
        room_price=kwargs['room_price'],
        room_vacancies=kwargs['room_vacancies'],
        room_images=kwargs['room_images']
    )
    return room

def create_admin(username=None, password=None):
    """Add admin"""
    user = User(email='aaaaa', password='aaaa')
    user.set_password('aaaa')
    user.save()



def authenticate(email, password):
    """Authenticates the user"""
    user = User.get_by_email(email=email)
    if user and user.check_password(password):
        return user
    return None

