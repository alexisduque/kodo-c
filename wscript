#! /usr/bin/env python
# encoding: utf-8

APPNAME = 'kodoc'
VERSION = '3.0.0'


def recurse_helper(ctx, name):
    if not ctx.has_dependency_path(name):
        ctx.fatal('Load a tool to find %s as system dependency' % name)
    else:
        p = ctx.dependency_path(name)
        ctx.recurse([p])


def options(opt):

    import waflib.extras.wurf_dependency_bundle as bundle
    import waflib.extras.wurf_dependency_resolve as resolve

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='boost',
        git_repository='github.com/steinwurf/boost.git',
        major=1, minor=8, patch=1))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='cpuid',
        git_repository='github.com/steinwurf/cpuid.git',
        major=3, minor=3, patch=1))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='fifi',
        git_repository='github.com/steinwurf/fifi.git',
        major=19, minor=0, patch=0))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='gtest',
        git_repository='github.com/steinwurf/gtest.git',
        major=2, minor=3, patch=1))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='kodo',
        git_repository='github.com/steinwurf/kodo.git',
        major=25, minor=0, patch=0))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='platform',
        git_repository='github.com/steinwurf/platform.git',
        major=1, minor=3, patch=0))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='recycle',
        git_repository='github.com/steinwurf/recycle.git',
        major=1, minor=1, patch=1))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='sak',
        git_repository='github.com/steinwurf/sak.git',
        major=14, minor=0, patch=1))

    bundle.add_dependency(opt, resolve.ResolveVersion(
        name='waf-tools',
        git_repository='github.com/steinwurf/waf-tools.git',
        major=2, minor=45, patch=0))

    opt.load('wurf_configure_output')
    opt.load('wurf_dependency_bundle')
    opt.load('wurf_standalone')
    opt.load('wurf_tools')


def configure(conf):

    if conf.is_toplevel():

        conf.load('wurf_dependency_bundle')
        conf.load('wurf_tools')

        conf.load_external_tool('install_path', 'wurf_install_path')
        conf.load_external_tool('mkspec', 'wurf_cxx_mkspec_tool')
        conf.load_external_tool('project_gen', 'wurf_project_generator')
        conf.load_external_tool('runners', 'wurf_runner')

        recurse_helper(conf, 'boost')
        recurse_helper(conf, 'fifi')
        recurse_helper(conf, 'gtest')
        recurse_helper(conf, 'kodo')
        recurse_helper(conf, 'sak')
        recurse_helper(conf, 'recycle')
        recurse_helper(conf, 'platform')
        recurse_helper(conf, 'cpuid')


def build(bld):

    CXX = bld.env.get_flat("CXX")
    # Matches both g++ and clang++
    if 'g++' in CXX or 'clang' in CXX:
        # The -fPIC is required for all underlying static libraries that
        # will be included in the shared library
        bld.env.append_value('CXXFLAGS', '-fPIC')
        # Hide most of the private symbols in the shared library to decrease
        # its size and improve its load time
        bld.env.append_value('CXXFLAGS', '-fvisibility=hidden')
        bld.env.append_value('CXXFLAGS', '-fvisibility-inlines-hidden')
        bld.env.append_value('LINKFLAGS', '-fvisibility=hidden')

    # Load the dependencies first
    if bld.is_toplevel():

        bld.load('wurf_dependency_bundle')

        recurse_helper(bld, 'boost')
        recurse_helper(bld, 'fifi')
        recurse_helper(bld, 'gtest')
        recurse_helper(bld, 'kodo')
        recurse_helper(bld, 'sak')
        recurse_helper(bld, 'recycle')
        recurse_helper(bld, 'platform')
        recurse_helper(bld, 'cpuid')

    extra_cxxflags = []

    # Matches MSVC
    if 'CL.exe' in CXX or 'cl.exe' in CXX:
        extra_cxxflags = ['/bigobj']

    bld.stlib(
        source='src/kodoc/kodoc.cpp',
        target='kodoc_static',
        name='kodoc_static',
        cxxflags=extra_cxxflags,
        defines=['KODOC_STATIC'],
        export_defines=['KODOC_STATIC'],
        export_includes='src',
        use=['kodo_includes', 'boost_includes', 'fifi',
             'recycle_includes', 'sak_includes', 'platform_includes'])

    # Define the task generator that will build the kodoc shared library
    gen = bld.shlib(
        source='src/kodoc/kodoc.cpp',
        target='kodoc',
        name='kodoc',
        cxxflags=extra_cxxflags,
        defines=['KODOC_DLL_EXPORTS'],
        install_path=None,
        export_includes='src',
        use=['kodo_includes', 'boost_includes', 'fifi',
             'recycle_includes', 'sak_includes', 'platform_includes'])

    # Make sure that the task generator is posted, which is necessary in
    # order to access the task generator by name in child projects.
    # We need this to get the location of the compiled shared library
    # when running the unit tests
    gen.post()

    # Define the applications after the 'kodoc' task generator is posted
    if bld.is_toplevel():

        bld.recurse('test')
        bld.recurse('examples/encode_decode_on_the_fly')
        bld.recurse('examples/encode_decode_simple')
        bld.recurse('examples/raw_symbols')
        bld.recurse('examples/shallow_encode_decode')
        bld.recurse('examples/switch_systematic_on_off')
        bld.recurse('examples/udp_sender_receiver')
        bld.recurse('examples/use_trace_layers')
        bld.recurse('benchmark/kodoc_throughput')
