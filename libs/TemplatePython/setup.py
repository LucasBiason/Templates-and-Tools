from setuptools import setup

setup(
    name='<<project>>',
    version='1.0.0',
    descriptions='Python library for <<desc here>>',
    author='<<name here>>',
    packages=[
        '<<project>>', 
        # more pachakes that need to be included...
    ],
    install_requires=[
        'requests==2.21.0',
       # requirements here
    ],
    include_package_data=True,
    zip_safe=False
)
