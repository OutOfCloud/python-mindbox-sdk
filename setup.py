from setuptools import setup

setup(name='mindbox-sdk',
      version='0.0.1',
      description='Some classes for mindbox API',
      packages=['mindbox_sdk',],
      install_requires=['requests', 'aiohttp'],
      license='MIT',
      author_email='anton.k@outofcloud.ru',
      zip_safe=False)
