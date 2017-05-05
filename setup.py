from distutils.core import setup
setup(
  name = 'tabtree',
  packages = ['tabtree'], # this must be the same as the name above
  version = '0.2.0',
  description = 'Parsing tabbed tree formatted text files into dict node trees',
  license='MIT License',
  author = 'Fran Oviamionayi',
  author_email = 'fran.ovia@gmail.com',
  url = 'https://github.com/fran-ovia/tabtree-py',
  download_url = 'https://github.com/fran-ovia/tabtree-py/releases/download/0.2.0/tabtree-0.2.0.zip',
  keywords = ['tabbed-tree', 'parsing', 'tab', 'tree'],
  classifiers = [
    'Programming Language :: Python',
    'Development Status :: 4 - Beta',
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],
)
