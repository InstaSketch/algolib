from distutils.core import setup

setup(name='fmiqlib',
	version='1.0',
	py_modules=[splitext(basename(i))[0] for i in glob.glob("fmiqlib/*.py")])
