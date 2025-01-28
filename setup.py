from setuptools import setup, find_packages

setup(
    name="cpi-cli",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
        'cryptography',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'cpi-cli = cpi_cli.cli:cli'
        ]
    }
)