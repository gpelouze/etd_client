import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()
with open('requirements.txt', 'r') as f:
    requirements = f.read().strip('\n').split('\n')

setuptools.setup(
    name='etd_client',
    version='2018.12.11',
    author='Gabriel Pelouze',
    author_email='gabriel@pelouze.net',
    description='Unofficial client for to the Exoplanet Transit Database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ArcturusB/etd_client',
    packages=setuptools.find_packages(),
    python_requires='>=3.5',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
)
