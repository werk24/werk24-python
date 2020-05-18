from setuptools import setup


setup(
    name="werk24",
    version="0.2.0",
    author="W24 Service GmbH",
    author_email="info@werk24.biz",
    description="Werk24 Client to read PDF- and Image-based Technical Drawings / Engineering Drawings",
    url="https://www.werk24.biz",
    entry_points={
        "console_scripts": [
            "w24cli=werk24.cli.w24cli:main",
        ]
    },
    packages=[
        "werk24",
        "werk24.models",
        "werk24.cli",
        "werk24.cli.w24cli"],
    install_requires=[
        "aioboto3 >= 6.4.1",
        "pydantic >= 1.4",
        "python-dotenv>=0.10.1",
        "websockets >= 8.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Image Recognition"])
