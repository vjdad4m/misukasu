import os
from setuptools import setup

cur_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cur_dir, 'README.md'), 'r') as f: long_desc = f.read()

setup(name='misukasu',
      version='0.0.0',
      description='Radar-based pose estimation with additional features',
      author='Adam Vajda',
      license='MIT',
      long_description=long_desc,
      packages=['misukasu'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      install_requires=['numpy', 'opencv-python'],
      python_requires='>=3.8',
      include_package_data=True)

os.makedirs('out/', exist_ok = True)
os.makedirs('out/camera/', exist_ok = True)
os.makedirs('out/radar/', exist_ok = True)
