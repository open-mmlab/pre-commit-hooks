from setuptools import find_packages, setup  # type: ignore


def readme():
    with open('./README.md', encoding='utf-8') as f:
        content = f.read()
    return content


setup(
    name='pre_commit_hooks',
    version='0.2.0',
    description='A pre-commit hook for OpenMMLab projects',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/open-mmlab/pre-commit-hooks',
    author='OpenMMLab Authors',
    author_email='openmmlab@gmail.com',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'say-hello=pre_commit_hooks.say_hello:main',
            'check-algo-readme=pre_commit_hooks.check_algo_readme:main',
            'check-copyright=pre_commit_hooks.check_copyright:main',
            'check-ecosystem-validity=pre_commit_hooks.check_ecosystem_validity:main'  # noqa: E501
        ],
    },
)
