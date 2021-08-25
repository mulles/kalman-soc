# Install script for directory: /home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/src/CppUTestExt

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/build/dep/cpputest/__CMake_build/src/CppUTestExt/libCppUTestExt.a")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/CppUTestExt" TYPE FILE FILES
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/CodeMemoryReportFormatter.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/IEEE754ExceptionsPlugin.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MemoryReportAllocator.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockExpectedCall.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockCheckedExpectedCall.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockExpectedCallsList.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockSupportPlugin.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MemoryReportFormatter.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockFailure.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockSupport.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockSupport_c.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/GMock.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/GTest.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/GTestSupport.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MemoryReporterPlugin.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/OrderedTest.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/GTestConvertor.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockActualCall.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockCheckedActualCall.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockNamedValue.h"
    "/home/mulles/Documents/2020_Documents/UNI/Master/Beuth_Berlin/Semester_4_SS2021_Masterarbeit/2021_LibreSolar/Code_and_Doc/kalman-soc/dep/cpputest/include/CppUTestExt/MockSupport.h"
    )
endif()

