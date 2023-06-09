from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='metisse',
    version="0.0.6",
    description="A versatile and automated testing framework for games and apps on Android and iOS platforms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Henry Chen',
    author_email='weekand7@gmail.com',
    license='Apache License 2.0',
    keywords=['automation', 'automated-test', 'game', 'android', 'ios'],
    packages=find_packages(exclude=['unit_tests', 'unit_tests.*']),
    package_data={
        'metisse': ['example/example_data/**/*'],
    },
    install_requires=[
        'facebook_wda>=1.3.3',
        'numpy>=1.17.3',
        'opencv_python>=4.5.1.48',
        'Pillow>=3.4.0',
        'PyQt6>=6.0.0',
        'dill>=0.3.1.1',
        'tidevice>=0.9.12',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
