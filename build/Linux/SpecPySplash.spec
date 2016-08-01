# -*- mode: python -*-

block_cipher = None

#added_files = [( '/home/juan/Documents/SpecPy/SpecPy.png', '.' )]
a = Analysis(['SpecPySplash.py'],
             pathex=['/home/juan/Documents/SpecPy/Gui\ Development'],
             binaries=None,
             datas=[( '/home/juan/anaconda3/lib/libmkl_avx.so', '.' )],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
#a.datas += [('SpecPy.png', '/home/juan/Documents/SpecPy/SpecPy.png', 'DATA' )]
a.datas += [('mainwindow.ui', '/home/juan/Documents/SpecPy/SpecPy/mainwindow.ui', 'DATA' )]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
#          a.binaries,
#          a.zipfiles,#
#          a.datas,#
	  exclude_binaries=True,
          name='SpecPy',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SpecPy')