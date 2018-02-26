from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user

User1 = User(name="Alexander Leighton", email="aleighton@protonmail.com", picture="Some_url")
session.add(User1)
session.commit()

# Create categories for catalog app
cameras = Category(user_id=1, name="Cameras")
session.add(cameras)
laptops = Category(user_id=1, name="Laptops")
session.add(laptops)
pcs = Category(user_id=1, name="PCs")
session.add(pcs)
phones = Category(user_id=1, name="Mobile Phones")
session.add(phones)
home_appliances = Category(user_id=1, name="Home Appliances")
session.add(home_appliances)
tvs = Category(user_id=1, name="TVs")
session.add(tvs)
storage = Category(user_id=1, name="Digital Storage")
session.add(storage)
cables = Category(user_id=1, name="Cables")
session.add(cables)
session.commit()


# Create camera items for category Cameras
camera1=Item(name="Nikon D7000 dlsr",
             description="20.2mp CMOS sensor, DX frame size",
             price="$889",
             category=cameras,
             user=User1)
camera2=Item(name="Canon D80 24.4mp Full Frame Sensor",
             price="$1250",
             category=cameras,
             user=User1)
session.add(camera1)
session.add(camera2)
session.commit()
