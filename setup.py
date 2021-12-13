from setuptools import find_packages, setup  # type: ignore


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name='mmprecommit',
    version='0.1.0',
    description='A pre-commit hook',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/open-mmlab/mmprecommit',
    author='MMPrecommit Authors',
    author_email='openmmlab@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['PyYAML'],
    scripts=['mmprecommit/say_hello.py', 'mmprecommit/check_algo_readme.py'],
)
