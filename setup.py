from distutils.core import setup

setup(
    name='algolib',
    version='0.4',
    packages=['algolib', 'algolib.descriptors'],
    url='https://github.com/InstaSketch/algolib',
    license='',
    author='Bryan Kok, Dylan Wang',
    author_email='',
    description='The algorithm behind InstaSketch',
    install_requires=[
        'numpy',
        'scipy'
    ]
)
