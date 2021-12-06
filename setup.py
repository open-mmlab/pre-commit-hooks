from setuptools import find_packages, setup  # type: ignore


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


version_file = 'mmprecommit/version.py'


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


setup(
    name='mmprecommit',
    version=get_version(),
    description='A pre-commit hook',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/open-mmlab/mmprecommit',
    author='MMPrecommit Authors',
    author_email='openmmlab@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    scripts=['mmprecommit/say_hello.py'],
)
