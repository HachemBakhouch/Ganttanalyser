from setuptools import setup, find_packages

setup(
    name="analyseur-charge-travail",
    version="0.1.0",
    description="Application pour analyser la charge de travail",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "openpyxl==3.1.2",
        "reportlab==4.0.8",
        "pandas==2.2.1",
        "numpy>=1.22.0",
    ],
    entry_points={
        "console_scripts": [
            "analyseur-charge=src.main:main",
        ],
    },
    python_requires=">=3.8",
)
