project('cpputest', 'cpp')

cppu_src = [
            'src/CppUTest/CommandLineArguments.cpp',
            'src/CppUTest/CommandLineTestRunner.cpp',
            'src/CppUTest/JUnitTestOutput.cpp',
            'src/CppUTest/MemoryLeakDetector.cpp',
            'src/CppUTest/MemoryLeakWarningPlugin.cpp',
            'src/CppUTest/SimpleMutex.cpp',
            'src/CppUTest/SimpleString.cpp',
            'src/CppUTest/TeamCityTestOutput.cpp',
            'src/CppUTest/TestFailure.cpp',
            'src/CppUTest/TestFilter.cpp',
            'src/CppUTest/TestHarness_c.cpp',
            'src/CppUTest/TestMemoryAllocator.cpp',
            'src/CppUTest/TestOutput.cpp',
            'src/CppUTest/TestPlugin.cpp',
            'src/CppUTest/TestRegistry.cpp',
            'src/CppUTest/TestResult.cpp',
            'src/CppUTest/TestTestingFixture.cpp',
            'src/CppUTest/Utest.cpp',
]

cppue_src = [
            'src/CppUTestExt/CodeMemoryReportFormatter.cpp',
            'src/CppUTestExt/IEEE754ExceptionsPlugin.cpp',
            'src/CppUTestExt/MemoryReportAllocator.cpp',
            'src/CppUTestExt/MemoryReporterPlugin.cpp',
            'src/CppUTestExt/MemoryReportFormatter.cpp',
            'src/CppUTestExt/MockActualCall.cpp',
            'src/CppUTestExt/MockExpectedCall.cpp',
            'src/CppUTestExt/MockExpectedCallsList.cpp',
            'src/CppUTestExt/MockFailure.cpp',
            'src/CppUTestExt/MockNamedValue.cpp',
            'src/CppUTestExt/MockSupport.cpp',
            'src/CppUTestExt/MockSupport_c.cpp',
            'src/CppUTestExt/MockSupportPlugin.cpp',
            'src/CppUTestExt/OrderedTest.cpp',
]

platform_src = [ 'src/Platforms/Gcc/UtestPlatform.cpp' ]

cppu_inc = include_directories('include')

libcpputest = library(  'cpputest', [cppu_src, platform_src],
                        include_directories : cppu_inc )
libcpputestext = library(  'cpputestext',[cppue_src, cppu_src, platform_src],
                        include_directories : cppu_inc )

lcpp_dep = declare_dependency(link_with : [libcpputest, libcpputestext],
                    include_directories : [cppu_inc])
