from setuptools import find_packages, setup  # type: ignore


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name='pre_commit_hooks',
    version='0.1.0',
    description='A pre-commit hook for OpenMMLab projects',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/open-mmlab/pre-commit-hooks',
    author='OpenMMLab Authors',
    author_email='openmmlab@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['PyYAML'],
    scripts=[
        'pre_commit_hooks/say_hello.py',
        'pre_commit_hooks/check_algo_readme.py',
    ],
)
