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
			
			['OS in "linux android" and library == "shared_library"',{
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
			'target_name': 'libjpeg',
			'type':'<(library)',
			
			'include_dirs':[
				'opencv_src/3rdparty/libjpeg',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'opencv_src/3rdparty/libjpeg',
				],
			 },
			
			'sources':[
				'opencv_src/3rdparty/libjpeg/change.log',
				'opencv_src/3rdparty/libjpeg/jaricom.c',
				'opencv_src/3rdparty/libjpeg/jcapimin.c',
				'opencv_src/3rdparty/libjpeg/jcapistd.c',
				'opencv_src/3rdparty/libjpeg/jcarith.c',
				'opencv_src/3rdparty/libjpeg/jccoefct.c',
				'opencv_src/3rdparty/libjpeg/jccolor.c',
				'opencv_src/3rdparty/libjpeg/jcdctmgr.c',
				'opencv_src/3rdparty/libjpeg/jchuff.c',
				'opencv_src/3rdparty/libjpeg/jcinit.c',
				'opencv_src/3rdparty/libjpeg/jcmainct.c',
				'opencv_src/3rdparty/libjpeg/jcmarker.c',
				'opencv_src/3rdparty/libjpeg/jcmaster.c',
				'opencv_src/3rdparty/libjpeg/jcomapi.c',
				'opencv_src/3rdparty/libjpeg/jconfig.h',
				'opencv_src/3rdparty/libjpeg/jcparam.c',
				'opencv_src/3rdparty/libjpeg/jcprepct.c',
				'opencv_src/3rdparty/libjpeg/jcsample.c',
				'opencv_src/3rdparty/libjpeg/jctrans.c',
				'opencv_src/3rdparty/libjpeg/jdapimin.c',
				'opencv_src/3rdparty/libjpeg/jdapistd.c',
				'opencv_src/3rdparty/libjpeg/jdarith.c',
				'opencv_src/3rdparty/libjpeg/jdatadst.c',
				'opencv_src/3rdparty/libjpeg/jdatasrc.c',
				'opencv_src/3rdparty/libjpeg/jdcoefct.c',
				'opencv_src/3rdparty/libjpeg/jdcolor.c',
				'opencv_src/3rdparty/libjpeg/jdct.h',
				'opencv_src/3rdparty/libjpeg/jddctmgr.c',
				'opencv_src/3rdparty/libjpeg/jdhuff.c',
				'opencv_src/3rdparty/libjpeg/jdinput.c',
				'opencv_src/3rdparty/libjpeg/jdmainct.c',
				'opencv_src/3rdparty/libjpeg/jdmarker.c',
				'opencv_src/3rdparty/libjpeg/jdmaster.c',
				'opencv_src/3rdparty/libjpeg/jdmerge.c',
				'opencv_src/3rdparty/libjpeg/jdpostct.c',
				'opencv_src/3rdparty/libjpeg/jdsample.c',
				'opencv_src/3rdparty/libjpeg/jdtrans.c',
				'opencv_src/3rdparty/libjpeg/jerror.c',
				'opencv_src/3rdparty/libjpeg/jerror.h',
				'opencv_src/3rdparty/libjpeg/jfdctflt.c',
				'opencv_src/3rdparty/libjpeg/jfdctfst.c',
				'opencv_src/3rdparty/libjpeg/jfdctint.c',
				'opencv_src/3rdparty/libjpeg/jidctflt.c',
				'opencv_src/3rdparty/libjpeg/jidctfst.c',
				'opencv_src/3rdparty/libjpeg/jidctint.c',
				'opencv_src/3rdparty/libjpeg/jinclude.h',
				'opencv_src/3rdparty/libjpeg/jmemansi.c',
				'opencv_src/3rdparty/libjpeg/jmemmgr.c',
				'opencv_src/3rdparty/libjpeg/jmemnobs.c',
				'opencv_src/3rdparty/libjpeg/jmemsys.h',
				'opencv_src/3rdparty/libjpeg/jmorecfg.h',
				'opencv_src/3rdparty/libjpeg/jpegint.h',
				'opencv_src/3rdparty/libjpeg/jpeglib.h',
				'opencv_src/3rdparty/libjpeg/jquant1.c',
				'opencv_src/3rdparty/libjpeg/jquant2.c',
				'opencv_src/3rdparty/libjpeg/jutils.c',
				'opencv_src/3rdparty/libjpeg/jversion.h',
				'opencv_src/3rdparty/libjpeg/README'
				
			],
			'conditions':[
				['OS=="ANDROID" or OS=="IOS"',{
					'sources!':[
						'opencv_src/3rdparty/libjpeg/jmemansi.c'
					]
				},{
					'sources!':[
						'opencv_src/3rdparty/libjpeg/jmemnobs.c'
					]
				}],
				['OS=="winrt"', {
					'defines':[
						'NO_GETENV'
					]
				}]
			]
		},

		
		
	],
	
}