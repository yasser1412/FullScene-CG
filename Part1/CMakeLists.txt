include(CheckIncludeFiles)
cmake_minimum_required(VERSION 3.15) # common to every CLion project
project(Full-Scene-Animation) # project name

if (UNIX)
    set(OpenGlLinkers -lglut -lGLU -lGL) # setting all the Glut libraries as one variable.
    ################################################

    # Common to all CLion project
    add_executable(SBE306B_Spring20_Project_Group_05 SBE306B_Spring20_Project_Group_05.cpp
                   src/startRendering.cpp src/texture.cpp src/imageloader.cpp
                   src/objLoader.cpp src/glm.cpp)
    target_link_libraries(Full-Scene-Animation ${OpenGlLinkers}) # linking opengl libraries to the project
    #################################################
endif ()

if (WIN32)
    cmake_minimum_required(VERSION 3.16)
    project(Full-Scene-Animation)

    set(CMAKE_CXX_STANDARD 17)

    # GLUT
    find_package(GLUT REQUIRED)
    include_directories(${GLUT_INCLUDE_DIR})
    if(NOT GLUT_FOUND)
        message(ERROR "GLUT not found!")
    endif(NOT GLUT_FOUND)

    # OpenGL
    find_package(OpenGL REQUIRED)
    include_directories(${OpenGL_INCLUDE_DIRS})
    link_directories(${OpenGL_LIBRARY_DIRS})
    add_definitions(${OpenGL_DEFINITIONS})
    if(NOT OPENGL_FOUND)
        message(ERROR "OPENGL not found!")
    endif(NOT OPENGL_FOUND)

    link_libraries(${OPENGL_LIBRARIES} ${GLUT_LIBRARIES} --verbose)

    # Common to all CLion project
    add_executable(SBE306B_Spring20_Project_Group_05 SBE306B_Spring20_Project_Group_05.cpp
                   src/startRendering.cpp src/texture.cpp src/imageloader.cpp
                   src/objLoader.cpp src/glm.cpp)

endif ()
