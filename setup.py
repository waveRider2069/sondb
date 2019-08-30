from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()
setup(
    name='sondb',
    packages=find_packages(),
    # packages = find_packages('src'),  # 包含所有src中的包
    # package_dir = {'':'src'},   # 告诉distutils包都在src下
    include_package_data=True,
    # package_data={
    #     # 任何包中含有.txt文件，都包含它
    #     '': ['*.txt'],
    #     # 包含demo包data文件夹中的 *.dat文件
    #     'demo': ['data/*.dat'],
    # },
    version='0.2',
    author="Shaun Gao",
    author_email="shaun.gao@sonova.com",
    description="Sonova (Shanghai) R&D developed projects/subjects database management website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    # url="https://github.com/pypa/sampleproject",
    # packeges=find_packages(),
    # py_modules=['cli'],
    install_requires=[
        'flask', 'mysql-connector-python'
    ],
    # entry_points = {
    #     'console_scripts': [
    #         'foo = demo:test',  #增加foo命令
    #         'bar = demo:test',  #增加bar命令
    #     ],
    #     'gui_scripts': [
    #         'baz = demo:test',
    #     ]
    # }
)
