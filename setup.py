import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unattached-volumes",
    version="0.0.1",
    author="Pedro Garcia Rodriguez",
    author_email="me@pgarcia.dev",
    description="Simple utility script for managing unattached "
    "EBS volumes on AWS using Python and boto3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/breakingpitt/unattached_volumes",
    project_urls={
        "Releases": "https://github.com/breakingpitt/unattached_volumes/releases"  # noqa: E501
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["unattached-volumes"],
    python_requires=">=3.12",
    install_requires=[
        "boto3==1.34.50",
    ],
    test_requires=[
        "pytest==8.0.2",
    ],
    extras_requires=[
        "pytest==8.0.2",
    ],
    entry_points={
        "console_scripts": [
            "unattached-volumes=unattached-volumes.unattached-volumes:main"
        ],
    },
)
