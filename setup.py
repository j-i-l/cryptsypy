from setuptools import setup

def readme():
    """
        This loads the README.md file.
    """
    with open('README.md') as f:
        return f.read()

setup(name = 'cryptsypy',
      version = '0.1dev',
      description='A package to interact with www.crypsty.com via their API.',
      #long_description='Long blabla',
      long_description=readme(),
      keywords='trader, www.cryptsy.com',
      classifiers=[
                   'Development Status :: Under development',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: www.crypsty.com',
                   ],
      data_files = [("", ["LICENSE.txt"])],
      include_package_data=True,
      url='git...',
      author='j-i-l',
      author_email='simply.mail.to.j.i.l@gmail.com',
      license='MIT',
      packages=['cryptsypy'],
      install_requires = ['apipy'],
      dependency_links=[
                        'https://github.com/j-i-l/apipy/archive/master.zip#egg=apipy-0.1',
                       ],	
      test_suite='nose.collector',
      tests_require=['nose'],
      #entry_points={
      #              'console_scripts': [
      #                                   'apipy_public_request=apipy.public_request:main'
      #                                 ],
      #              },
      zip_safe=False)


