# -*- mode: python -*-

block_cipher = None

a = Analysis(['SpecPySplash.py'],
             pathex=['/home/juan/Desktop/GUI\ Development'],
             binaries=None,
             datas=[( '/home/juan/anaconda3/lib/libmkl_avx.so', '.' )],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
#	  exclude_binaries=True,
          name='SpecPy',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='Icon.ico')
