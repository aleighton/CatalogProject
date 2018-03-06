from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, Category, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user

User1 = User(name="Alexander Leighton",
             email="aleighton@gmail.com",
             picture="Some_url")
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
monitors = Category(user_id=1, name="Monitors")
session.add(monitors)
session.commit()


# Create camera items for category Cameras
camera1 = Item(name="Nikon D7000 dlsr",
               description="20.2mp CMOS sensor, DX frame size",
               price="$889",
               category=cameras,
               user=User1)
camera2 = Item(name="Canon D80 24.4mp Full Frame Sensor",
               price="$1250",
               category=cameras,
               user=User1)
camera3 = Item(name="Nikon D7000 dlsr",
               description="20.2mp CMOS sensor, DX frame size",
               price="$889",
               category=cameras,
               user=User1)
camera4 = Item(name="Canon D80 24.4mp Full Frame Sensor",
               price="$1250",
               category=cameras,
               user=User1)
camera5 = Item(name="Nikon D7000 dlsr",
               description="20.2mp CMOS sensor, DX frame size",
               price="$889",
               category=cameras,
               user=User1)
camera6 = Item(name="Canon D80 24.4mp Full Frame Sensor",
               price="$1250",
               category=cameras,
               user=User1)
session.add(camera1)
session.add(camera2)
session.add(camera3)
session.add(camera4)
session.add(camera5)
session.add(camera6)
session.commit()

# Create Laptop items for category Laptops
laptop1 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
laptop2 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
laptop3 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
laptop4 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
laptop5 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
laptop6 = Item(name="Asus Zenbook",
               description="For business, 8Gb of Ram, Core i7, 256GB SSD",
               price="$1250",
               category=laptops,
               user=User1)
session.add(laptop1)
session.add(laptop2)
session.add(laptop3)
session.add(laptop4)
session.add(laptop5)
session.add(laptop6)
session.commit()

# Create PC items for category PCs
pc1 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
pc2 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
pc3 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
pc4 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
pc5 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
pc6 = Item(name="Dell Workstation Pro",
           description="For Powerusers, video work and rendering",
           price="$3000",
           category=pcs,
           user=User1)
session.add(pc1)
session.add(pc2)
session.add(pc3)
session.add(pc4)
session.add(pc5)
session.add(pc6)
session.commit()

# Create Mobile Phone items for category Mobile Phones
mobile1 = Item(name="Apple Iphone X",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
mobile2 = Item(name="Asus Zenphone",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
mobile3 = Item(name="Huawei P10",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
mobile4 = Item(name="Samsung S8",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
mobile5 = Item(name="Apple Iphone 8 Plus",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
mobile6 = Item(name="Fairphone 2",
               description="A masterpiece of design",
               price="$1000",
               category=phones,
               user=User1)
session.add(mobile1)
session.add(mobile2)
session.add(mobile3)
session.add(mobile4)
session.add(mobile5)
session.add(mobile6)
session.commit()

# Create Monitor items for category Monitors
monitor1 = Item(name="AOC Gaming, 144mhz, Freesync",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)
monitor1 = Item(name="BenQ ultrawide 29inch 1080p",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)
monitor1 = Item(name="Asus 27inch, 4K, 2ms response",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)
monitor1 = Item(name="HP Infinity display",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)
monitor1 = Item(name="Dell Inspiron 24inch HD resolution",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)
monitor1 = Item(name="Apple Mac 27inch 4K",
                description="A masterpiece of design",
                price="$1000",
                category=phones,
                user=User1)

session.add(monitor1)
session.add(monitor2)
session.add(monitor3)
session.add(monitor4)
session.add(monitor5)
session.add(monitor6)
session.commit()

print ("Database created for Catalog App!")
