import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hass-flair-helper",
    version="0.1.3",
    author="Robert Drinovac",
    author_email="unlisted@gmail.com",
    description="A Python library for home-assistant-flair to help utilize the Flair Python API ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RobertD502/hass-flair-helper',
    keywords='flair, flair vents, flair api, flair home assistant',
    packages=setuptools.find_packages(),
    install_requires=["flair-client==1.0.0"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
    project_urls={  # Optional
    'Bug Reports': 'https://github.com/RobertD502/hass-flair-helper/issues',
    'Source': 'https://github.com/RobertD502/hass-flair-helper/',
    },
)
