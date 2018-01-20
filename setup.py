from setuptools import setup

setup(name='studiouhr',
        version='0.1',
        description='A pyglet based fullscreen studio clock',
        url='https://github.com/atoav/studiouhr',
        author='David Huss',
        author_email='dh@atoav.com',
        license='MIT',
        packages=['studiouhr'],
        install_requires=['pyglet', 'astral', 'colorsys'],
        package_data = {'':['fonts/*.ttf']},
        zip_safe=False
        )
