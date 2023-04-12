from setuptools import setup, find_packages

setup(
    name='metis',
    version="0.1.0",
    description="A versatile and automated testing framework for games and apps on Android and iOS platforms",
    author='Henry Chen',
    author_email='weekand7@gmail.com',
    packages=find_packages(),
    install_requires=[
        'facebook_wda>=1.4.6',
        'natsort>=8.2.0',
        'numpy<=1.19.5',
        'opencv_python>=4.7.0.68',
        'Pillow>=9.4.0',
        'protobuf>=4.22.1',
        'PyQt6>=6.4.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)