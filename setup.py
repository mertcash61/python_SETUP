from setuptools import setup, find_packages

setup(
    name='my_package',  # Paketinizin adı
    version='0.1.0',  # Paketinizin sürümü
    author='John Doe',  # Yazar adı
    author_email='john.doe@example.com',  # Yazar e-posta adresi
    description='A sample Python package for demonstration purposes.',  # Paket açıklaması
    long_description=open('README.md').read(),  # Uzun açıklama (README dosyasından)
    long_description_content_type='text/markdown',  # Uzun açıklama içeriği tipi
    packages=find_packages(),  # Paketleri bul
    install_requires=[  # Gerekli bağımlılıklar
        'numpy',      # Örnek bağımlılık
        'pandas',     # Örnek bağımlılık
        'requests',   # HTTP istekleri için bağımlılık
        'matplotlib',  # Veri görselleştirme için bağımlılık
        'scikit-learn' # Makine öğrenimi için bağımlılık
    ],
    classifiers=[  # Paket sınıflandırmaları
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',  # Geliştiriciler için
        'Topic :: Scientific/Engineering :: Visualization',  # Görselleştirme
        'Topic :: Scientific/Engineering :: Data Analysis',  # Veri analizi
    ],
    python_requires='>=3.7',  # Gerekli Python sürümü
)
