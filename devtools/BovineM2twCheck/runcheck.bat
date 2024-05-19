SET EDITOR=notepad

if not exist lib (
	mkdir lib;
	copy ..\common_kotlin_library\*.* lib
)

SET LIBRARIES=lib/kotlin-reflect.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-reflect-sources.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib-sources.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib-jdk7.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib-jdk7-sources.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib-jdk8.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-stdlib-jdk8-sources.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-test.jar
SET LIBRARIES=%LIBRARIES%;lib/kotlin-test-sources.jar

java -cp "target;%LIBRARIES%" main.BovineM2twCheckKt configuration.txt

start "%EDITOR%" eda.error.log
start "%EDITOR%" edct.error.log
start "%EDITOR%" filereferences.error.log
start "%EDITOR%" unit.error.log
start "%EDITOR%" script.error.log
start "%EDITOR%" sounds.error.log
start "%EDITOR%" stratmap.error.log
start "%EDITOR%" sundry.error.log
start "%EDITOR%" checker.output.log