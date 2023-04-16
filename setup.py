from setuptools import setup, find_packages

setup(
    name='metis',
    version="0.1.7",
    description="A versatile and automated testing framework for games and apps on Android and iOS platforms",
    author='Henry Chen',
    author_email='weekand7@gmail.com',
    license = 'Apache License 2.0',
    packages=find_packages(exclude=['unit_tests', 'unit_tests.*']),
    package_data={
        'metis': ['example/example_data/**/*'],
    },
    install_requires=[
        'facebook_wda>=1.3.3',
        'numpy>=1.17.3',
        'opencv_python>=4.5.1.48',
        'Pillow>=3.4.0',
        'PyQt6>=6.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)