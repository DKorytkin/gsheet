
import codecs
from setuptools import setup


setup(
    name="GSheet",
    version='0.0.1',
    author='Denis Korytkin',
    author_email='dkorytkin@gmail.com',
    description='Simple library writing data to google sheets Edit',
    keywords='google sheet',
    url='https://github.com/DKorytkin/gsheet',
    py_modules=[
        'gsheet', 'sheet_exceptions', 'config', 'helpers',
        'bl.app_auth', 'bl.drive',
        'bl.sheet.chart', 'bl.sheet.format', 'bl.sheet.value',
    ],
    python_requires='>=3.6',
    install_requires=['trafaret==1.0.0'],
    long_description=codecs.open('README.md', 'r', 'utf-8').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
)
