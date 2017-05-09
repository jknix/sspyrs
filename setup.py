from setuptools import setup

setup(name='datasciencetools',
      version='0.1',
      description='Lightweight interface for SSRS reports to python',
      url='',
      author='James Nix',
      author_email='jnix@garretsongroup.com',
      license='MIT',
      packages=['datasciencetools', 'sspyrs'],
      dependency_links=['https://github.com/requests/requests-ntlm'],
      install_requires=[
          'pandas>=0.18.1',
          'pyodbc>=4.0.15'
      ],
      zip_safe=False)
