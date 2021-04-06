from pathlib import Path
from setuptools import setup, find_packages


setup(
    name="openapi_elm_client",
    version="0.2.0",
    packages=find_packages("src"),
    author="Austin Bingham",
    author_email="austin.bingham@gmail.com",
    description="Elm client generator for OpenAPI specifications",
    license="MIT",
    keywords="",
    url="http://github.com/abingham/openapi-elm-client",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
    ],
    platforms="any",
    include_package_data=True,
    package_dir={"": "src"},
    package_data={"openapi_elm_client": ["templates/*j2"]},
    install_requires=[
        "click",
        "swagger-to",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        "dev": ["black", "bumpversion"],
        # 'doc': ['sphinx', 'cartouche'],
        "test": ["godkjenn>=4,<5", "pytest"],
    },
    entry_points={
        "console_scripts": [
            "openapi-elm-client = openapi_elm_client.cli:main",
        ],
    },
    long_description=Path("README.rst").read_text(encoding="utf-8"),
)
