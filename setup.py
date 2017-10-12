from setuptools import setup

setup(name='sspyrs',
      version='0.2',
      description='Lightweight interface for SSRS reports to python',
      long_description=open('README.rst').read(),
      url='https://pypi.python.org/pypi/sspyrs',
      author='James Nix',
      author_email='james@nixanalytics.com',
      license='MIT',
      packages=['sspyrs'],
      install_requires=[
           'pandas>=0.18.1',
           'openpyxl>=2.4.7',
           'xmltodict>=0.10.2',
           'requests_ntlm>=1.0.0'
      ],
      keywords=['ssrs report reporting sql'],
      zip_safe=False)
