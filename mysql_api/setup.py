from setuptools import setup, find_packages

setup(
    name='mysql_api',
    version='0.0.1',
    install_requires=[
        'uvicorn',
        'fastapi',
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
         "console_scripts": ["startup_api=final_db_start:startup"],
     },
)