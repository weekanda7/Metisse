from setuptools import setup, find_packages

setup(
    name='metis',
    version='2.12.2',
    description='UI Test Automation Framework for Games and Apps on Android/iOS',
    author='Henry Chen',
    author_email='weekand7@gmail.com',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here, e.g. 'numpy>=1.18.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
)