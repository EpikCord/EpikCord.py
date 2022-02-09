from distutils.core import setup
from EpikCord.__main__ import __version__
packagePartsReq = {
  "voice": ["PyNaCl"] #one part is enough for now
}

#Read The Readme
with open("README.md") as f:
    long_description = f.read()

#read version
ver = __version__()
setup(
  name = 'EpikCord.py', 
  packages = ['EpikCord'], 
  version = ver,      
  license='MIT',        
  description = 'A Modern API wrapper for Discord, Intended for replacement of the now discontinued Discord.py library',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'EpikHost',                   
  author_email = 'support@epikhost.xyz',      
  url = 'https://github.com/EpikHost/EpikCord.py',   
  #download_url = 'https://github.com/EpikHost/EpikCord.py/archive/v_01.tar.gz',
  keywords = ['EpikCord.py', 'Discord', 'API', "Bot", "EpikCord"],   
  install_requires=[
          'aiohttp',
          "websocket-client"
      ],
  extras_require=packagePartsReq,
  python_requires='>=3.8',    

  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',   
    'Natural Language :: English',
    'Operating System :: OS Independent' ,  
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
  include_package_data=True
)