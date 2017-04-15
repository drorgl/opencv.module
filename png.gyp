{
	'variables':{
		#must be static library, libpng and opencv don't play nice when they are dlls as they are sharing file descriptors
		#which does not work when compiled as shared libraries
		'library' : 'static_library',
		#'library' : 'shared_library',
	},

	'target_defaults': {
		'configurations': {
			'Debug' : {},
			'Release':{},
		},
		
		'msvs_settings': {
			'VCCLCompilerTool':{
				'Optimization':'3',#'MaxSpeed'
				'OmitFramePointers': 'true',
			},
		},
		
		
		'conditions':[
			['target_arch=="x64"', {
				'msvs_configuration_platform': 'x64',
			}],
			
			['OS in "linux android"',{
				'cflags':[
					'-fPIC',
				],
			}],
			
			['OS=="linux" and target_arch=="ia32"',{
				'cflags':[
					'-m32',
				],
				'ldflags':[
					'-m32',
					'-L/usr/lib32',
					'-L/usr/lib32/debug',
				],
			}],
			['OS=="linux" and target_arch=="x64"',{
				'cflags':[
					'-m64'
				],
				'ldflags':[
					'-m64',
				],
			}],
		],
	},
	
	'targets':
	[
		{
			'target_name': 'libpng',
			'type':'<(library)',
			
			'include_dirs':[
				'opencv_src/3rdparty/libpng',
				'<!@(nnbu-dependency --headers zlib)',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'opencv_src/3rdparty/libpng',
				],
			 },
			'dependencies':[
				#'../zlib.module/zlib.gyp:zlib',
				'<!@(nnbu-dependency --dependency zlib)',
			],
			'link_settings':{
					'libraries':[
						'<!@(nnbu-dependency --lib-fix --libs zlib)',
					],
			},
			'sources':[
				'opencv_src/3rdparty/libpng/png.c',
				'opencv_src/3rdparty/libpng/png.h',
				'opencv_src/3rdparty/libpng/pngconf.h',
				'opencv_src/3rdparty/libpng/pngdebug.h',
				'opencv_src/3rdparty/libpng/pngerror.c',
				'opencv_src/3rdparty/libpng/pngget.c',
				'opencv_src/3rdparty/libpng/pnginfo.h',
				'opencv_src/3rdparty/libpng/pnglibconf.h',
				'opencv_src/3rdparty/libpng/pngmem.c',
				'opencv_src/3rdparty/libpng/pngpread.c',
				'opencv_src/3rdparty/libpng/pngpriv.h',
				'opencv_src/3rdparty/libpng/pngread.c',
				'opencv_src/3rdparty/libpng/pngrio.c',
				'opencv_src/3rdparty/libpng/pngrtran.c',
				'opencv_src/3rdparty/libpng/pngrutil.c',
				'opencv_src/3rdparty/libpng/pngset.c',
				'opencv_src/3rdparty/libpng/pngstruct.h',
				'opencv_src/3rdparty/libpng/pngtrans.c',
				'opencv_src/3rdparty/libpng/pngwio.c',
				'opencv_src/3rdparty/libpng/pngwrite.c',
				'opencv_src/3rdparty/libpng/pngwtran.c',
				'opencv_src/3rdparty/libpng/pngwutil.c',		
			],
			'conditions':[
				['target_arch == "arm"',{
					'sources':[
						'opencv_src/3rdparty/libpng/arm/filter_neon.S'
					],
				}],
			]
		},

		
		
	],
	
}