from setuptools import setup

setup(
    name = 'DAb Endpoint',
    version='1.0',
    license='GNU General Public License v3',
    author='Simone Corti',
    author_email='pisewip@gmail.com',
    description='Vending machine application with Flask',
    packages=['app'],
    platforms='any',
    install_requires=[
        'Flask',
        'pyserial',
        'sqlalchemy',
        'Flask-Session',
        'Flask-Migrate',
        'Flask-Login',
        'Flask-WTF',
        'requests',
        'pymodbus',
        'pyscard'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
