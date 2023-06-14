from setuptools import setup, find_packages

# Ler as dependências do arquivo requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='PID_controller',
    version='1.0.0',
    author='Matheus Cascalho',
    author_email='cascalhom@gmail.com',
    description='Controlador PID com simulação de sistemas dinâmicos',
    packages=find_packages(),
    install_requires=requirements,
)
