# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['deep_space_trader\\__main__.py'],
             pathex=['deep_space_trader'],
             binaries=[],
             datas=[('C:\\Python37\\Lib\\site-packages\\PyQt5\\Qt\\bin', 'PyQt5\\Qt\\bin'), ('deep_space_trader\\images', 'images')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Deep Space Trader',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Deep Space Trader')
