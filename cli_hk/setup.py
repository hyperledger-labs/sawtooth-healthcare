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

# import os
# import subprocess

from setuptools import setup, find_packages

conf_dir = "/etc/sawtooth"

# data_files = [
#     (conf_dir, ['packaging/healthcare.toml'])
# ]
#
# if os.path.exists("/etc/default"):
#     data_files.append(
#         ('/etc/default', ['packaging/systemd/sawtooth-healthcare-client-python']))
#
# if os.path.exists("/lib/systemd/system"):
#     data_files.append(('/lib/systemd/system',
#                        ['packaging/systemd/sawtooth-healthcare-client-python.service']))

setup(
    name='healthcare-client-hk',
    version='0.1',
    description='Sawtooth HealthCare Client Example',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-core',
    packages=find_packages(),
    # packages=find_packages(include=['cli_hk*', 'common*']),
    install_requires=[
        # 'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'requests',
        'sawtooth-signing',
        'PyYAML',
        'sawtooth-cli',
    ],
    # data_files=data_files,
    entry_points={
        'console_scripts': [
            'cli-hk = cli.workflow.dehr_hk_cli:main_wrapper',
            # 'healthcare-tp-python = processor.workflow.main:main',
        ]
})