from setuptools import setup

setup(name='studiouhr',
        version='0.2',
        description='A pyglet based fullscreen studio clock',
        url='https://github.com/atoav/studiouhr',
        author='David Huss',
        author_email='dh@atoav.com',
        license='MIT',
        packages=['studiouhr'],
        install_requires=['pyglet', 'astral'],
        package_data = {'':['fonts/*.ttf']},
        entry_points={'console_scripts':['studiouhr=studiouhr:main']},
        zip_safe=False
        )
