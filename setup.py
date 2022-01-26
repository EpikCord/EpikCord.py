from distutils.core import setup
setup(
  name = 'EpikCord.py', 
  packages = ['EpikCord'], 
  version = '0.4.3',      
  license='MIT',        
  description = 'Have you ever wanted to make a Discord Bot? Are you upset that Discord.py has been discontinued? We introduce EpikCord.py, a Discord.py replacement.',
  long_description = "I present to you, EpikCord.py, this is a python package which will hopefully be a great replacement for Discord.py as the creator has decided to discontinue the package. Whilst there are forks of the discord.py repo, we have started this library from scratch. We hope you enjoy using it!",
  author = 'EpikHost',                   
  author_email = 'support@epikhost.xyz',      
  url = 'https://github.com/EpikHost/EpikCord.py',   
  #download_url = 'https://github.com/EpikHost/EpikCord.py/archive/v_01.tar.gz',
  keywords = ['EpikCord.py', 'Discord', 'API', "Bot", "EpikCord"],   
  install_requires=[
          'aiohttp',
          "websocket-client"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3.8',
  ],
)