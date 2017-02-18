from databases import *


engine = create_engine('sqlite:///welcome_to_you.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

products = [
{'name':'dress','description':'evening dress for plus-sized women','photo':'http://runwayfashion.in/ar/plus-size-clothing-women-curvy-fashion-dresses/'},

{'name':'casual outfit','description': 'you can always be fabulous in the most comfortable clothes','photo'},

{'name':'anorixia','description':'i had a problem because of my weight so '},

{'name':'not fitting','description':'nothing in the store is good for my body'},

{'name':'obesity','description':'hating my body'},

{'name':'losing hope','description':'im done with trying'}

]

for post in posts:
    newPost = Post(name=post['name'], description=post['description'])
    session.add(newPost)
    session.commit()