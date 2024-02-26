# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/Scanner.py'],
    pathex=[],
    binaries=[],
    datas=[('src/html/index.html', 'html')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Scanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['src/icon.icns'],
    manifest='akespec',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Scanner',
)
app = BUNDLE(
    coll,
    name='Scanner.app',
    icon='src/icon.icns',
    bundle_identifier=None,
)
