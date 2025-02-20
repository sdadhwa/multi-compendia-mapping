from setuptools import setup, find_packages

setup(
    name='mcomp-mapping',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'pandas',
        'pytest',
        'scanpy',
        'seaborn',
        'umap-learn',
        'scikit-learn',
        'matplotlib',
        'ipython',
        'requests',
    ],
)