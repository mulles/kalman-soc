# Install script for directory: /home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/src/CppUTest

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "RelWithDebInfo")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/build/dep/cpputest/__CMake_build/src/CppUTest/libCppUTest.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/CppUTest" TYPE FILE FILES
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/CommandLineArguments.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/PlatformSpecificFunctions.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestMemoryAllocator.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/CommandLineTestRunner.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/PlatformSpecificFunctions_c.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestOutput.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/CppUTestConfig.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/SimpleString.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/SimpleStringInternalCache.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestPlugin.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/JUnitTestOutput.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TeamCityTestOutput.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/StandardCLibrary.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestRegistry.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/MemoryLeakDetector.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestFailure.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestResult.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/MemoryLeakDetectorMallocMacros.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestFilter.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestTestingFixture.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/MemoryLeakDetectorNewMacros.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestHarness.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/Utest.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/MemoryLeakWarningPlugin.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/TestHarness_c.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/UtestMacros.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTest/SimpleMutex.h"
    )
endif()

