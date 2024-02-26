from setuptools import setup

APP = ['src/main.py']
DATA_FILES = [('html', ['src/html/index.html'])]
OPTIONS = {
    'iconfile': 'src/icon.icns',
    'plist': {
        'CFBundleName': 'Scanner',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
    },
    'includes': ['wxPython','upnpclient','qrcode', 'pipreqs'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
