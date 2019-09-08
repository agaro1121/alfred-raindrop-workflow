from setuptools import find_packages, setup
# from package import Package

setup(
    name='raindrop',
    version='0.0.1',
    description='Raindrop.io alfred workflow',
    long_description=open('README.md').read(),
    author="Anthony Garo",
    author_email="agaro1121@gmail.com",
    packages=["raindrop", "raindrop/workflow", "lib"],
    include_package_data=True,
    install_requires=[
        "requests",
        "Alfred-Workflow"
    ]
)