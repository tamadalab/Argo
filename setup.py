import imp
from importlib_metadata import entry_points
from setuptools import setup

setup(
    name = "argo",
    version="1.0.0",
    py_modules=["argo"],
    install_requires = [
        "Click"
    ],
    entry_points={
        "console_scripts": [
            "argo = argo:main",
        ]
    },
)