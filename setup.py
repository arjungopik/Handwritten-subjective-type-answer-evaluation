from setuptools import setup

setup(
    name='word-detector',
    version='1.0.0',
    description='Subjective answer evaluation',
    author='Arjun Gopi K',
    packages=['word_detector'],
    url="https://github.com/arjungopik/handwritten-text-detection-and-recognition",
    install_requires=['numpy', 'sklearn', 'opencv-python'],
    python_requires='>=3.7'
)
