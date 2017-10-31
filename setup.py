from setuptools import find_packages, setup

setup(
    name='scrapyc',
    version='0.0.1',
    description="Simple client to scrapyd. Done right.",
    keywords=[],
    url="https://github.com/f213/scrapyd-client/",
    author="Fedor Borshev",
    author_email="f@f213.in",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'requests',
        'Click',
        'colorama',
    ],
    entry_points="""
        [console_scripts]
        scrapyc = scrapyc.cli:main
    """,
    include_package_data=True,
    zip_safe=False,
)
