from distutils.core import setup
packagePartsReq = {
  "voice": ["PyNaCl"] #one part is enough for now
}

#Read The Readme
with open("README.md") as f:
    long_description = f.read()
setup(
  name = 'EpikCord.py', 
  packages = ['EpikCord'], 
  version = '0.4.3',      
  license='MIT',        
  description = 'A Modern API wrapper for Discord, Intended for replacement of the now deprecated Discord.py library',
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
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.8',
  ],
)