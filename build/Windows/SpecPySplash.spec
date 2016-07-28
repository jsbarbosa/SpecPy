# -*- mode: python -*-

block_cipher = None


a = Analysis(['SpecPySplash.py'],
             pathex=['C:\\Users\\lenovo\\Desktop'],
             binaries=None,
             datas=[('C:\\Users\\lenovo\\Anaconda3\\Library\\bin\\mkl_avx.dll', '.' )],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('SpecPy.png', 'C:\\Users\\lenovo\\Desktop\\SpecPy.png', 'DATA' )]


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SpecPySplash',
          debug=False,
          strip=False,
          upx=True,
          console=False, icon='Icon.ico')
