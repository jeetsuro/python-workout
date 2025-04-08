from setuptools import setup, find_packages

## STEPS to follow :
## --------------------------------------------------------------------------
# pip install -e .	                #Install package locally (editable mode)
# python -m setuptool_test.app	    #Run the package as a module
# python setup.py sdist bdist_wheel	#Create package distribution
# twine upload dist/*	            #Upload to PyPI

setup(
    name="setuptool_test",           # Package Name
    version="0.1.0",                 # Version
    packages=find_packages(),        # Automatically find packages
    install_requires=[],             # Add dependencies if needed
    entry_points={                   # Allows running `setuptool_test` as a CLI
        "console_scripts": [
            "setuptool-test=setuptool_test.app:main"
        ]
    },
)



    
                   
    
    
    

