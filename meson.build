project(
    'Kalman SoC',
    'cpp',
    version: '0.0.1',
    subproject_dir: 'dep'
)

# Import binary helpers
python = find_program('python3', 'python', required: false)
clangFormat = find_program('clang-format', required: false)
cmake = import('cmake')

# Add Kalman filter source code
src_files = files([
    'src/SoCKalman.cpp',
])

# Include kalman directory for main executable
kalman_inc = include_directories([
    '.',
    'src'
])

# Build the source library
kalman_lib = static_library(
    'Kalman',
    [ src_files ],
    pic: false
)

# Build the backtesting tool executable
backtest = executable(
    'backtest',
    'backtest/main.cpp',
    include_directories: [ kalman_inc ],
    link_with: [ kalman_lib ],
    native: true
)

# Only build examples and tests when not a subproject
if (meson.is_subproject() != true)

    # Add unit test src
    subdir('tests')
    test_src_inc = get_variable('test_src_inc')
    test_src_files = get_variable('test_src_files')

    # Add CppUTest dependency
<<<<<<< HEAD
    cpputest = subproject('cpputest')
    cpputest_dep = cpputest.get_variable('lcpp_dep')
=======
    cpputest_opt = cmake.subproject_options()
    cpputest_opt.add_cmake_defines({'EXTENSIONS': true})
    cpputest = cmake.subproject('cpputest', options: cpputest_opt)
    cpputest_dep = cpputest.dependency('CppUTest')
    cpputestext_dep = cpputest.dependency('CppUTestExt')
>>>>>>> c9c8c2d9fc09f8652174b786026f0539c451ee4c

    # Build native unit tests
    run_tests = executable(
        'run_tests',
        [ test_src_files, src_files, './tests/main.cpp' ],
        include_directories: [ test_src_inc ],
        dependencies: [ cpputest_dep, cpputestext_dep ],
        native: true,
        build_by_default: false
    )

    # Unit test
    test('cpputest', run_tests)

    # Setup custom build commands
    run_target('lint', command: [ 'clang-format', '-verbose',
                                  '-style=file', '-i', src_files,
                                  test_src_files ])

endif

message('''

Build commands:
    ninja           compile
    ninja clean     clean
    ninja lint      prints a diff for files that do not match the style guide
'''
)
