from setuptools import setup, find_packages

setup(
    name='json_processor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'dev': [
            'pytest'
        ],
    },
    entry_points={
        'console_scripts': [
            'json_processor=json_processor.processor:main',
        ],
    },
)