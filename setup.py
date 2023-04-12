from setuptools import setup, find_packages

setup(
    name='metis',
    version="0.1.6",
    description="A versatile and automated testing framework for games and apps on Android and iOS platforms",
    author='Henry Chen',
    author_email='weekand7@gmail.com',
    license = 'Apache License 2.0',
    packages=find_packages(exclude=['unit_tests', 'unit_tests.*']),
    package_data={
        'metis': ['example/**/*.png'],
    },
    install_requires=[
        'facebook_wda>=1.4.6',
        'natsort>=8.2.0',
        'numpy>=1.19.5',
        'opencv_python>=4.5.1.48',
        'Pillow>=8.0.0.dev0',
        'protobuf>= 4.21.4',
        'PyQt6>=6.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)