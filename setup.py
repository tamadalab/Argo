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
            "argo = argo:cli",
        ]
    },
)