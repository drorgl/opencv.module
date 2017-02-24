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
			'target_name': 'libjasper',
			'type':'<(library)',
			
			'include_dirs':[
				'opencv_src/3rdparty/libjasper',
			],
			'direct_dependent_settings': {
				'include_dirs': [
					'opencv_src/3rdparty/libjasper',
				],
			 },
			
			'defines':[
				'EXCLUDE_MIF_SUPPORT',
				'EXCLUDE_PNM_SUPPORT',
				'EXCLUDE_BMP_SUPPORT',
				'EXCLUDE_RAS_SUPPORT',
				'EXCLUDE_JPG_SUPPORT',
				'EXCLUDE_PGX_SUPPORT'
			],
			'sources':[
				'opencv_src/3rdparty/libjasper/copyright',
				'opencv_src/3rdparty/libjasper/jasper',
				'opencv_src/3rdparty/libjasper/jas_cm.c',
				'opencv_src/3rdparty/libjasper/jas_debug.c',
				'opencv_src/3rdparty/libjasper/jas_getopt.c',
				'opencv_src/3rdparty/libjasper/jas_icc.c',
				'opencv_src/3rdparty/libjasper/jas_iccdata.c',
				'opencv_src/3rdparty/libjasper/jas_image.c',
				'opencv_src/3rdparty/libjasper/jas_init.c',
				'opencv_src/3rdparty/libjasper/jas_malloc.c',
				'opencv_src/3rdparty/libjasper/jas_seq.c',
				'opencv_src/3rdparty/libjasper/jas_stream.c',
				'opencv_src/3rdparty/libjasper/jas_string.c',
				'opencv_src/3rdparty/libjasper/jas_tmr.c',
				'opencv_src/3rdparty/libjasper/jas_tvp.c',
				'opencv_src/3rdparty/libjasper/jas_version.c',
				'opencv_src/3rdparty/libjasper/jp2_cod.c',
				'opencv_src/3rdparty/libjasper/jp2_cod.h',
				'opencv_src/3rdparty/libjasper/jp2_dec.c',
				'opencv_src/3rdparty/libjasper/jp2_dec.h',
				'opencv_src/3rdparty/libjasper/jp2_enc.c',
				'opencv_src/3rdparty/libjasper/jpc_bs.c',
				'opencv_src/3rdparty/libjasper/jpc_bs.h',
				'opencv_src/3rdparty/libjasper/jpc_cod.h',
				'opencv_src/3rdparty/libjasper/jpc_cs.c',
				'opencv_src/3rdparty/libjasper/jpc_cs.h',
				'opencv_src/3rdparty/libjasper/jpc_dec.c',
				'opencv_src/3rdparty/libjasper/jpc_dec.h',
				'opencv_src/3rdparty/libjasper/jpc_enc.c',
				'opencv_src/3rdparty/libjasper/jpc_enc.h',
				'opencv_src/3rdparty/libjasper/jpc_fix.h',
				'opencv_src/3rdparty/libjasper/jpc_flt.h',
				'opencv_src/3rdparty/libjasper/jpc_math.c',
				'opencv_src/3rdparty/libjasper/jpc_math.h',
				'opencv_src/3rdparty/libjasper/jpc_mct.c',
				'opencv_src/3rdparty/libjasper/jpc_mct.h',
				'opencv_src/3rdparty/libjasper/jpc_mqcod.c',
				'opencv_src/3rdparty/libjasper/jpc_mqcod.h',
				'opencv_src/3rdparty/libjasper/jpc_mqdec.c',
				'opencv_src/3rdparty/libjasper/jpc_mqdec.h',
				'opencv_src/3rdparty/libjasper/jpc_mqenc.c',
				'opencv_src/3rdparty/libjasper/jpc_mqenc.h',
				'opencv_src/3rdparty/libjasper/jpc_qmfb.c',
				'opencv_src/3rdparty/libjasper/jpc_qmfb.h',
				'opencv_src/3rdparty/libjasper/jpc_t1cod.c',
				'opencv_src/3rdparty/libjasper/jpc_t1cod.h',
				'opencv_src/3rdparty/libjasper/jpc_t1dec.c',
				'opencv_src/3rdparty/libjasper/jpc_t1dec.h',
				'opencv_src/3rdparty/libjasper/jpc_t1enc.c',
				'opencv_src/3rdparty/libjasper/jpc_t1enc.h',
				'opencv_src/3rdparty/libjasper/jpc_t2cod.c',
				'opencv_src/3rdparty/libjasper/jpc_t2cod.h',
				'opencv_src/3rdparty/libjasper/jpc_t2dec.c',
				'opencv_src/3rdparty/libjasper/jpc_t2dec.h',
				'opencv_src/3rdparty/libjasper/jpc_t2enc.c',
				'opencv_src/3rdparty/libjasper/jpc_t2enc.h',
				'opencv_src/3rdparty/libjasper/jpc_tagtree.c',
				'opencv_src/3rdparty/libjasper/jpc_tagtree.h',
				'opencv_src/3rdparty/libjasper/jpc_tsfb.c',
				'opencv_src/3rdparty/libjasper/jpc_tsfb.h',
				'opencv_src/3rdparty/libjasper/jpc_util.c',
				'opencv_src/3rdparty/libjasper/jpc_util.h',
				'opencv_src/3rdparty/libjasper/LICENSE',
				'opencv_src/3rdparty/libjasper/README',		
				
				'opencv_src/3rdparty/libjasper/jasper/jasper.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_cm.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_config.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_config.h.in',
				'opencv_src/3rdparty/libjasper/jasper/jas_config2.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_debug.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_fix.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_getopt.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_icc.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_image.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_init.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_malloc.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_math.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_seq.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_stream.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_string.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_tmr.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_tvp.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_types.h',
				'opencv_src/3rdparty/libjasper/jasper/jas_version.h'				
				
			],
			'conditions':[
				['OS=="win"', {
					'defines':[
						'JAS_WIN_MSVC_BUILD'
					]
				}]
			]
		},

		
		
	],
	
}