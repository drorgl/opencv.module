{
	'variables':{
		#'library' : 'static_library',
		'library' : 'shared_library',
		'cuda' : '0',
		'opencl' : '0',
		'viz' : '0',
		'have_gtk' : '<!(node build_utils/pkg-config.js --exists gtk+-3.0)'
		
	},
	
	'target_defaults': {
		'include_dirs+':[
			'opencv_src/include',
			'config/<(OS)',
		],
		'direct_dependent_settings': {
			'include_dirs+': [
				'opencv_src/include',
				'config/<(OS)',
			]
		},
		'defines':[
			'__OPENCV_BUILD',
			'CVAPI_EXPORTS',
		],
		
		
	
		'msvs_settings': {
			# This magical incantation is necessary because VC++ will compile
			# object files to same directory... even if they have the same name!
			'VCCLCompilerTool': {
				'ForcedIncludeFiles' : ['stdint.h'],
			  'ObjectFile': '$(IntDir)/%(RelativeDir)/',
			  #'AdditionalOptions': ['/GL-','/w'], #['/wd4244' ,'/wd4018','/wd4133' ,'/wd4090'] #GL- was added because the forced optimization coming from node-gyp is disturbing the weird coding style from ffmpeg.
			  'WarningLevel':0,
			  'WholeProgramOptimization' : 'false',
			  'ExceptionHandling' : '1' #/EHsc
			},
			
		},
		
		'configurations':{
			'Debug':{
				'conditions': [
				  ['target_arch=="x64"', {
					'msvs_configuration_platform': 'x64',
				  }],
				],
				'defines':[
					'DEBUG',
				],
				'msvs_settings': {				
					'VCCLCompilerTool': {
						#'RuntimeLibrary': 3, # MultiThreadedDebugDLL (/MDd)
					},
					'VCLinkerTool' : {
						'GenerateDebugInformation' : 'true',
						'conditions':[
							['target_arch=="x64"', {
								'TargetMachine' : 17 # /MACHINE:X64
							}],
						],
						
					}
				}
			},
			'Release':{
				'conditions': [
				  ['target_arch=="x64"', {
					'msvs_configuration_platform': 'x64',
				  }],
				],
				'msvs_settings': {				
					'VCCLCompilerTool': {
						#'RuntimeLibrary': 2, # MultiThreadedDLL (/MD)
					},
					'VCLinkerTool' : {
						'conditions':[
							['target_arch=="x64"', {
								'TargetMachine' : 17 # /MACHINE:X64
							}],
						],
						
					}
				}
			},
		},
		
		'conditions': [
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
			[ 'OS in "win linux" and target_arch=="ia32"', {
				'defines':[
					#'ARCH_X86_64=0',
					#'ARCH_X86_32=1',
				],
			}],
			[ 'OS in "win linux" and target_arch=="x64"', {
				'defines':[
					#'ARCH_X86_64=1',
					#'ARCH_X86_32=1',
				],
			}],
			['OS == "win"',{
				# TODO: precompiled headers should be split to each project and use the "precomp.hpp" file
				# the attempt below failed because the compilers attempted to share the obj files and file sharing 
				# exceptions were thrown
				# 'msvs_precompiled_header': 'config/<(OS)/stdafx.h',
				# 'msvs_precompiled_source': 'config/<(OS)/stdafx.cpp',
			    # 'sources': ['config/<(OS)/stdafx.cpp'],
				
				'defines':[
					#'inline=__inline',
					#'__asm__=__asm',
					'WIN32',
				],
				'defines!':[
					'_CRT_SECURE_NO_DEPRECATE',
					'_CRT_NONSTDC_NO_DEPRECATE',
					'_HAS_EXCEPTIONS=0',
				],
				'include_dirs+':[
					
				],

			}],
			['OS != "win" and library == "shared_library"',{
				'cflags':[
					'-fPIC',
				],	
				'defines':[
					'PIC',
				],
			}],
		  ['OS != "win"', {
			'cflags':[
				#'-std=gnu99',
			],
			'cflags_cc!': [ '-fno-rtti', '-fno-exceptions' ],
			
			'conditions': [
			  ['OS=="solaris"', {
				'cflags': [ '-pthreads' ],
			  }],
			  ['OS not in "solaris android"', {
				'cflags': [ '-pthread' ],
			  }],
			],
		}],
		['OS=="android" and target_arch=="arm"',{
			'defines':[
				'ANDROID'
			],
			'cflags':[
				'-marm',
				'-march=armv7-a',
				'-mfpu=neon',
				'-mfloat-abi=softfp',
				'-funsafe-math-optimizations',
				'-O1',
			],
			'cflags!':['-O3','-O2'], #optimization sometimes crashes gcc
			'cflags_cc!':['-O3','-O2'],#optimization sometimes crashes gcc
			'ldflags':[
				'-llog'
			],
		  }],
		],
	  },
	'targets':
	[
		{
			'target_name':'calib3d',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/calib3d/include',
				'config/<(OS)',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/calib3d/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'features2d',
				'flann',
				'imgproc',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_calib3d.cpp',
				
				'opencv_src/modules/calib3d/include/opencv2/calib3d.hpp',
				'opencv_src/modules/calib3d/src/calibinit.cpp',
				'opencv_src/modules/calib3d/src/calibration.cpp',
				'opencv_src/modules/calib3d/src/checkchessboard.cpp',
				'opencv_src/modules/calib3d/src/circlesgrid.cpp',
				'opencv_src/modules/calib3d/src/circlesgrid.hpp',
				'opencv_src/modules/calib3d/src/compat_ptsetreg.cpp',
				'opencv_src/modules/calib3d/src/compat_stereo.cpp',
				'opencv_src/modules/calib3d/src/dls.cpp',
				'opencv_src/modules/calib3d/src/dls.h',
				'opencv_src/modules/calib3d/src/epnp.cpp',
				'opencv_src/modules/calib3d/src/epnp.h',
				'opencv_src/modules/calib3d/src/fisheye.cpp',
				'opencv_src/modules/calib3d/src/fisheye.hpp',
				'opencv_src/modules/calib3d/src/five-point.cpp',
				'opencv_src/modules/calib3d/src/fundam.cpp',
				'opencv_src/modules/calib3d/src/homography_decomp.cpp',
				'opencv_src/modules/calib3d/src/levmarq.cpp',
				'opencv_src/modules/calib3d/src/main.cpp',
				'opencv_src/modules/calib3d/src/opencl',
				'opencv_src/modules/calib3d/src/p3p.cpp',
				'opencv_src/modules/calib3d/src/p3p.h',
				'opencv_src/modules/calib3d/src/polynom_solver.cpp',
				'opencv_src/modules/calib3d/src/polynom_solver.h',
				'opencv_src/modules/calib3d/src/posit.cpp',
				'opencv_src/modules/calib3d/src/precomp.hpp',
				'opencv_src/modules/calib3d/src/ptsetreg.cpp',
				'opencv_src/modules/calib3d/src/quadsubpix.cpp',
				'opencv_src/modules/calib3d/src/rho.cpp',
				'opencv_src/modules/calib3d/src/rho.h',
				'opencv_src/modules/calib3d/src/solvepnp.cpp',
				'opencv_src/modules/calib3d/src/stereobm.cpp',
				'opencv_src/modules/calib3d/src/stereosgbm.cpp',
				'opencv_src/modules/calib3d/src/triangulate.cpp',
				'opencv_src/modules/calib3d/src/upnp.cpp',
				'opencv_src/modules/calib3d/src/upnp.h',
				'opencv_src/modules/calib3d/src/opencl/stereobm.cl',
			],
		},
		
		{
			'target_name':'core',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/core/include',
				'config/<(OS)',
			],
			'direct_dependent_settings': {
				'include_dirs+' : [
					'opencv_src/modules/core/include',
				],
			},
			'dependencies':[
				#'hal',
				'../zlib.module/zlib.gyp:zlib',
			],
			'sources':[
				'opencv_src/modules/core/include/opencv2/core.hpp',
				
				'opencv_src/modules/core/src/algorithm.cpp',
				'opencv_src/modules/core/src/alloc.cpp',
				'opencv_src/modules/core/src/arithm.cpp',
				'opencv_src/modules/core/src/arithm_core.hpp',
				'opencv_src/modules/core/src/arithm_simd.hpp',
				'opencv_src/modules/core/src/array.cpp',
				'opencv_src/modules/core/src/bufferpool.impl.hpp',
				'opencv_src/modules/core/src/command_line_parser.cpp',
				'opencv_src/modules/core/src/conjugate_gradient.cpp',
				'opencv_src/modules/core/src/convert.cpp',
				'opencv_src/modules/core/src/copy.cpp',
				'opencv_src/modules/core/src/cuda_gpu_mat.cpp',
				'opencv_src/modules/core/src/cuda_host_mem.cpp',
				'opencv_src/modules/core/src/cuda_info.cpp',
				'opencv_src/modules/core/src/cuda_stream.cpp',
				'opencv_src/modules/core/src/datastructs.cpp',
				'opencv_src/modules/core/src/directx.cpp',
				'opencv_src/modules/core/src/directx.inc.hpp',
				'opencv_src/modules/core/src/downhill_simplex.cpp',
				'opencv_src/modules/core/src/dxt.cpp',
				'opencv_src/modules/core/src/glob.cpp',
				'opencv_src/modules/core/src/gl_core_3_1.cpp',
				'opencv_src/modules/core/src/gl_core_3_1.hpp',
				'opencv_src/modules/core/src/hal_replacement.hpp',
				'opencv_src/modules/core/src/kmeans.cpp',
				'opencv_src/modules/core/src/lapack.cpp',
				'opencv_src/modules/core/src/lda.cpp',
				'opencv_src/modules/core/src/lpsolver.cpp',
				'opencv_src/modules/core/src/mathfuncs.cpp',
				'opencv_src/modules/core/src/mathfuncs_core.cpp',
				'opencv_src/modules/core/src/matmul.cpp',
				'opencv_src/modules/core/src/matop.cpp',
				'opencv_src/modules/core/src/matrix.cpp',
				'opencv_src/modules/core/src/matrix_decomp.cpp',
				'opencv_src/modules/core/src/merge.cpp',
				'opencv_src/modules/core/src/ocl.cpp',
				'opencv_src/modules/core/src/opengl.cpp',
				'opencv_src/modules/core/src/out.cpp',
				'opencv_src/modules/core/src/parallel.cpp',
				'opencv_src/modules/core/src/parallel_pthreads.cpp',
				'opencv_src/modules/core/src/pca.cpp',
				'opencv_src/modules/core/src/persistence.cpp',
				'opencv_src/modules/core/src/precomp.hpp',
				'opencv_src/modules/core/src/rand.cpp',
				'opencv_src/modules/core/src/split.cpp',
				'opencv_src/modules/core/src/stat.cpp',
				'opencv_src/modules/core/src/stl.cpp',
				'opencv_src/modules/core/src/system.cpp',
				'opencv_src/modules/core/src/tables.cpp',
				'opencv_src/modules/core/src/types.cpp',
				'opencv_src/modules/core/src/umatrix.cpp',
				'opencv_src/modules/core/src/va_intel.cpp',
			

				'opencv_src/modules/core/src/cuda/gpu_mat.cu',
				
				'opencv_src/modules/core/src/opencl/arithm.cl',
				'opencv_src/modules/core/src/opencl/convert.cl',
				'opencv_src/modules/core/src/opencl/copymakeborder.cl',
				'opencv_src/modules/core/src/opencl/copyset.cl',
				'opencv_src/modules/core/src/opencl/cvtclr_dx.cl',
				'opencv_src/modules/core/src/opencl/fft.cl',
				'opencv_src/modules/core/src/opencl/flip.cl',
				'opencv_src/modules/core/src/opencl/gemm.cl',
				'opencv_src/modules/core/src/opencl/inrange.cl',
				'opencv_src/modules/core/src/opencl/lut.cl',
				'opencv_src/modules/core/src/opencl/meanstddev.cl',
				'opencv_src/modules/core/src/opencl/minmaxloc.cl',
				'opencv_src/modules/core/src/opencl/mixchannels.cl',
				'opencv_src/modules/core/src/opencl/mulspectrums.cl',
				'opencv_src/modules/core/src/opencl/normalize.cl',
				'opencv_src/modules/core/src/opencl/reduce.cl',
				'opencv_src/modules/core/src/opencl/reduce2.cl',
				'opencv_src/modules/core/src/opencl/repeat.cl',
				'opencv_src/modules/core/src/opencl/set_identity.cl',
				'opencv_src/modules/core/src/opencl/split_merge.cl',
				'opencv_src/modules/core/src/opencl/transpose.cl',
				
				
				'opencv_src/modules/core/src/opencl/runtime/opencl_clamdblas.cpp',
				'opencv_src/modules/core/src/opencl/runtime/opencl_clamdfft.cpp',
				'opencv_src/modules/core/src/opencl/runtime/opencl_core.cpp',
				'opencv_src/modules/core/src/opencl/runtime/runtime_common.hpp',
				
				'opencv_src/modules/core/src/opencl/runtime/autogenerated/opencl_clamdblas_impl.hpp',
				'opencv_src/modules/core/src/opencl/runtime/autogenerated/opencl_clamdfft_impl.hpp',
				'opencv_src/modules/core/src/opencl/runtime/autogenerated/opencl_core_impl.hpp',
				'opencv_src/modules/core/src/opencl/runtime/autogenerated/opencl_gl_impl.hpp'
			],
		},
		
		
		{
			'target_name':'cudaarithm',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudaarithm/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudaarithm/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'opencv_src/modules/cudaarithm/include/opencv2/cudaarithm.hpp',
				'opencv_src/modules/cudaarithm/src/arithm.cpp',
				'opencv_src/modules/cudaarithm/src/core.cpp',
				'opencv_src/modules/cudaarithm/src/element_operations.cpp',
				'opencv_src/modules/cudaarithm/src/precomp.hpp',
				'opencv_src/modules/cudaarithm/src/reductions.cpp',
				
				'opencv_src/modules/cudaarithm/src/cuda/absdiff_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/absdiff_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/add_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/add_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/add_weighted.cu',
				'opencv_src/modules/cudaarithm/src/cuda/bitwise_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/bitwise_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/cmp_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/cmp_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/copy_make_border.cu',
				'opencv_src/modules/cudaarithm/src/cuda/countnonzero.cu',
				'opencv_src/modules/cudaarithm/src/cuda/div_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/div_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/integral.cu',
				'opencv_src/modules/cudaarithm/src/cuda/lut.cu',
				'opencv_src/modules/cudaarithm/src/cuda/math.cu',
				'opencv_src/modules/cudaarithm/src/cuda/minmax.cu',
				'opencv_src/modules/cudaarithm/src/cuda/minmaxloc.cu',
				'opencv_src/modules/cudaarithm/src/cuda/minmax_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/mul_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/mul_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/mul_spectrums.cu',
				'opencv_src/modules/cudaarithm/src/cuda/norm.cu',
				'opencv_src/modules/cudaarithm/src/cuda/normalize.cu',
				'opencv_src/modules/cudaarithm/src/cuda/polar_cart.cu',
				'opencv_src/modules/cudaarithm/src/cuda/reduce.cu',
				'opencv_src/modules/cudaarithm/src/cuda/split_merge.cu',
				'opencv_src/modules/cudaarithm/src/cuda/sub_mat.cu',
				'opencv_src/modules/cudaarithm/src/cuda/sub_scalar.cu',
				'opencv_src/modules/cudaarithm/src/cuda/sum.cu',
				'opencv_src/modules/cudaarithm/src/cuda/threshold.cu',
				'opencv_src/modules/cudaarithm/src/cuda/transpose.cu',
			],
		},
		
		
		{
			'target_name':'cudabgsegm',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudabgsegm/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudabgsegm/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'video',
			],
			'sources':[
				'opencv_src/modules/cudabgsegm/include/opencv2/cudabgsegm.hpp',
				'opencv_src/modules/cudabgsegm/src/mog.cpp',
				'opencv_src/modules/cudabgsegm/src/mog2.cpp',
				'opencv_src/modules/cudabgsegm/src/precomp.hpp',
				
				'opencv_src/modules/cudabgsegm/src/cuda/mog.cu',
				'opencv_src/modules/cudabgsegm/src/cuda/mog2.cu',
			],
		},
		
		
		{
			'target_name':'cudacodec',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudacodec/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudacodec/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'opencv_src/modules/cudacodec/include/opencv2/cudacodec.hpp',
				'opencv_src/modules/cudacodec/src/cuvid_video_source.cpp',
				'opencv_src/modules/cudacodec/src/cuvid_video_source.hpp',
				'opencv_src/modules/cudacodec/src/ffmpeg_video_source.cpp',
				'opencv_src/modules/cudacodec/src/ffmpeg_video_source.hpp',
				'opencv_src/modules/cudacodec/src/frame_queue.cpp',
				'opencv_src/modules/cudacodec/src/frame_queue.hpp',
				'opencv_src/modules/cudacodec/src/precomp.hpp',
				'opencv_src/modules/cudacodec/src/thread.cpp',
				'opencv_src/modules/cudacodec/src/thread.hpp',
				'opencv_src/modules/cudacodec/src/video_decoder.cpp',
				'opencv_src/modules/cudacodec/src/video_decoder.hpp',
				'opencv_src/modules/cudacodec/src/video_parser.cpp',
				'opencv_src/modules/cudacodec/src/video_parser.hpp',
				'opencv_src/modules/cudacodec/src/video_reader.cpp',
				'opencv_src/modules/cudacodec/src/video_source.cpp',
				'opencv_src/modules/cudacodec/src/video_source.hpp',
				'opencv_src/modules/cudacodec/src/video_writer.cpp',
				
				'opencv_src/modules/cudacodec/src/cuda/nv12_to_rgb.cu',
				'opencv_src/modules/cudacodec/src/cuda/rgb_to_yv12.cu',
			],
		},
		
			{
			'target_name':'cudafeatures2d',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudafeatures2d/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudafeatures2d/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'features2d',
				'flann',
				'cudafilters',
				'imgproc',
				'cudaarithm',
				'cudawarping',
			],
			'sources':[
				'opencv_src/modules/cudafeatures2d/include/opencv2/cudafeatures2d.hpp',
				'opencv_src/modules/cudafeatures2d/src/brute_force_matcher.cpp',
				'opencv_src/modules/cudafeatures2d/src/fast.cpp',
				'opencv_src/modules/cudafeatures2d/src/feature2d_async.cpp',
				'opencv_src/modules/cudafeatures2d/src/orb.cpp',
				'opencv_src/modules/cudafeatures2d/src/precomp.hpp',
				
				'opencv_src/modules/cudafeatures2d/src/cuda/bf_knnmatch.cu',
				'opencv_src/modules/cudafeatures2d/src/cuda/bf_match.cu',
				'opencv_src/modules/cudafeatures2d/src/cuda/bf_radius_match.cu',
				'opencv_src/modules/cudafeatures2d/src/cuda/fast.cu',
				'opencv_src/modules/cudafeatures2d/src/cuda/orb.cu',
			],
		},
		
		
			{
			'target_name':'cudafilters',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudafilters/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudafilters/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
				'cudaarithm',
			],
			'sources':[
				'opencv_src/modules/cudafilters/include/opencv2/cudafilters.hpp',
				'opencv_src/modules/cudafilters/src/filtering.cpp',
				'opencv_src/modules/cudafilters/src/precomp.hpp',

				'opencv_src/modules/cudafilters/src/cuda/column_filter.16sc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.16sc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.16sc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.16uc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.16uc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.16uc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32fc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32fc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32fc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32sc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32sc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.32sc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.8uc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.8uc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.8uc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/column_filter.hpp',
				'opencv_src/modules/cudafilters/src/cuda/filter2d.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16sc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16sc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16sc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16uc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16uc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.16uc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32fc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32fc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32fc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32sc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32sc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.32sc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.8uc1.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.8uc3.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.8uc4.cu',
				'opencv_src/modules/cudafilters/src/cuda/row_filter.hpp',
			],
		},
		
		
			{
			'target_name':'cudaimgproc',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudaimgproc/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudaimgproc/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/cudaimgproc/include/opencv2/cudaimgproc.hpp',
				'opencv_src/modules/cudaimgproc/src/bilateral_filter.cpp',
				'opencv_src/modules/cudaimgproc/src/blend.cpp',
				'opencv_src/modules/cudaimgproc/src/canny.cpp',
				'opencv_src/modules/cudaimgproc/src/color.cpp',
				'opencv_src/modules/cudaimgproc/src/corners.cpp',
				'opencv_src/modules/cudaimgproc/src/cvt_color_internal.h',
				'opencv_src/modules/cudaimgproc/src/generalized_hough.cpp',
				'opencv_src/modules/cudaimgproc/src/gftt.cpp',
				#'opencv_src/modules/cudaimgproc/src/histogram.cpp',
				'opencv_src/modules/cudaimgproc/src/hough_circles.cpp',
				'opencv_src/modules/cudaimgproc/src/hough_lines.cpp',
				'opencv_src/modules/cudaimgproc/src/hough_segments.cpp',
				'opencv_src/modules/cudaimgproc/src/match_template.cpp',
				'opencv_src/modules/cudaimgproc/src/mean_shift.cpp',
				'opencv_src/modules/cudaimgproc/src/mssegmentation.cpp',
				'opencv_src/modules/cudaimgproc/src/precomp.hpp',	
				
				'opencv_src/modules/cudaimgproc/src/cuda/bilateral_filter.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/blend.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/build_point_list.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/canny.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/clahe.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/color.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/corners.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/debayer.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/generalized_hough.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/gftt.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/hist.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/hough_circles.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/hough_lines.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/hough_segments.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/match_template.cu',
				'opencv_src/modules/cudaimgproc/src/cuda/mean_shift.cu',
			],
		},
		
		
		
		
		
		{
			'target_name':'cudaobjdetect',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudaobjdetect/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudaobjdetect/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'cudaarithm',
				'cudawarping',
				'imgproc',
				'objdetect',
			],
			'sources':[
				'opencv_src/modules/cudaobjdetect/include/opencv2/cudaobjdetect.hpp',
				'opencv_src/modules/cudaobjdetect/src/cascadeclassifier.cpp',
				'opencv_src/modules/cudaobjdetect/src/hog.cpp',
				'opencv_src/modules/cudaobjdetect/src/precomp.hpp',
				
				'opencv_src/modules/cudaobjdetect/src/cuda/hog.cu',
				'opencv_src/modules/cudaobjdetect/src/cuda/lbp.cu',
				'opencv_src/modules/cudaobjdetect/src/cuda/lbp.hpp',
			],
		},
		
		
		
		
		
			{
			'target_name':'cudastereo',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudastereo/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudastereo/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'calib3d',
				'features2d',
				'flann',
			],
			'sources':[
				'opencv_src/modules/cudastereo/include/opencv2/cudastereo.hpp',
				'opencv_src/modules/cudastereo/src/disparity_bilateral_filter.cpp',
				'opencv_src/modules/cudastereo/src/precomp.hpp',
				'opencv_src/modules/cudastereo/src/stereobm.cpp',
				'opencv_src/modules/cudastereo/src/stereobp.cpp',
				'opencv_src/modules/cudastereo/src/stereocsbp.cpp',
				'opencv_src/modules/cudastereo/src/util.cpp',
				
				'opencv_src/modules/cudastereo/src/cuda/disparity_bilateral_filter.cu',
				'opencv_src/modules/cudastereo/src/cuda/disparity_bilateral_filter.hpp',
				'opencv_src/modules/cudastereo/src/cuda/stereobm.cu',
				'opencv_src/modules/cudastereo/src/cuda/stereobp.cu',
				'opencv_src/modules/cudastereo/src/cuda/stereocsbp.cu',
				'opencv_src/modules/cudastereo/src/cuda/stereocsbp.hpp',
				'opencv_src/modules/cudastereo/src/cuda/util.cu',
			],
		},
		
		
		{
			'target_name':'cudawarping',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudawarping/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudawarping/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/cudawarping/include/opencv2/cudawarping.hpp',
				'opencv_src/modules/cudawarping/src/precomp.hpp',
				'opencv_src/modules/cudawarping/src/pyramids.cpp',
				'opencv_src/modules/cudawarping/src/remap.cpp',
				'opencv_src/modules/cudawarping/src/resize.cpp',
				'opencv_src/modules/cudawarping/src/warp.cpp',
				
				'opencv_src/modules/cudawarping/src/cuda/pyr_down.cu',
				'opencv_src/modules/cudawarping/src/cuda/pyr_up.cu',
				'opencv_src/modules/cudawarping/src/cuda/remap.cu',
				'opencv_src/modules/cudawarping/src/cuda/resize.cu',
				'opencv_src/modules/cudawarping/src/cuda/warp.cu',
			],
		},
		
		{
			'target_name':'cudev',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/cudev/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/cudev/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'opencv_src/modules/cudev/include/opencv2/cudev.hpp',
				'opencv_src/modules/cudev/src/stub.cpp',
			],
		},
		
		{
			'target_name':'features2d',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/features2d/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/features2d/include',
				],
			},
			'dependencies':[
				'flann',
				'core',
				#'hal',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/features2d/include/opencv2/features2d.hpp',
				
				'config/<(OS)/opencl_kernels_features2d.cpp',
				
				'opencv_src/modules/features2d/src/agast.cpp',
				'opencv_src/modules/features2d/src/agast_score.cpp',
				'opencv_src/modules/features2d/src/agast_score.hpp',
				'opencv_src/modules/features2d/src/akaze.cpp',
				'opencv_src/modules/features2d/src/bagofwords.cpp',
				'opencv_src/modules/features2d/src/blobdetector.cpp',
				'opencv_src/modules/features2d/src/brisk.cpp',
				'opencv_src/modules/features2d/src/draw.cpp',
				'opencv_src/modules/features2d/src/dynamic.cpp',
				'opencv_src/modules/features2d/src/evaluation.cpp',
				'opencv_src/modules/features2d/src/fast.cpp',
				'opencv_src/modules/features2d/src/fast_score.cpp',
				'opencv_src/modules/features2d/src/fast_score.hpp',
				'opencv_src/modules/features2d/src/feature2d.cpp',
				'opencv_src/modules/features2d/src/gftt.cpp',
				'opencv_src/modules/features2d/src/kaze.cpp',
				'opencv_src/modules/features2d/src/keypoint.cpp',
				'opencv_src/modules/features2d/src/matchers.cpp',
				'opencv_src/modules/features2d/src/mser.cpp',
				'opencv_src/modules/features2d/src/orb.cpp',
				'opencv_src/modules/features2d/src/precomp.hpp',
				
				'opencv_src/modules/features2d/src/kaze/AKAZEConfig.h',
				'opencv_src/modules/features2d/src/kaze/AKAZEFeatures.cpp',
				'opencv_src/modules/features2d/src/kaze/AKAZEFeatures.h',
				'opencv_src/modules/features2d/src/kaze/fed.cpp',
				'opencv_src/modules/features2d/src/kaze/fed.h',
				'opencv_src/modules/features2d/src/kaze/KAZEConfig.h',
				'opencv_src/modules/features2d/src/kaze/KAZEFeatures.cpp',
				'opencv_src/modules/features2d/src/kaze/KAZEFeatures.h',
				'opencv_src/modules/features2d/src/kaze/nldiffusion_functions.cpp',
				'opencv_src/modules/features2d/src/kaze/nldiffusion_functions.h',
				'opencv_src/modules/features2d/src/kaze/TEvolution.h',
				'opencv_src/modules/features2d/src/kaze/utils.h',
				
				'opencv_src/modules/features2d/src/opencl/brute_force_match.cl',
				'opencv_src/modules/features2d/src/opencl/fast.cl',
				'opencv_src/modules/features2d/src/opencl/orb.cl',
			],
		},
		
		{
			'target_name':'flann',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/flann/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/flann/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'opencv_src/modules/flann/include/opencv2/flann.hpp',
				'opencv_src/modules/flann/src/flann.cpp',
				'opencv_src/modules/flann/src/miniflann.cpp',
				'opencv_src/modules/flann/src/precomp.hpp',
			],
		},
		
		{
			'target_name':'hal',
			'type':'static_library',
			'include_dirs+' : [
				'opencv_src/modules/hal/include',
			],
			'direct_dependent_settings': {
				'include_dirs+' : [
					'opencv_src/modules/hal/include',
				],
			},
			'sources':[
				#'opencv_src/modules/hal/include/opencv2/hal.hpp',
				#'opencv_src/modules/hal/src/arithm.cpp',
				#'opencv_src/modules/hal/src/color.cpp',
				#'opencv_src/modules/hal/src/filter.cpp',
				##'opencv_src/modules/hal/src/mathfuncs.cpp',
				##'opencv_src/modules/hal/src/matrix.cpp',
				#'opencv_src/modules/hal/src/precomp.hpp',
				#'opencv_src/modules/hal/src/resize.cpp',
				##'opencv_src/modules/hal/src/stat.cpp',
				#'opencv_src/modules/hal/src/warp.cpp',
			],
		},
		
		{
			'target_name':'highgui',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/highgui/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/highgui/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgcodecs',
				'videoio',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/highgui/include/opencv2/highgui.hpp',
				#'opencv_src/modules/highgui/src/agile_wrl.h',
				#'opencv_src/modules/highgui/src/ppltasks_winrt.h',
				'opencv_src/modules/highgui/src/precomp.hpp',
				'opencv_src/modules/highgui/src/window.cpp',
				#'opencv_src/modules/highgui/src/window_carbon.cpp',
				#'opencv_src/modules/highgui/src/window_cocoa.mm',
				#'opencv_src/modules/highgui/src/window_gtk.cpp',
				#'opencv_src/modules/highgui/src/window_QT.cpp',
				#'opencv_src/modules/highgui/src/window_QT.h',
				#'opencv_src/modules/highgui/src/window_QT.qrc',
				
			],
			'conditions':[
				['have_gtk==1',{
					'sources':[
						'opencv_src/modules/highgui/src/window_gtk.cpp',
					],
					'defines':[
						'HAVE_GTK=1'
					],
					'cflags':[
						'<!(node build_utils/pkg-config.js --cflags gtk+-3.0 --silence-errors)'
					],
					'libraries':[
						'<!(node build_utils/pkg-config.js --libs gtk+-3.0 --silence-errors)'
					]
				}],
				['OS=="win"', {
					'sources' :[
						'opencv_src/modules/highgui/src/window_w32.cpp',
					],
					'link_settings': {
						'libraries': [
						  '-lVfw32.lib',
						  '-lGdi32.lib',
						  '-lAdvapi32.lib',
						  '-lUser32.lib',
						  '-lOle32.lib',
						  '-lComctl32.lib',
						  '-lComdlg32.lib',
						]
				  },
				}],
			],
		},
		
		{
			'target_name':'imgcodecs',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/imgcodecs/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/imgcodecs/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
				'png.gyp:libpng',
				'../zlib.module/zlib.gyp:zlib',
				'libjasper.gyp:libjasper',
				'libjpeg.gyp:libjpeg'
			],
			'sources':[
				'opencv_src/modules/imgcodecs/include/opencv2/imgcodecs.hpp',
				
				'opencv_src/modules/imgcodecs/src/bitstrm.cpp',
				'opencv_src/modules/imgcodecs/src/bitstrm.hpp',
				'opencv_src/modules/imgcodecs/src/exif.cpp',
				'opencv_src/modules/imgcodecs/src/exif.hpp',
				'opencv_src/modules/imgcodecs/src/grfmts.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_base.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_base.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_bmp.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_bmp.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_exr.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_exr.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_gdal.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_gdal.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_gdcm.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_gdcm.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_hdr.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_hdr.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_jpeg.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_jpeg.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_jpeg2000.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_jpeg2000.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_pam.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_pam.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_png.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_png.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_pxm.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_pxm.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_sunras.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_sunras.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_tiff.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_tiff.hpp',
				'opencv_src/modules/imgcodecs/src/grfmt_webp.cpp',
				'opencv_src/modules/imgcodecs/src/grfmt_webp.hpp',
				'opencv_src/modules/imgcodecs/src/loadsave.cpp',
				'opencv_src/modules/imgcodecs/src/precomp.hpp',
				'opencv_src/modules/imgcodecs/src/rgbe.cpp',
				'opencv_src/modules/imgcodecs/src/rgbe.hpp',
				'opencv_src/modules/imgcodecs/src/utils.cpp',
				'opencv_src/modules/imgcodecs/src/utils.hpp'
			],
		},
		
		{
			'target_name':'imgproc',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/imgproc/include',
				'config/<(OS)',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/imgproc/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_imgproc.cpp',
			
				'opencv_src/modules/imgproc/include/opencv2/imgproc.hpp',
				'opencv_src/modules/imgproc/src/accum.cpp',
				'opencv_src/modules/imgproc/src/approx.cpp',
				'opencv_src/modules/imgproc/src/blend.cpp',
				'opencv_src/modules/imgproc/src/canny.cpp',
				'opencv_src/modules/imgproc/src/clahe.cpp',
				'opencv_src/modules/imgproc/src/color.cpp',
				'opencv_src/modules/imgproc/src/colormap.cpp',
				'opencv_src/modules/imgproc/src/connectedcomponents.cpp',
				'opencv_src/modules/imgproc/src/contours.cpp',
				'opencv_src/modules/imgproc/src/convhull.cpp',
				'opencv_src/modules/imgproc/src/corner.cpp',
				'opencv_src/modules/imgproc/src/cornersubpix.cpp',
				'opencv_src/modules/imgproc/src/demosaicing.cpp',
				'opencv_src/modules/imgproc/src/deriv.cpp',
				'opencv_src/modules/imgproc/src/distransform.cpp',
				'opencv_src/modules/imgproc/src/drawing.cpp',
				'opencv_src/modules/imgproc/src/emd.cpp',
				'opencv_src/modules/imgproc/src/featureselect.cpp',
				'opencv_src/modules/imgproc/src/filter.cpp',
				'opencv_src/modules/imgproc/src/filterengine.hpp',
				'opencv_src/modules/imgproc/src/floodfill.cpp',
				'opencv_src/modules/imgproc/src/gabor.cpp',
				'opencv_src/modules/imgproc/src/gcgraph.hpp',
				'opencv_src/modules/imgproc/src/generalized_hough.cpp',
				'opencv_src/modules/imgproc/src/geometry.cpp',
				'opencv_src/modules/imgproc/src/grabcut.cpp',
				'opencv_src/modules/imgproc/src/hershey_fonts.cpp',
				'opencv_src/modules/imgproc/src/histogram.cpp',
				'opencv_src/modules/imgproc/src/hough.cpp',
				'opencv_src/modules/imgproc/src/imgwarp.cpp',
				'opencv_src/modules/imgproc/src/intersection.cpp',
				'opencv_src/modules/imgproc/src/linefit.cpp',
				'opencv_src/modules/imgproc/src/lsd.cpp',
				'opencv_src/modules/imgproc/src/matchcontours.cpp',
				'opencv_src/modules/imgproc/src/min_enclosing_triangle.cpp',
				'opencv_src/modules/imgproc/src/moments.cpp',
				'opencv_src/modules/imgproc/src/morph.cpp',
				'opencv_src/modules/imgproc/src/phasecorr.cpp',
				'opencv_src/modules/imgproc/src/precomp.hpp',
				'opencv_src/modules/imgproc/src/pyramids.cpp',
				'opencv_src/modules/imgproc/src/rotcalipers.cpp',
				'opencv_src/modules/imgproc/src/samplers.cpp',
				'opencv_src/modules/imgproc/src/segmentation.cpp',
				'opencv_src/modules/imgproc/src/shapedescr.cpp',
				'opencv_src/modules/imgproc/src/smooth.cpp',
				'opencv_src/modules/imgproc/src/subdivision2d.cpp',
				'opencv_src/modules/imgproc/src/sumpixels.cpp',
				'opencv_src/modules/imgproc/src/tables.cpp',
				'opencv_src/modules/imgproc/src/templmatch.cpp',
				'opencv_src/modules/imgproc/src/thresh.cpp',
				'opencv_src/modules/imgproc/src/undistort.cpp',
				'opencv_src/modules/imgproc/src/utils.cpp',
				'opencv_src/modules/imgproc/src/_geom.h',
				
				'opencv_src/modules/imgproc/src/opencl/accumulate.cl',
				'opencv_src/modules/imgproc/src/opencl/bilateral.cl',
				'opencv_src/modules/imgproc/src/opencl/blend_linear.cl',
				'opencv_src/modules/imgproc/src/opencl/boxFilter.cl',
				'opencv_src/modules/imgproc/src/opencl/calc_back_project.cl',
				'opencv_src/modules/imgproc/src/opencl/canny.cl',
				'opencv_src/modules/imgproc/src/opencl/clahe.cl',
				'opencv_src/modules/imgproc/src/opencl/corner.cl',
				'opencv_src/modules/imgproc/src/opencl/covardata.cl',
				'opencv_src/modules/imgproc/src/opencl/cvtcolor.cl',
				'opencv_src/modules/imgproc/src/opencl/filter2D.cl',
				'opencv_src/modules/imgproc/src/opencl/filter2DSmall.cl',
				'opencv_src/modules/imgproc/src/opencl/filterSepCol.cl',
				'opencv_src/modules/imgproc/src/opencl/filterSepRow.cl',
				'opencv_src/modules/imgproc/src/opencl/filterSep_singlePass.cl',
				'opencv_src/modules/imgproc/src/opencl/filterSmall.cl',
				'opencv_src/modules/imgproc/src/opencl/gftt.cl',
				'opencv_src/modules/imgproc/src/opencl/histogram.cl',
				'opencv_src/modules/imgproc/src/opencl/hough_lines.cl',
				'opencv_src/modules/imgproc/src/opencl/integral_sum.cl',
				'opencv_src/modules/imgproc/src/opencl/laplacian5.cl',
				'opencv_src/modules/imgproc/src/opencl/match_template.cl',
				'opencv_src/modules/imgproc/src/opencl/medianFilter.cl',
				'opencv_src/modules/imgproc/src/opencl/moments.cl',
				'opencv_src/modules/imgproc/src/opencl/morph.cl',
				'opencv_src/modules/imgproc/src/opencl/precornerdetect.cl',
				'opencv_src/modules/imgproc/src/opencl/pyr_down.cl',
				'opencv_src/modules/imgproc/src/opencl/pyr_up.cl',
				'opencv_src/modules/imgproc/src/opencl/remap.cl',
				'opencv_src/modules/imgproc/src/opencl/resize.cl',
				'opencv_src/modules/imgproc/src/opencl/threshold.cl',
				'opencv_src/modules/imgproc/src/opencl/warp_affine.cl',
				'opencv_src/modules/imgproc/src/opencl/warp_perspective.cl',
				
			],
		},
		
		{
			'target_name':'ml',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/ml/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/ml/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
			],
			'sources':[
				'opencv_src/modules/ml/include/opencv2/ml.hpp',
				'opencv_src/modules/ml/src/ann_mlp.cpp',
				'opencv_src/modules/ml/src/boost.cpp',
				'opencv_src/modules/ml/src/data.cpp',
				'opencv_src/modules/ml/src/em.cpp',
				'opencv_src/modules/ml/src/gbt.cpp',
				'opencv_src/modules/ml/src/inner_functions.cpp',
				'opencv_src/modules/ml/src/kdtree.cpp',
				'opencv_src/modules/ml/src/kdtree.hpp',
				'opencv_src/modules/ml/src/knearest.cpp',
				'opencv_src/modules/ml/src/lr.cpp',
				'opencv_src/modules/ml/src/nbayes.cpp',
				'opencv_src/modules/ml/src/precomp.hpp',
				'opencv_src/modules/ml/src/rtrees.cpp',
				'opencv_src/modules/ml/src/svm.cpp',
				'opencv_src/modules/ml/src/testset.cpp',
				'opencv_src/modules/ml/src/tree.cpp',
			],
		},
		
		{
			'target_name':'objdetect',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/objdetect/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/objdetect/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
				'ml',
				'highgui',
				'imgcodecs',
				'videoio',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_objdetect.cpp',
			
				'opencv_src/modules/objdetect/include/opencv2/objdetect.hpp',
				'opencv_src/modules/objdetect/src/cascadedetect.cpp',
				'opencv_src/modules/objdetect/src/cascadedetect.hpp',
				'opencv_src/modules/objdetect/src/cascadedetect_convert.cpp',
				'opencv_src/modules/objdetect/src/detection_based_tracker.cpp',
				'opencv_src/modules/objdetect/src/haar.cpp',
				'opencv_src/modules/objdetect/src/hog.cpp',
				'opencv_src/modules/objdetect/src/precomp.hpp',
				
				'opencv_src/modules/objdetect/src/opencl/cascadedetect.cl',
				'opencv_src/modules/objdetect/src/opencl/objdetect_hog.cl',
			],
		},
		
		{
			'target_name':'photo',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/photo/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/photo/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_photo.cpp',
			
				'opencv_src/modules/photo/include/opencv2/photo.hpp',
				'opencv_src/modules/photo/src/align.cpp',
				'opencv_src/modules/photo/src/arrays.hpp',
				'opencv_src/modules/photo/src/calibrate.cpp',
				'opencv_src/modules/photo/src/contrast_preserve.cpp',
				'opencv_src/modules/photo/src/contrast_preserve.hpp',
				'opencv_src/modules/photo/src/denoise_tvl1.cpp',
				'opencv_src/modules/photo/src/denoising.cpp',
				'opencv_src/modules/photo/src/denoising.cuda.cpp',
				'opencv_src/modules/photo/src/fast_nlmeans_denoising_invoker.hpp',
				'opencv_src/modules/photo/src/fast_nlmeans_denoising_invoker_commons.hpp',
				'opencv_src/modules/photo/src/fast_nlmeans_denoising_opencl.hpp',
				'opencv_src/modules/photo/src/fast_nlmeans_multi_denoising_invoker.hpp',
				'opencv_src/modules/photo/src/hdr_common.cpp',
				'opencv_src/modules/photo/src/hdr_common.hpp',
				'opencv_src/modules/photo/src/inpaint.cpp',
				'opencv_src/modules/photo/src/merge.cpp',
				'opencv_src/modules/photo/src/npr.cpp',
				'opencv_src/modules/photo/src/npr.hpp',
				'opencv_src/modules/photo/src/precomp.hpp',
				'opencv_src/modules/photo/src/seamless_cloning.cpp',
				'opencv_src/modules/photo/src/seamless_cloning.hpp',
				'opencv_src/modules/photo/src/seamless_cloning_impl.cpp',
				'opencv_src/modules/photo/src/tonemap.cpp',
				
				'opencv_src/modules/photo/src/cuda/nlm.cu',
				
				'opencv_src/modules/photo/src/opencl/nlmeans.cl',
			],
		},
		
		{
			'target_name':'shape',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/shape/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/shape/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'video',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/shape/include/opencv2/shape.hpp',
				'opencv_src/modules/shape/src/aff_trans.cpp',
				'opencv_src/modules/shape/src/emdL1.cpp',
				'opencv_src/modules/shape/src/emdL1_def.hpp',
				'opencv_src/modules/shape/src/haus_dis.cpp',
				'opencv_src/modules/shape/src/hist_cost.cpp',
				'opencv_src/modules/shape/src/precomp.cpp',
				'opencv_src/modules/shape/src/precomp.hpp',
				'opencv_src/modules/shape/src/scd_def.hpp',
				'opencv_src/modules/shape/src/sc_dis.cpp',
				'opencv_src/modules/shape/src/tps_trans.cpp',
			],
		},
		
		{
			'target_name':'stitching',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/stitching/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/stitching/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'features2d',
				'flann',
				'imgproc',
				'calib3d',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_stitching.cpp',
			
				'opencv_src/modules/stitching/include/opencv2/stitching.hpp',
				'opencv_src/modules/stitching/src/autocalib.cpp',
				'opencv_src/modules/stitching/src/blenders.cpp',
				'opencv_src/modules/stitching/src/camera.cpp',
				'opencv_src/modules/stitching/src/exposure_compensate.cpp',
				'opencv_src/modules/stitching/src/matchers.cpp',
				'opencv_src/modules/stitching/src/motion_estimators.cpp',
				'opencv_src/modules/stitching/src/precomp.hpp',
				'opencv_src/modules/stitching/src/seam_finders.cpp',
				'opencv_src/modules/stitching/src/stitcher.cpp',
				'opencv_src/modules/stitching/src/timelapsers.cpp',
				'opencv_src/modules/stitching/src/util.cpp',
				'opencv_src/modules/stitching/src/warpers.cpp',
				'opencv_src/modules/stitching/src/warpers_cuda.cpp',
				
				'opencv_src/modules/stitching/src/cuda/build_warp_maps.cu',
				
				'opencv_src/modules/stitching/src/opencl/multibandblend.cl',
				'opencv_src/modules/stitching/src/opencl/warpers.cl',
				
			],
		},
		
		{
			'target_name':'superres',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/superres/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/superres/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
				'video',
				'videoio',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_superres.cpp',
			
				'opencv_src/modules/superres/include/opencv2/superres.hpp',
				'opencv_src/modules/superres/src/btv_l1.cpp',
				'opencv_src/modules/superres/src/btv_l1_cuda.cpp',
				'opencv_src/modules/superres/src/frame_source.cpp',
				'opencv_src/modules/superres/src/input_array_utility.cpp',
				'opencv_src/modules/superres/src/input_array_utility.hpp',
				'opencv_src/modules/superres/src/optical_flow.cpp',
				'opencv_src/modules/superres/src/precomp.hpp',
				'opencv_src/modules/superres/src/ring_buffer.hpp',
				'opencv_src/modules/superres/src/super_resolution.cpp',
				
				'opencv_src/modules/superres/src/cuda/btv_l1_gpu.cu',
				
				'opencv_src/modules/superres/src/opencl/superres_btvl1.cl',
			],
		},
		
		{
			'target_name':'ts',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/ts/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/ts/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgcodecs',
				'videoio',
				'highgui',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/ts/include/opencv2/ts.hpp',
				'opencv_src/modules/ts/src/cuda_perf.cpp',
				'opencv_src/modules/ts/src/cuda_test.cpp',
				'opencv_src/modules/ts/src/ocl_perf.cpp',
				'opencv_src/modules/ts/src/ocl_test.cpp',
				'opencv_src/modules/ts/src/precomp.hpp',
				'opencv_src/modules/ts/src/ts.cpp',
				'opencv_src/modules/ts/src/ts_arrtest.cpp',
				'opencv_src/modules/ts/src/ts_func.cpp',
				'opencv_src/modules/ts/src/ts_gtest.cpp',
				'opencv_src/modules/ts/src/ts_perf.cpp',
			],
		},
		
		{
			'target_name':'video',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/video/include',
				'config/<(OS)',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/video/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
			],
			'sources':[
				'config/<(OS)/opencl_kernels_video.cpp',
			
				'opencv_src/modules/video/include/opencv2/video.hpp',
				'opencv_src/modules/video/src/bgfg_gaussmix2.cpp',
				'opencv_src/modules/video/src/bgfg_KNN.cpp',
				'opencv_src/modules/video/src/camshift.cpp',
				'opencv_src/modules/video/src/compat_video.cpp',
				'opencv_src/modules/video/src/ecc.cpp',
				'opencv_src/modules/video/src/kalman.cpp',
				'opencv_src/modules/video/src/lkpyramid.cpp',
				'opencv_src/modules/video/src/lkpyramid.hpp',
				'opencv_src/modules/video/src/optflowgf.cpp',
				'opencv_src/modules/video/src/precomp.hpp',
				'opencv_src/modules/video/src/tvl1flow.cpp',
				
				'opencv_src/modules/video/src/opencl/bgfg_mog2.cl',
				'opencv_src/modules/video/src/opencl/optical_flow_farneback.cl',
				'opencv_src/modules/video/src/opencl/optical_flow_tvl1.cl',
				'opencv_src/modules/video/src/opencl/pyrlk.cl',
			],
		},
		
		{
			'target_name':'videoio',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/videoio/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/videoio/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgcodecs',
				'imgproc',
			],
			'sources':[
				'opencv_src/modules/videoio/include/opencv2/videoio.hpp',
				#'opencv_src/modules/videoio/src/agile_wrl.hpp',
				'opencv_src/modules/videoio/src/cap.cpp',
				#'opencv_src/modules/videoio/src/cap_android.cpp',
				'opencv_src/modules/videoio/src/cap_avfoundation.mm',
				'opencv_src/modules/videoio/src/cap_cmu.cpp',
				'opencv_src/modules/videoio/src/cap_dc1394.cpp',
				'opencv_src/modules/videoio/src/cap_dc1394_v2.cpp',
				'opencv_src/modules/videoio/src/cap_dshow.cpp',
				'opencv_src/modules/videoio/src/cap_dshow.hpp',
				'opencv_src/modules/videoio/src/cap_ffmpeg.cpp',
				'opencv_src/modules/videoio/src/cap_ffmpeg_api.hpp',
				'opencv_src/modules/videoio/src/cap_ffmpeg_impl.hpp',
				#'opencv_src/modules/videoio/src/cap_giganetix.cpp',
				'opencv_src/modules/videoio/src/cap_gphoto2.cpp',
				#'opencv_src/modules/videoio/src/cap_gstreamer.cpp',
				'opencv_src/modules/videoio/src/cap_images.cpp',
				'opencv_src/modules/videoio/src/cap_intelperc.cpp',
				'opencv_src/modules/videoio/src/cap_intelperc.hpp',
				'opencv_src/modules/videoio/src/cap_ios_abstract_camera.mm',
				'opencv_src/modules/videoio/src/cap_ios_photo_camera.mm',
				'opencv_src/modules/videoio/src/cap_ios_video_camera.mm',
				'opencv_src/modules/videoio/src/cap_libv4l.cpp',
				'opencv_src/modules/videoio/src/cap_mjpeg_decoder.cpp',
				'opencv_src/modules/videoio/src/cap_mjpeg_encoder.cpp',
				'opencv_src/modules/videoio/src/cap_msmf.cpp',
				'opencv_src/modules/videoio/src/cap_msmf.hpp',
				'opencv_src/modules/videoio/src/cap_openni.cpp',
				'opencv_src/modules/videoio/src/cap_openni2.cpp',
				'opencv_src/modules/videoio/src/cap_pvapi.cpp',
				#'opencv_src/modules/videoio/src/cap_qt.cpp',
				'opencv_src/modules/videoio/src/cap_qtkit.mm',
				#'opencv_src/modules/videoio/src/cap_unicap.cpp',
				'opencv_src/modules/videoio/src/cap_v4l.cpp',
				#'opencv_src/modules/videoio/src/cap_vfw.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt_bridge.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt_bridge.hpp',
				#'opencv_src/modules/videoio/src/cap_winrt_capture.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt_capture.hpp',
				#'opencv_src/modules/videoio/src/cap_winrt_video.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt_video.hpp',
				#'opencv_src/modules/videoio/src/cap_ximea.cpp',
				#'opencv_src/modules/videoio/src/cap_xine.cpp',
				'opencv_src/modules/videoio/src/ffmpeg_codecs.hpp',
				#'opencv_src/modules/videoio/src/ppltasks_winrt.hpp',
				'opencv_src/modules/videoio/src/precomp.hpp',
				
				#'opencv_src/modules/videoio/src/cap_winrt/CaptureFrameGrabber.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt/CaptureFrameGrabber.hpp',
				#'opencv_src/modules/videoio/src/cap_winrt/MediaSink.hpp',
				#'opencv_src/modules/videoio/src/cap_winrt/MediaStreamSink.cpp',
				#'opencv_src/modules/videoio/src/cap_winrt/MediaStreamSink.hpp',
				#'opencv_src/modules/videoio/src/cap_winrt/MFIncludes.hpp',
			],
		},
		
		{
			'target_name':'videostab',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/videostab/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/videostab/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'imgproc',
				'video',
				'features2d',
				'calib3d',
				'flann',
				'videoio',
				'photo',
			],
			'sources':[
				'opencv_src/modules/videostab/include/opencv2/videostab.hpp',
				'opencv_src/modules/videostab/src/clp.hpp',
				'opencv_src/modules/videostab/src/deblurring.cpp',
				'opencv_src/modules/videostab/src/fast_marching.cpp',
				'opencv_src/modules/videostab/src/frame_source.cpp',
				'opencv_src/modules/videostab/src/global_motion.cpp',
				'opencv_src/modules/videostab/src/inpainting.cpp',
				'opencv_src/modules/videostab/src/log.cpp',
				'opencv_src/modules/videostab/src/motion_stabilizing.cpp',
				'opencv_src/modules/videostab/src/optical_flow.cpp',
				'opencv_src/modules/videostab/src/outlier_rejection.cpp',
				'opencv_src/modules/videostab/src/precomp.hpp',
				'opencv_src/modules/videostab/src/stabilizer.cpp',
				'opencv_src/modules/videostab/src/wobble_suppression.cpp',
				
				'opencv_src/modules/videostab/src/cuda/global_motion.cu',
			],
		},
		
		
		
		{
			'target_name':'world',
			'type':'<(library)',
			'include_dirs+' : [
				'opencv_src/modules/world/include',
			],
			'direct_dependent_settings': {
				'include_dirs' : [
					'opencv_src/modules/world/include',
				],
			},
			'dependencies':[
				'core',
				#'hal',
				'video',
				'features2d',
				'imgproc',
				'flann',
				
			],
			'sources':[
				'opencv_src/modules/world/include/opencv2/world.hpp',
				'opencv_src/modules/world/src/precomp.hpp',
				'opencv_src/modules/world/src/world_init.cpp',
			],
		},
		
		
	],
	
	'conditions':[
		['cuda == 1',{
			'targets':[
				{
					'target_name':'cudalegacy',
					'type':'<(library)',
					'include_dirs+' : [
						'opencv_src/modules/cudalegacy/include',
					],
					'direct_dependent_settings': {
						'include_dirs' : [
							'opencv_src/modules/cudalegacy/include',
						],
					},
					'dependencies':[
						'core',
						#'hal',
					],
					'sources':[
						'opencv_src/modules/cudalegacy/include/opencv2/cudalegacy.hpp',
						'opencv_src/modules/cudalegacy/src/bm.cpp',
						'opencv_src/modules/cudalegacy/src/bm_fast.cpp',
						'opencv_src/modules/cudalegacy/src/calib3d.cpp',
						'opencv_src/modules/cudalegacy/src/fgd.cpp',
						'opencv_src/modules/cudalegacy/src/gmg.cpp',
						'opencv_src/modules/cudalegacy/src/graphcuts.cpp',
						'opencv_src/modules/cudalegacy/src/image_pyramid.cpp',
						'opencv_src/modules/cudalegacy/src/interpolate_frames.cpp',
						'opencv_src/modules/cudalegacy/src/NCV.cpp',
						'opencv_src/modules/cudalegacy/src/needle_map.cpp',
						'opencv_src/modules/cudalegacy/src/precomp.hpp',
						
						'opencv_src/modules/cudalegacy/src/cuda/bm.cu',
						'opencv_src/modules/cudalegacy/src/cuda/bm_fast.cu',
						'opencv_src/modules/cudalegacy/src/cuda/calib3d.cu',
						'opencv_src/modules/cudalegacy/src/cuda/ccomponetns.cu',
						'opencv_src/modules/cudalegacy/src/cuda/fgd.cu',
						'opencv_src/modules/cudalegacy/src/cuda/fgd.hpp',
						'opencv_src/modules/cudalegacy/src/cuda/gmg.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NCV.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NCVAlg.hpp',
						'opencv_src/modules/cudalegacy/src/cuda/NCVBroxOpticalFlow.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NCVColorConversion.hpp',
						'opencv_src/modules/cudalegacy/src/cuda/NCVHaarObjectDetection.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NCVPixelOperations.hpp',
						'opencv_src/modules/cudalegacy/src/cuda/NCVPyramid.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NCVRuntimeTemplates.hpp',
						'opencv_src/modules/cudalegacy/src/cuda/needle_map.cu',
						'opencv_src/modules/cudalegacy/src/cuda/NPP_staging.cu',
					],
				},
				
				{
					'target_name':'cudaoptflow',
					'type':'<(library)',
					'include_dirs+' : [
						'opencv_src/modules/cudaoptflow/include',
					],
					'direct_dependent_settings': {
						'include_dirs' : [
							'opencv_src/modules/cudaoptflow/include',
						],
					},
					'dependencies':[
						'core',
						#'hal',
						'cudaarithm',
						'cudawarping',
						'imgproc',
						'cudaimgproc',
						'video',
					],
					'sources':[
						'opencv_src/modules/cudaoptflow/include/opencv2/cudaoptflow.hpp',
						'opencv_src/modules/cudaoptflow/src/brox.cpp',
						'opencv_src/modules/cudaoptflow/src/farneback.cpp',
						'opencv_src/modules/cudaoptflow/src/precomp.hpp',
						'opencv_src/modules/cudaoptflow/src/pyrlk.cpp',
						'opencv_src/modules/cudaoptflow/src/tvl1flow.cpp',
						
						'opencv_src/modules/cudaoptflow/src/cuda/farneback.cu',
						'opencv_src/modules/cudaoptflow/src/cuda/pyrlk.cu',
						'opencv_src/modules/cudaoptflow/src/cuda/tvl1flow.cu',
					],
				},
			],
		}],
		['viz == 1',{
			'targets':[
				{
					'target_name':'viz',
					'type':'<(library)',
					'include_dirs+' : [
						'opencv_src/modules/viz/include',
					],
					'direct_dependent_settings': {
						'include_dirs' : [
							'opencv_src/modules/viz/include',
						],
					},
					'dependencies':[
						'core',
						#'hal',
					],
					'sources':[
						'opencv_src/modules/viz/include/opencv2/viz.hpp',
						'opencv_src/modules/viz/src/clouds.cpp',
						'opencv_src/modules/viz/src/precomp.hpp',
						'opencv_src/modules/viz/src/shapes.cpp',
						'opencv_src/modules/viz/src/types.cpp',
						'opencv_src/modules/viz/src/viz3d.cpp',
						'opencv_src/modules/viz/src/vizcore.cpp',
						'opencv_src/modules/viz/src/vizimpl.cpp',
						'opencv_src/modules/viz/src/vizimpl.hpp',
						'opencv_src/modules/viz/src/widget.cpp',
						
						'opencv_src/modules/viz/src/vtk/vtkCloudMatSink.cpp',
						'opencv_src/modules/viz/src/vtk/vtkCloudMatSink.h',
						'opencv_src/modules/viz/src/vtk/vtkCloudMatSource.cpp',
						'opencv_src/modules/viz/src/vtk/vtkCloudMatSource.h',
						'opencv_src/modules/viz/src/vtk/vtkCocoaInteractorFix.mm',
						'opencv_src/modules/viz/src/vtk/vtkImageMatSource.cpp',
						'opencv_src/modules/viz/src/vtk/vtkImageMatSource.h',
						'opencv_src/modules/viz/src/vtk/vtkOBJWriter.cpp',
						'opencv_src/modules/viz/src/vtk/vtkOBJWriter.h',
						'opencv_src/modules/viz/src/vtk/vtkTrajectorySource.cpp',
						'opencv_src/modules/viz/src/vtk/vtkTrajectorySource.h',
						'opencv_src/modules/viz/src/vtk/vtkVizInteractorStyle.cpp',
						'opencv_src/modules/viz/src/vtk/vtkVizInteractorStyle.hpp',
						'opencv_src/modules/viz/src/vtk/vtkXYZReader.cpp',
						'opencv_src/modules/viz/src/vtk/vtkXYZReader.h',
						'opencv_src/modules/viz/src/vtk/vtkXYZWriter.cpp',
						'opencv_src/modules/viz/src/vtk/vtkXYZWriter.h',
						
					],
				},
			
			],
		}],
	],
}