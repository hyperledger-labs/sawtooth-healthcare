# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from __future__ import print_function

import os
# import subprocess

from setuptools import setup, find_packages  # , Command

conf_dir = "/etc/sawtooth"

data_files = [
    (conf_dir, ['packaging/healthcare.toml'])
]

if os.path.exists("/etc/default"):
    data_files.append(
        ('/etc/default', ['packaging/systemd/sawtooth-healthcare-tp-python']))

if os.path.exists("/lib/systemd/system"):
    data_files.append(('/lib/systemd/system',
                       ['packaging/systemd/sawtooth-healthcare-tp-python.service']))

# class CleanCommand(Command):
#     """Custom clean command to tidy up the project root."""
#     user_options = []
#
#     def initialize_options(self):
#         pass
#
#     def finalize_options(self):
#         pass
#
#     def run(self):
#         os.system('rm -vrf ./build ./dist ./*.egg-info')


setup(
    name='healthcare-processor',
    version='0.1',
    description='Sawtooth HealthCare Processor Example',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-core',
    # packages=find_packages(exclude=['cli', 'rest_api']),
    # packages=find_packages(include=['processor*', 'common*']),
    packages=find_packages(),
    # package_dir={'': 'processor'},
    install_requires=[
        # 'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        # 'sawtooth-signing',
        # 'PyYAML',
    ],
    # cmdclass={
    #     'clean': CleanCommand,
    # },
    data_files=data_files,
    entry_points={
        'console_scripts': [
            # 'xo = sawtooth_xo.xo_cli:main_wrapper',
            'healthcare-tp = processor.workflow.main:main',
        ]
    })
