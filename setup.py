"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(

    name='JolieMousse',  # Required

  
    version='1.0.0',  # Required

   
    description='A tool to prepare beer brewing sessions',  # Required


    long_description=long_description,  # Optional

 
    long_description_content_type='text/markdown',  # Optional (see note above)


    author='José Fournier',  # Optional

    author_email='jaaf64@zoraldia.com',  # Optional

    classifiers=[  # Optional

        'Development Status :: 3 - Alpha',
        
        'Intended Audience :: Developers',
      
        'License :: GNU GPLv3',

        'Programming Language :: Python :: 3.6',
    ],


    keywords='beer brewing homebrewing',  # Optional


    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn'],  # Optional

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={  # Optional
        'dev': ['check-manifest'],
   
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #


    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'main=JolieMousse:main',
        ],
    },


    
)
