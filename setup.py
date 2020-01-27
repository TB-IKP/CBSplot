from setuptools import setup

setup(
        name='CBSplot',
        version='0.1.0',
        description='Plot routine for cbsmodel',
        url='http://github.com/TB-IKP/CBSplot',
        author='Tobias Beck',
        author_email='tbeck@ikp.tu-darmstadt.de',
        #license=None,
        python_requires='>=3',
        packages=['CBSplot'],
        install_requires=['numpy','matplotlib','uncertainties'],
)
