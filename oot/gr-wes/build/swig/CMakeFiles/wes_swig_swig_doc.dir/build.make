# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/wes/gnuradio/gr-wes

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/wes/gnuradio/gr-wes/build

# Utility rule file for wes_swig_swig_doc.

# Include the progress variables for this target.
include swig/CMakeFiles/wes_swig_swig_doc.dir/progress.make

swig/CMakeFiles/wes_swig_swig_doc: swig/wes_swig_doc.i


swig/wes_swig_doc.i: swig/wes_swig_doc_swig_docs/xml/index.xml
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/wes/gnuradio/gr-wes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Generating python docstrings for wes_swig_doc"
	cd /home/wes/gnuradio/gr-wes/docs/doxygen && /usr/bin/python3 -B /home/wes/gnuradio/gr-wes/docs/doxygen/swig_doc.py /home/wes/gnuradio/gr-wes/build/swig/wes_swig_doc_swig_docs/xml /home/wes/gnuradio/gr-wes/build/swig/wes_swig_doc.i

swig/wes_swig_doc_swig_docs/xml/index.xml: swig/_wes_swig_doc_tag
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/home/wes/gnuradio/gr-wes/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Generating doxygen xml for wes_swig_doc docs"
	cd /home/wes/gnuradio/gr-wes/build/swig && ./_wes_swig_doc_tag
	cd /home/wes/gnuradio/gr-wes/build/swig && /usr/bin/doxygen /home/wes/gnuradio/gr-wes/build/swig/wes_swig_doc_swig_docs/Doxyfile

wes_swig_swig_doc: swig/CMakeFiles/wes_swig_swig_doc
wes_swig_swig_doc: swig/wes_swig_doc.i
wes_swig_swig_doc: swig/wes_swig_doc_swig_docs/xml/index.xml
wes_swig_swig_doc: swig/CMakeFiles/wes_swig_swig_doc.dir/build.make

.PHONY : wes_swig_swig_doc

# Rule to build all files generated by this target.
swig/CMakeFiles/wes_swig_swig_doc.dir/build: wes_swig_swig_doc

.PHONY : swig/CMakeFiles/wes_swig_swig_doc.dir/build

swig/CMakeFiles/wes_swig_swig_doc.dir/clean:
	cd /home/wes/gnuradio/gr-wes/build/swig && $(CMAKE_COMMAND) -P CMakeFiles/wes_swig_swig_doc.dir/cmake_clean.cmake
.PHONY : swig/CMakeFiles/wes_swig_swig_doc.dir/clean

swig/CMakeFiles/wes_swig_swig_doc.dir/depend:
	cd /home/wes/gnuradio/gr-wes/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/wes/gnuradio/gr-wes /home/wes/gnuradio/gr-wes/swig /home/wes/gnuradio/gr-wes/build /home/wes/gnuradio/gr-wes/build/swig /home/wes/gnuradio/gr-wes/build/swig/CMakeFiles/wes_swig_swig_doc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : swig/CMakeFiles/wes_swig_swig_doc.dir/depend
