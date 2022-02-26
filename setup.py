import os
import sys
import subprocess

from setuptools import find_packages, setup
from setuptools.command.install import install
# TODO: This is a bit buggy since it requires torch before installing torch.
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

WORKDIR = os.path.dirname(os.path.abspath(__file__))

def get_git_commit_number():
    if not os.path.exists('.git'):
        return '0000000'

    cmd_out = subprocess.run(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE)
    git_commit_number = cmd_out.stdout.decode('utf-8')[:7]
    return git_commit_number


def make_cuda_ext(name, module, sources,include_dirs=[],extra_compile_args={}):
    cuda_ext = CUDAExtension(
        name='%s.%s' % (module, name),
        sources=[os.path.join(*module.split('.'), src) for src in sources],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args
    )
    return cuda_ext


def write_version_to_file(version, target_file):
    with open(target_file, 'w') as f:
        print('__version__ = "%s"' % version, file=f)


class PostInstallation(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        # Note: buggy for kornia==0.5.3 and it will be fixed in the next version.
        # Set kornia to 0.5.2 temporarily
        subprocess.call([sys.executable, '-m', 'pip', 'install', 'kornia==0.5.2', '--no-dependencies'])


if __name__ == '__main__':
    version = '0.0.1+%s' % get_git_commit_number()
    # write_version_to_file(version, 'trident/version.py')

    setup(
        name='trident',
        version=version,
        description='Trident is a framework for fast cpp/python/cuda development, test and deploy!',
        install_requires=[
            'numpy',
            'torch'
        ],
        author='Charles Wittman',
        author_email='qzh19950601@gmail.com',
        license='Apache License 2.0',
        packages=find_packages(),
        cmdclass={
            'build_ext': BuildExtension,
            'install': PostInstallation,
        },
        ext_modules=[
            make_cuda_ext(
                name='examplelib',
                module='trident.example',
                sources=[
                    'core/example_torch.cpp',
                    'core/example_numpy.cpp',
                ]
            ),
        ],
    )
    os.system('rm -rf %s/build'%WORKDIR)
    
