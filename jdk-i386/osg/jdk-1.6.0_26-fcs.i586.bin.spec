%global __os_install_post %{nil}
%global __spec_install_post %{nil}
%global __debug_install_post %{nil}
%global debug_package %{nil}
%undefine __debug_package
%undefine _enable_debug_packages
Name: jdk
Epoch: 2000
Version: 1.6.0_26
Release: fcs.1%{?dist}
Group: Development/Tools
URL: http://java.sun.com/
License: Copyright (c) 2010, Oracle and/or its affiliates. All rights reserved. Also under other license(s) as shown at the Description field.
Summary: Java(TM) Platform Standard Edition Development Kit
Source: jdk-1.6.0_26-fcs.i586.bin.tar.gz
ExclusiveArch: i386
AutoReqProv: no
Prefix: /usr/java
Requires: /bin/basename
Requires: /bin/cat
Requires: /bin/cp
Requires: /bin/gawk
Requires: /bin/grep
Requires: /bin/ln
Requires: /bin/ls
Requires: /bin/mkdir
Requires: /bin/mv
Requires: /bin/pwd
Requires: /bin/rm
Requires: /bin/sed
Requires: /bin/sort
Requires: /bin/touch
Requires: /usr/bin/cut
Requires: /usr/bin/dirname
Requires: /usr/bin/expr
Requires: /usr/bin/find
Requires: /usr/bin/tail
Requires: /usr/bin/tr
Requires: /usr/bin/wc
Requires: /bin/sh
Requires: /bin/sh
Requires: /bin/sh
Requires: /bin/sh
Requires: rpmlib(PayloadFilesHavePrefix)
Requires: rpmlib(CompressedFileNames)
Provides: jaxp_parser_impl
Provides: xml-commons-apis
Provides: jdk
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
The Java Platform Standard Edition Development Kit (JDK) includes both
the runtime environment (Java virtual machine, the Java platform classes
and supporting files) and development tools (compilers, debuggers,
tool libraries and other tools).

The JDK is a development environment for building applications, applets
and components that can be deployed with the Java Platform Standard
Edition Runtime Environment.



%prep
%setup -n jdk-1.6.0_26-fcs.i586.extract



%build
exit 0



%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
mv * $RPM_BUILD_ROOT
pushd $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/i386/client/classes.jsa)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/i386/client/classes.jsa
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/plugin.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/plugin.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/ext/localedata.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/ext/localedata.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/rt.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/rt.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/jsse.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/jsse.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/lib/tools.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/lib/tools.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/javaws.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/javaws.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/deploy.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/deploy.jar
mkdir -p $RPM_BUILD_ROOT/$(dirname /usr/java/jdk1.6.0_26/jre/lib/charsets.jar)
touch $RPM_BUILD_ROOT/usr/java/jdk1.6.0_26/jre/lib/charsets.jar

popd


%files
%defattr(-,root,root,-)
%dir /etc/.java
%dir /etc/.java/.systemPrefs
%config(noreplace) %verify(group link user mode rdev) /etc/.java/.systemPrefs/.system.lock
%config(noreplace) %verify(group link user mode rdev) /etc/.java/.systemPrefs/.systemRootModFile
%attr(0755,root,root) %config() %verify(group link user mode rdev) /etc/init.d/jexec
%dir /usr/java
%dir /usr/java/jdk1.6.0_26
%doc /usr/java/jdk1.6.0_26/COPYRIGHT
%doc /usr/java/jdk1.6.0_26/LICENSE
%doc /usr/java/jdk1.6.0_26/README.html
%doc /usr/java/jdk1.6.0_26/THIRDPARTYLICENSEREADME.txt
%dir /usr/java/jdk1.6.0_26/bin
/usr/java/jdk1.6.0_26/bin/ControlPanel
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/HtmlConverter
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/appletviewer
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/apt
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/extcheck
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/idlj
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jar
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jarsigner
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/java
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/java-rmi.cgi
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/javac
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/javadoc
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/javah
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/javap
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/javaws
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jconsole
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jcontrol
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jdb
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jhat
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jinfo
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jmap
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jps
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jrunscript
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jsadebugd
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jstack
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jstat
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jstatd
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/jvisualvm
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/keytool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/native2ascii
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/orbd
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/pack200
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/policytool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/rmic
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/rmid
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/rmiregistry
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/schemagen
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/serialver
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/servertool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/tnameserv
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/unpack200
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/wsgen
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/wsimport
%attr(0755,root,root) /usr/java/jdk1.6.0_26/bin/xjc
%dir /usr/java/jdk1.6.0_26/demo
%dir /usr/java/jdk1.6.0_26/demo/applets
/usr/java/jdk1.6.0_26/demo/applets.html
%dir /usr/java/jdk1.6.0_26/demo/applets/Animator
/usr/java/jdk1.6.0_26/demo/applets/Animator/Animation.class
/usr/java/jdk1.6.0_26/demo/applets/Animator/AnimationFrame.class
/usr/java/jdk1.6.0_26/demo/applets/Animator/Animator.class
/usr/java/jdk1.6.0_26/demo/applets/Animator/Animator.java
/usr/java/jdk1.6.0_26/demo/applets/Animator/DescriptionFrame.class
/usr/java/jdk1.6.0_26/demo/applets/Animator/ParseException.class
%dir /usr/java/jdk1.6.0_26/demo/applets/Animator/audio
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/0.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/1.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/2.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/3.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/4.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/5.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/6.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/7.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/8.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/9.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/audio/spacemusic.au
/usr/java/jdk1.6.0_26/demo/applets/Animator/example1.html
/usr/java/jdk1.6.0_26/demo/applets/Animator/example2.html
/usr/java/jdk1.6.0_26/demo/applets/Animator/example3.html
/usr/java/jdk1.6.0_26/demo/applets/Animator/example4.html
%dir /usr/java/jdk1.6.0_26/demo/applets/Animator/images
%dir /usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T1.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T10.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T2.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T3.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T4.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T5.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T6.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T7.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T8.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/Beans/T9.gif
%dir /usr/java/jdk1.6.0_26/demo/applets/Animator/images/SimpleAnimation
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/SimpleAnimation/T1.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/SimpleAnimation/T2.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/images/loading-msg.gif
/usr/java/jdk1.6.0_26/demo/applets/Animator/index.html
%dir /usr/java/jdk1.6.0_26/demo/applets/ArcTest
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/ArcCanvas.class
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/ArcControls.class
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/ArcTest.class
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/ArcTest.java
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/IntegerTextField.class
/usr/java/jdk1.6.0_26/demo/applets/ArcTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/BarChart
/usr/java/jdk1.6.0_26/demo/applets/BarChart/BarChart.class
/usr/java/jdk1.6.0_26/demo/applets/BarChart/BarChart.java
/usr/java/jdk1.6.0_26/demo/applets/BarChart/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/Blink
/usr/java/jdk1.6.0_26/demo/applets/Blink/Blink$1.class
/usr/java/jdk1.6.0_26/demo/applets/Blink/Blink.class
/usr/java/jdk1.6.0_26/demo/applets/Blink/Blink.java
/usr/java/jdk1.6.0_26/demo/applets/Blink/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/CardTest
/usr/java/jdk1.6.0_26/demo/applets/CardTest/CardPanel.class
/usr/java/jdk1.6.0_26/demo/applets/CardTest/CardTest.class
/usr/java/jdk1.6.0_26/demo/applets/CardTest/CardTest.java
/usr/java/jdk1.6.0_26/demo/applets/CardTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/Clock
/usr/java/jdk1.6.0_26/demo/applets/Clock/Clock.class
/usr/java/jdk1.6.0_26/demo/applets/Clock/Clock.java
/usr/java/jdk1.6.0_26/demo/applets/Clock/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/DitherTest
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/CardinalTextField.class
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/DitherCanvas.class
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/DitherControls.class
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/DitherTest.class
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/DitherTest.java
/usr/java/jdk1.6.0_26/demo/applets/DitherTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/DrawTest
/usr/java/jdk1.6.0_26/demo/applets/DrawTest/DrawControls.class
/usr/java/jdk1.6.0_26/demo/applets/DrawTest/DrawPanel.class
/usr/java/jdk1.6.0_26/demo/applets/DrawTest/DrawTest.class
/usr/java/jdk1.6.0_26/demo/applets/DrawTest/DrawTest.java
/usr/java/jdk1.6.0_26/demo/applets/DrawTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/Fractal
/usr/java/jdk1.6.0_26/demo/applets/Fractal/CLSFractal.class
/usr/java/jdk1.6.0_26/demo/applets/Fractal/CLSFractal.java
/usr/java/jdk1.6.0_26/demo/applets/Fractal/CLSRule.class
/usr/java/jdk1.6.0_26/demo/applets/Fractal/CLSTurtle.class
/usr/java/jdk1.6.0_26/demo/applets/Fractal/ContextLSystem.class
/usr/java/jdk1.6.0_26/demo/applets/Fractal/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/GraphLayout
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/Edge.class
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/Graph.class
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/Graph.java
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/GraphPanel.class
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/Node.class
%dir /usr/java/jdk1.6.0_26/demo/applets/GraphLayout/audio
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/audio/computer.au
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/audio/drip.au
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/audio/gong.au
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/example1.html
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/example2.html
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/example3.html
/usr/java/jdk1.6.0_26/demo/applets/GraphLayout/example4.html
%dir /usr/java/jdk1.6.0_26/demo/applets/GraphicsTest
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/AppletFrame.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/AppletFrame.java
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/ArcCard.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/ArcDegreePanel.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/ArcPanel.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/ColorUtils.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/GraphicsCards.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/GraphicsPanel.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/GraphicsTest.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/GraphicsTest.java
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/OvalShape.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/PolygonShape.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/RectShape.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/RoundRectShape.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/Shape.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/ShapeTest.class
/usr/java/jdk1.6.0_26/demo/applets/GraphicsTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/ImageMap
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/AniArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/AniArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ButtonFilter.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ButtonFilter.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ClickArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ClickArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/DelayedSoundArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/DelayedSoundArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HighlightArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HighlightArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HighlightFilter.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HighlightFilter.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HrefButtonArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/HrefButtonArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ImageMap.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ImageMap.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ImageMapArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/ImageMapArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/LinkArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/LinkArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/NameArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/NameArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/RoundButtonFilter.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/RoundButtonFilter.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/RoundHrefButtonArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/RoundHrefButtonArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/SoundArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/SoundArea.java
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/TickerArea.class
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/TickerArea.java
%dir /usr/java/jdk1.6.0_26/demo/applets/ImageMap/audio
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/audio/chirp1.au
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/audio/hi.au
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/example1.html
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/imagemapcheat.html
%dir /usr/java/jdk1.6.0_26/demo/applets/ImageMap/images
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/images/jim.graham.gif
/usr/java/jdk1.6.0_26/demo/applets/ImageMap/sources.html
%dir /usr/java/jdk1.6.0_26/demo/applets/JumpingBox
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/JumpingBox.class
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/JumpingBox.java
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/adapt-or-die.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/cannot.be.completed.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/danger.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/ip.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/that.hurts.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/thin.bell.au
/usr/java/jdk1.6.0_26/demo/applets/JumpingBox/sounds/tiptoe.thru.the.tulips.au
%dir /usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/Atom.class
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/Matrix3D.class
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/Matrix3D.java
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/XYZApp.class
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/XYZApp.java
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/XYZChemModel.class
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/example1.html
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/example2.html
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/example3.html
%dir /usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/HyaluronicAcid.xyz
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/benzene.xyz
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/buckminsterfullerine.xyz
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/cyclohexane.xyz
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/ethane.xyz
/usr/java/jdk1.6.0_26/demo/applets/MoleculeViewer/models/water.xyz
%dir /usr/java/jdk1.6.0_26/demo/applets/NervousText
/usr/java/jdk1.6.0_26/demo/applets/NervousText/NervousText.class
/usr/java/jdk1.6.0_26/demo/applets/NervousText/NervousText.java
/usr/java/jdk1.6.0_26/demo/applets/NervousText/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/SimpleGraph
/usr/java/jdk1.6.0_26/demo/applets/SimpleGraph/GraphApplet.class
/usr/java/jdk1.6.0_26/demo/applets/SimpleGraph/GraphApplet.java
/usr/java/jdk1.6.0_26/demo/applets/SimpleGraph/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/SortDemo
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/BidirBubbleSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/BidirBubbleSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/BubbleSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/BubbleSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/QSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/QSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/SortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/SortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/SortItem.class
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/SortItem.java
/usr/java/jdk1.6.0_26/demo/applets/SortDemo/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/SpreadSheet
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/Cell.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/CellUpdater.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/InputField.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/Node.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/SpreadSheet.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/SpreadSheet.java
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/SpreadSheetInput.class
/usr/java/jdk1.6.0_26/demo/applets/SpreadSheet/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/TicTacToe
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/TicTacToe.class
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/TicTacToe.java
%dir /usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio/beep.au
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio/ding.au
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio/return.au
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio/yahoo1.au
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/audio/yahoo2.au
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/example1.html
%dir /usr/java/jdk1.6.0_26/demo/applets/TicTacToe/images
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/images/cross.gif
/usr/java/jdk1.6.0_26/demo/applets/TicTacToe/images/not.gif
%dir /usr/java/jdk1.6.0_26/demo/applets/WireFrame
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/FileFormatException.class
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/Matrix3D.class
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/Matrix3D.java
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/Model3D.class
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/ThreeD.class
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/ThreeD.java
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/example1.html
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/example2.html
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/example3.html
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/example4.html
%dir /usr/java/jdk1.6.0_26/demo/applets/WireFrame/models
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/models/cube.obj
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/models/dinasaur.obj
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/models/hughes_500.obj
/usr/java/jdk1.6.0_26/demo/applets/WireFrame/models/knoxS.obj
%dir /usr/java/jdk1.6.0_26/demo/jfc
%dir /usr/java/jdk1.6.0_26/demo/jfc/CodePointIM
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/CodePointIM.jar
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/README.html
%dir /usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/CodePointIM.java
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/CodePointInputMethod.java
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/CodePointInputMethodDescriptor.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/resources
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/resources/codepoint.properties
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/resources/codepoint_ja.properties
/usr/java/jdk1.6.0_26/demo/jfc/CodePointIM/src/resources/codepoint_zh_CN.properties
%dir /usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/FileChooserDemo.jar
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/ExampleFileView.java
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/FileChooserDemo.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/resources
%dir /usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/resources/images
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/resources/images/gifIcon.gif
/usr/java/jdk1.6.0_26/demo/jfc/FileChooserDemo/src/resources/images/jpgIcon.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/Font2DTest
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/Font2DTest.html
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/Font2DTest.jar
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/src
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/src/Font2DTest.java
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/src/Font2DTestApplet.java
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/src/FontPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/Font2DTest/src/RangeMenu.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/Java2Demo.html
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/Java2Demo.jar
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/fonts
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/fonts/A.ttf
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/bld.jpg
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/boat.png
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/box.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/boxwave.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/clone.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/clouds.jpg
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/cupanim.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/duke.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/duke.png
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/duke.running.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/dukeplug.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/fight.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/globe.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/java-logo.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/java_logo.png
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/jumptojavastrip.png
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/loop.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/looping.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/magnify.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/painting.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/print.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/remove.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/snooze.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/star7.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/start.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/start2.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/stop.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/stop2.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/surfing.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/thumbsup.gif
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/images/tip.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/AnimatingControlsSurface.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/AnimatingSurface.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/CloningFeature.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/ControlsSurface.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/CustomControls.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/CustomControlsContext.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/DemoFonts.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/DemoGroup.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/DemoImages.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/DemoPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/GlobalControls.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/GlobalPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/Intro.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/Java2Demo.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/Java2DemoApplet.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/MemoryMonitor.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/PerformanceMonitor.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/RunWindow.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/Surface.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/TextureChooser.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/Tools.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Arcs_Curves
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Arcs_Curves/Arcs.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Arcs_Curves/BezierAnim.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Arcs_Curves/Curves.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Arcs_Curves/Ellipses.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Clipping
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Clipping/Areas.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Clipping/ClipAnim.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Clipping/Intersection.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Clipping/Text.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Colors
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Colors/BullsEye.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Colors/ColorConvert.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Colors/Rotator3D.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Composite
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Composite/ACimages.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Composite/ACrules.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Composite/FadeAnim.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts/AllFonts.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts/AttributedStr.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts/Highlighting.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts/Outline.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Fonts/Tree.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Images
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Images/DukeAnim.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Images/ImageOps.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Images/JPEGFlip.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Images/WarpImage.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Lines
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Lines/Caps.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Lines/Dash.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Lines/Joins.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Lines/LineAnim.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Mix
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Mix/Balls.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Mix/BezierScroller.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Mix/Stars3D.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paint
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paint/GradAnim.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paint/Gradient.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paint/Texture.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paint/TextureAnim.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paths
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paths/Append.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paths/CurveQuadTo.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paths/FillStroke.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Paths/WindingRule.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Transforms
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Transforms/Rotate.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Transforms/SelectTx.java
/usr/java/jdk1.6.0_26/demo/jfc/Java2D/src/java2d/demos/Transforms/TransformAnim.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Laffy
/usr/java/jdk1.6.0_26/demo/jfc/Laffy/laffy.png
/usr/java/jdk1.6.0_26/demo/jfc/Laffy/readme.html
%dir /usr/java/jdk1.6.0_26/demo/jfc/Metalworks
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/Metalworks.jar
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/AquaMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/BigContrastMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/ContrastMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/DemoMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/GreenMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/KhakiMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalThemeMenu.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/Metalworks.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalworksDocumentFrame.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalworksFrame.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalworksHelp.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalworksInBox.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/MetalworksPrefs.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/PropertiesMetalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/UISwitchListener.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources
%dir /usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/back.gif
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/credits.html
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/duke.gif
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/javalogo.gif
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/metal.html
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/metalworks.html
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/swing.html
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/HelpFiles/toc.html
/usr/java/jdk1.6.0_26/demo/jfc/Metalworks/src/resources/MyTheme.theme
%dir /usr/java/jdk1.6.0_26/demo/jfc/Notepad
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/Notepad.jar
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/Notepad/src
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/ElementTreePanel.java
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/Notepad.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/Notepad.properties
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/Notepad_fr.properties
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/Notepad_sv.properties
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/Notepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/copy.gif
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/cut.gif
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/new.gif
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/open.gif
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/paste.gif
/usr/java/jdk1.6.0_26/demo/jfc/Notepad/src/resources/save.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SampleTree
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/README.txt
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/SampleTree.jar
%dir /usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/DynamicTreeNode.java
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/SampleData.java
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/SampleTree.java
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/SampleTreeCellRenderer.java
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/SampleTreeModel.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/resources
%dir /usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/resources/images
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/resources/images/collapsed.gif
/usr/java/jdk1.6.0_26/demo/jfc/SampleTree/src/resources/images/expanded.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/Stylepad
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/README.txt
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/Stylepad.jar
%dir /usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/ElementTreePanel.java
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/HelloWorld.java
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/Notepad.java
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/Stylepad.java
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/Wonderland.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Notepad.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Notepad_fr.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Notepad_sv.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Notepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Stylepad.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Stylepad_sv.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/Stylepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/alice.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/bold.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/bullets.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/caterpillar.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/center.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/copy.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/cut.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/fg.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/hatter.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/italic.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/left.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/new.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/open.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/paste.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/rabbit.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/rabbit2.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/right.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/save.gif
/usr/java/jdk1.6.0_26/demo/jfc/Stylepad/src/resources/underline.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingApplet
/usr/java/jdk1.6.0_26/demo/jfc/SwingApplet/README.txt
/usr/java/jdk1.6.0_26/demo/jfc/SwingApplet/SwingApplet.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingApplet/SwingApplet.jar
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingApplet/src
/usr/java/jdk1.6.0_26/demo/jfc/SwingApplet/src/SwingApplet.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/README.txt
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/SwingSet2.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/SwingSet2.jar
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/AquaTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/BezierAnimationPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ButtonDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/CharcoalTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/CodeViewer.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ColorChooserDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ComboBoxDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ContrastTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/DemoModule.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/DirectionPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/EmeraldTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ExampleFileView.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/FileChooserDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/HtmlDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/InternalFrameDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/LayoutControlPanel.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ListDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/OptionPaneDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/Permuter.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ProgressBarDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/RubyTheme.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ScrollPaneDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/SliderDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/SplitPaneDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/SwingSet2.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/SwingSet2Applet.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/TabbedPaneDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/TableDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/ToolTipDemo.java
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/TreeDemo.java
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/ant.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/bug.html
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/About.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/COPYRIGHT
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/apple.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/asparagus.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/banana.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/broccoli.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/cantaloupe.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/carrot.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/corn.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/grapefruit.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/grapes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/kiwi.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/onion.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/peach.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/pear.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/pepper.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/pickle.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/pineapple.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/raspberry.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/strawberry.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/tomato.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/food/watermelon.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/cab.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/cab_small.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/fish.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/fish_small.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/moon.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/moon_small.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/sun.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/ImageClub/misc/sun_small.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/COPYRIGHT
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/ant.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/book.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/bug.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/bug2.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/crest.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/king.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/micro.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/Octavo/seaweed.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b1.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b1d.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b1p.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b1r.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b2.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b2d.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b2p.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b2r.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b3.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b3d.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b3p.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/b3r.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/bl.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/bldn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/bm.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/bmdn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/br.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/brdn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/c.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/cb.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/cbr.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/cbrs.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/cbs.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/cdn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/ml.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/mldn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/mr.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/mrdn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/rb.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/rbp.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/rbr.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/rbrs.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/rbs.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/tl.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/tldn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/tm.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/tmdn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/toggle.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/toggledn.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/tr.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/buttons/trdn.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/brenteyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/brenthair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/brentmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/georgeseyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/georgeshair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/georgesmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/hanseyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/hanshair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/hansmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/howardeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/howardhair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/howardmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jameseyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jameshair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jamesmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jeffeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jeffhair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jeffmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/joneyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jonhair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/jonmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/laraeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/larahair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/laramouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/larryeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/larryhair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/larrymouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/lisaeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/lisahair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/lisamouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/michaeleyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/michaelhair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/michaelmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/philipeyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/philiphair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/philipmouth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/scotteyes.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/scotthair.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/combobox/scottmouth.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/filechooser
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/filechooser/find.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/filechooser/gifIcon.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/filechooser/help.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/filechooser/jpgIcon.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/htmldemo
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/htmldemo/back.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/htmldemo/forward.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/htmldemo/header.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/blue.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/cyan.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/gray.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/green.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/magenta.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/red.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/list/yellow.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/optionpane
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/optionpane/bottle.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/optionpane/ibd.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/optionpane/ibu.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/COPYRIGHT
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/colheader.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/crayons.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/lowerleft.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/rowheader.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/upperleft.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/scrollpane/upperright.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/splash.png
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/splitpane
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/splitpane/README
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/splitpane/earth.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/splitpane/moon.jpg
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/blake.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/brooke.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/david.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/ewan.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/ewan.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/hania.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/laine.jpg
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/matthew.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tabbedpane/stephen.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JButton.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JColorChooser.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JComboBox.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JDesktop.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JDialog.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JEditorPane.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JFileChooser.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JList.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JMenu.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JOptionPane.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JProgressBar.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JRadioButton.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JScrollBar.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JScrollPane.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JSlider.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JSplitPane.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JTabbedPane.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JTable.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/JTree.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/toolbar/ToolTip.gif
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tooltip
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/images/tooltip/cow.gif
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/index.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/king.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/preface.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/seaweed.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/swingset.properties
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/swingset_ja.properties
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/swingset_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/title.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet2/src/resources/tree.txt
%dir /usr/java/jdk1.6.0_26/demo/jfc/SwingSet3
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet3/readme.html
/usr/java/jdk1.6.0_26/demo/jfc/SwingSet3/swingset3.png
%dir /usr/java/jdk1.6.0_26/demo/jfc/TableExample
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/README.txt
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/TableExample.jar
%dir /usr/java/jdk1.6.0_26/demo/jfc/TableExample/src
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/JDBCAdapter.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/OldJTable.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableExample.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableExample2.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableExample3.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableExample4.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableMap.java
/usr/java/jdk1.6.0_26/demo/jfc/TableExample/src/TableSorter.java
%dir /usr/java/jdk1.6.0_26/demo/jpda
/usr/java/jdk1.6.0_26/demo/jpda/examples.jar
%dir /usr/java/jdk1.6.0_26/demo/jvmti
%dir /usr/java/jdk1.6.0_26/demo/jvmti/agent_util
/usr/java/jdk1.6.0_26/demo/jvmti/agent_util/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/agent_util/src
/usr/java/jdk1.6.0_26/demo/jvmti/agent_util/src/agent_util.c
/usr/java/jdk1.6.0_26/demo/jvmti/agent_util/src/agent_util.h
%dir /usr/java/jdk1.6.0_26/demo/jvmti/gctest
/usr/java/jdk1.6.0_26/demo/jvmti/gctest/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/gctest/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/gctest/lib/libgctest.so
%dir /usr/java/jdk1.6.0_26/demo/jvmti/gctest/src
/usr/java/jdk1.6.0_26/demo/jvmti/gctest/src/gctest.c
/usr/java/jdk1.6.0_26/demo/jvmti/gctest/src/sample.makefile.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapTracker
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/README.txt
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/heapTracker.jar
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/lib/libheapTracker.so
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/src
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/src/HeapTracker.java
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/src/heapTracker.c
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/src/heapTracker.h
/usr/java/jdk1.6.0_26/demo/jvmti/heapTracker/src/sample.makefile.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapViewer
/usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/lib/libheapViewer.so
%dir /usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/src
/usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/src/heapViewer.c
/usr/java/jdk1.6.0_26/demo/jvmti/heapViewer/src/sample.makefile.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/hprof
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/hprof/src
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/Tracker.java
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/debug_malloc.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/debug_malloc.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_b_spec.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_blocks.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_blocks.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_check.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_check.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_class.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_class.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_cpu.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_cpu.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_error.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_error.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_event.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_event.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_frame.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_frame.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_init.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_init.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_io.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_io.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_ioname.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_ioname.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_listener.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_listener.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_loader.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_loader.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_md.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_monitor.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_monitor.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_object.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_object.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_reference.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_reference.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_site.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_site.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_stack.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_stack.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_string.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_string.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_table.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_table.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tag.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tag.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tls.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tls.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_trace.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_trace.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tracker.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_tracker.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_util.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/hprof_util.h
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/jvm.hprof.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/linux
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/linux/hprof_md.c
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/manual.html
/usr/java/jdk1.6.0_26/demo/jvmti/hprof/src/sample.makefile.txt
/usr/java/jdk1.6.0_26/demo/jvmti/index.html
%dir /usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo
/usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/src
/usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/src/java_crw_demo.c
/usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/src/java_crw_demo.h
/usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/src/sample.makefile.txt
/usr/java/jdk1.6.0_26/demo/jvmti/java_crw_demo/src/test_crw.c
%dir /usr/java/jdk1.6.0_26/demo/jvmti/minst
/usr/java/jdk1.6.0_26/demo/jvmti/minst/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/minst/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/minst/lib/libminst.so
/usr/java/jdk1.6.0_26/demo/jvmti/minst/minst.jar
%dir /usr/java/jdk1.6.0_26/demo/jvmti/minst/src
/usr/java/jdk1.6.0_26/demo/jvmti/minst/src/Minst.java
/usr/java/jdk1.6.0_26/demo/jvmti/minst/src/minst.c
/usr/java/jdk1.6.0_26/demo/jvmti/minst/src/minst.h
/usr/java/jdk1.6.0_26/demo/jvmti/minst/src/sample.makefile.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/mtrace
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/mtrace/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/mtrace/lib/libmtrace.so
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/mtrace.jar
%dir /usr/java/jdk1.6.0_26/demo/jvmti/mtrace/src
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/src/Mtrace.java
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/src/mtrace.c
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/src/mtrace.h
/usr/java/jdk1.6.0_26/demo/jvmti/mtrace/src/sample.makefile.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/versionCheck
/usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/lib/libversionCheck.so
%dir /usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/src
/usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/src/sample.makefile.txt
/usr/java/jdk1.6.0_26/demo/jvmti/versionCheck/src/versionCheck.c
%dir /usr/java/jdk1.6.0_26/demo/jvmti/waiters
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/README.txt
%dir /usr/java/jdk1.6.0_26/demo/jvmti/waiters/lib
%attr(0755,root,root) /usr/java/jdk1.6.0_26/demo/jvmti/waiters/lib/libwaiters.so
%dir /usr/java/jdk1.6.0_26/demo/jvmti/waiters/src
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Agent.cpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Agent.hpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Monitor.cpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Monitor.hpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Thread.cpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/Thread.hpp
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/sample.makefile.txt
/usr/java/jdk1.6.0_26/demo/jvmti/waiters/src/waiters.cpp
%dir /usr/java/jdk1.6.0_26/demo/management
%dir /usr/java/jdk1.6.0_26/demo/management/FullThreadDump
/usr/java/jdk1.6.0_26/demo/management/FullThreadDump/FullThreadDump.jar
/usr/java/jdk1.6.0_26/demo/management/FullThreadDump/README.txt
%dir /usr/java/jdk1.6.0_26/demo/management/FullThreadDump/src
/usr/java/jdk1.6.0_26/demo/management/FullThreadDump/src/Deadlock.java
/usr/java/jdk1.6.0_26/demo/management/FullThreadDump/src/FullThreadDump.java
/usr/java/jdk1.6.0_26/demo/management/FullThreadDump/src/ThreadMonitor.java
%dir /usr/java/jdk1.6.0_26/demo/management/JTop
/usr/java/jdk1.6.0_26/demo/management/JTop/JTop.jar
/usr/java/jdk1.6.0_26/demo/management/JTop/README.txt
%dir /usr/java/jdk1.6.0_26/demo/management/JTop/src
/usr/java/jdk1.6.0_26/demo/management/JTop/src/JTop.java
/usr/java/jdk1.6.0_26/demo/management/JTop/src/JTopPlugin.java
%dir /usr/java/jdk1.6.0_26/demo/management/JTop/src/META-INF
%dir /usr/java/jdk1.6.0_26/demo/management/JTop/src/META-INF/services
/usr/java/jdk1.6.0_26/demo/management/JTop/src/META-INF/services/com.sun.tools.jconsole.JConsolePlugin
%dir /usr/java/jdk1.6.0_26/demo/management/MemoryMonitor
/usr/java/jdk1.6.0_26/demo/management/MemoryMonitor/MemoryMonitor.jar
/usr/java/jdk1.6.0_26/demo/management/MemoryMonitor/README.txt
%dir /usr/java/jdk1.6.0_26/demo/management/MemoryMonitor/src
/usr/java/jdk1.6.0_26/demo/management/MemoryMonitor/src/MemoryMonitor.java
%dir /usr/java/jdk1.6.0_26/demo/management/VerboseGC
/usr/java/jdk1.6.0_26/demo/management/VerboseGC/README.txt
/usr/java/jdk1.6.0_26/demo/management/VerboseGC/VerboseGC.jar
%dir /usr/java/jdk1.6.0_26/demo/management/VerboseGC/src
/usr/java/jdk1.6.0_26/demo/management/VerboseGC/src/PrintGCStat.java
/usr/java/jdk1.6.0_26/demo/management/VerboseGC/src/VerboseGC.java
/usr/java/jdk1.6.0_26/demo/management/index.html
%dir /usr/java/jdk1.6.0_26/demo/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/README.txt
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/FileChooserDemo/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Font2DTest/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Java2D/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Metalworks/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Notepad/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SampleTree/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/Stylepad/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingApplet/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/SwingSet2/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/jfc/TableExample/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/FullThreadDump/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/JTop
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/JTop/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/MemoryMonitor/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/management/VerboseGC/nbproject/project.xml
/usr/java/jdk1.6.0_26/demo/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/scripting
%dir /usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/build.properties
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/build.xml
%dir /usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/nbproject
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/demo/nbproject/scripting/jconsole-plugin/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/demo/plugin
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets
/usr/java/jdk1.6.0_26/demo/plugin/applets.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Animator
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/Animation.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/AnimationFrame.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/Animator.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/Animator.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/DescriptionFrame.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/ParseException.class
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/0.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/1.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/2.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/3.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/4.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/5.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/6.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/7.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/8.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/9.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/audio/spacemusic.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/example1.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/example2.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/example3.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/example4.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T1.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T10.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T2.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T3.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T4.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T5.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T6.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T7.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T8.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/Beans/T9.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/SimpleAnimation
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/SimpleAnimation/T1.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/SimpleAnimation/T2.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/images/loading-msg.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/Animator/index.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/ArcCanvas.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/ArcControls.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/ArcTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/ArcTest.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/IntegerTextField.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ArcTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/BarChart
/usr/java/jdk1.6.0_26/demo/plugin/applets/BarChart/BarChart.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/BarChart/BarChart.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/BarChart/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Blink
/usr/java/jdk1.6.0_26/demo/plugin/applets/Blink/Blink$1.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Blink/Blink.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Blink/Blink.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/Blink/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/CardTest
/usr/java/jdk1.6.0_26/demo/plugin/applets/CardTest/CardPanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/CardTest/CardTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/CardTest/CardTest.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/CardTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Clock
/usr/java/jdk1.6.0_26/demo/plugin/applets/Clock/Clock.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Clock/Clock.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/Clock/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/CardinalTextField.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/DitherCanvas.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/DitherControls.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/DitherTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/DitherTest.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/DitherTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest
/usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest/DrawControls.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest/DrawPanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest/DrawTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest/DrawTest.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/DrawTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/CLSFractal.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/CLSFractal.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/CLSRule.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/CLSTurtle.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/ContextLSystem.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/Fractal/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/Edge.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/Graph.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/Graph.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/GraphPanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/Node.class
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/audio
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/audio/computer.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/audio/drip.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/audio/gong.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/example1.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/example2.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/example3.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphLayout/example4.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/AppletFrame.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/AppletFrame.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/ArcCard.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/ArcDegreePanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/ArcPanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/ColorUtils.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/GraphicsCards.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/GraphicsPanel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/GraphicsTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/GraphicsTest.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/OvalShape.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/PolygonShape.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/RectShape.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/RoundRectShape.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/Shape.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/ShapeTest.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/GraphicsTest/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/AniArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/AniArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ButtonFilter.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ButtonFilter.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ClickArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ClickArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/DelayedSoundArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/DelayedSoundArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HighlightArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HighlightArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HighlightFilter.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HighlightFilter.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HrefButtonArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/HrefButtonArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ImageMap.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ImageMap.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ImageMapArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/ImageMapArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/LinkArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/LinkArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/NameArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/NameArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/RoundButtonFilter.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/RoundButtonFilter.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/RoundHrefButtonArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/RoundHrefButtonArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/SoundArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/SoundArea.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/TickerArea.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/TickerArea.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/audio
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/audio/chirp1.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/audio/hi.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/example1.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/imagemapcheat.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/images
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/images/jim.graham.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/ImageMap/sources.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/JumpingBox.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/JumpingBox.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/adapt-or-die.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/cannot.be.completed.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/danger.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/ip.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/that.hurts.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/thin.bell.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/JumpingBox/sounds/tiptoe.thru.the.tulips.au
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/Atom.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/Matrix3D.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/Matrix3D.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/XYZApp.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/XYZApp.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/XYZChemModel.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/example1.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/example2.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/example3.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/HyaluronicAcid.xyz
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/benzene.xyz
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/buckminsterfullerine.xyz
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/cyclohexane.xyz
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/ethane.xyz
/usr/java/jdk1.6.0_26/demo/plugin/applets/MoleculeViewer/models/water.xyz
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/NervousText
/usr/java/jdk1.6.0_26/demo/plugin/applets/NervousText/NervousText.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/NervousText/NervousText.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/NervousText/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/SimpleGraph
/usr/java/jdk1.6.0_26/demo/plugin/applets/SimpleGraph/GraphApplet.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SimpleGraph/GraphApplet.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SimpleGraph/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/BidirBubbleSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/BidirBubbleSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/BubbleSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/BubbleSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/QSortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/QSortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/SortAlgorithm.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/SortAlgorithm.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/SortItem.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/SortItem.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SortDemo/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/Cell.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/CellUpdater.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/InputField.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/Node.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/SpreadSheet.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/SpreadSheet.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/SpreadSheetInput.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/SpreadSheet/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/TicTacToe.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/TicTacToe.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio/beep.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio/ding.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio/return.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio/yahoo1.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/audio/yahoo2.au
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/example1.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/images
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/images/cross.gif
/usr/java/jdk1.6.0_26/demo/plugin/applets/TicTacToe/images/not.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/FileFormatException.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/Matrix3D.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/Matrix3D.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/Model3D.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/ThreeD.class
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/ThreeD.java
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/example1.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/example2.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/example3.html
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/example4.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/models
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/models/cube.obj
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/models/dinasaur.obj
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/models/hughes_500.obj
/usr/java/jdk1.6.0_26/demo/plugin/applets/WireFrame/models/knoxS.obj
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/CodePointIM.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/README.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/CodePointIM.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/CodePointInputMethod.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/CodePointInputMethodDescriptor.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/resources
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/resources/codepoint.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/resources/codepoint_ja.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/CodePointIM/src/resources/codepoint_zh_CN.properties
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/FileChooserDemo.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/README.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/ExampleFileView.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/FileChooserDemo.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/resources
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/resources/images
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/resources/images/gifIcon.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/FileChooserDemo/src/resources/images/jpgIcon.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/Font2DTest.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/Font2DTest.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/README.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/src/Font2DTest.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/src/Font2DTestApplet.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/src/FontPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Font2DTest/src/RangeMenu.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/Java2Demo.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/Java2Demo.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/README.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/fonts
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/fonts/A.ttf
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/bld.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/boat.png
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/box.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/boxwave.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/clone.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/clouds.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/cupanim.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/duke.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/duke.png
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/duke.running.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/dukeplug.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/fight.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/globe.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/java-logo.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/java_logo.png
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/jumptojavastrip.png
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/loop.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/looping.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/magnify.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/painting.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/print.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/remove.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/snooze.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/star7.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/start.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/start2.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/stop.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/stop2.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/surfing.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/thumbsup.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/images/tip.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/AnimatingControlsSurface.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/AnimatingSurface.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/CloningFeature.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/ControlsSurface.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/CustomControls.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/CustomControlsContext.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/DemoFonts.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/DemoGroup.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/DemoImages.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/DemoPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/GlobalControls.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/GlobalPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/Intro.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/Java2Demo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/Java2DemoApplet.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/MemoryMonitor.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/PerformanceMonitor.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/RunWindow.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/Surface.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/TextureChooser.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/Tools.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Arcs_Curves
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Arcs_Curves/Arcs.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Arcs_Curves/BezierAnim.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Arcs_Curves/Curves.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Arcs_Curves/Ellipses.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Clipping
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Clipping/Areas.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Clipping/ClipAnim.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Clipping/Intersection.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Clipping/Text.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Colors
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Colors/BullsEye.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Colors/ColorConvert.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Colors/Rotator3D.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Composite
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Composite/ACimages.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Composite/ACrules.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Composite/FadeAnim.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts/AllFonts.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts/AttributedStr.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts/Highlighting.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts/Outline.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Fonts/Tree.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Images
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Images/DukeAnim.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Images/ImageOps.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Images/JPEGFlip.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Images/WarpImage.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Lines
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Lines/Caps.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Lines/Dash.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Lines/Joins.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Lines/LineAnim.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Mix
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Mix/Balls.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Mix/BezierScroller.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Mix/Stars3D.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paint
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paint/GradAnim.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paint/Gradient.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paint/Texture.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paint/TextureAnim.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paths
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paths/Append.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paths/CurveQuadTo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paths/FillStroke.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Paths/WindingRule.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Transforms
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Transforms/Rotate.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Transforms/SelectTx.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Java2D/src/java2d/demos/Transforms/TransformAnim.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Laffy
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Laffy/laffy.png
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Laffy/readme.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/Metalworks.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/README.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/AquaMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/BigContrastMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/ContrastMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/DemoMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/GreenMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/KhakiMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalThemeMenu.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/Metalworks.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalworksDocumentFrame.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalworksFrame.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalworksHelp.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalworksInBox.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/MetalworksPrefs.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/PropertiesMetalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/UISwitchListener.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/back.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/credits.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/duke.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/javalogo.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/metal.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/metalworks.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/swing.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/HelpFiles/toc.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Metalworks/src/resources/MyTheme.theme
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/Notepad.jar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/README.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/ElementTreePanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/Notepad.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/Notepad.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/Notepad_fr.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/Notepad_sv.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/Notepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/copy.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/cut.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/new.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/open.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/paste.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Notepad/src/resources/save.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/README.txt
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/SampleTree.jar
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/DynamicTreeNode.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/SampleData.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/SampleTree.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/SampleTreeCellRenderer.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/SampleTreeModel.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/resources
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/resources/images
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/resources/images/collapsed.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SampleTree/src/resources/images/expanded.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/README.txt
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/Stylepad.jar
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/ElementTreePanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/HelloWorld.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/Notepad.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/Stylepad.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/Wonderland.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Notepad.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Notepad_fr.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Notepad_sv.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Notepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Stylepad.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Stylepad_sv.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/Stylepad_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/alice.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/bold.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/bullets.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/caterpillar.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/center.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/copy.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/cut.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/fg.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/hatter.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/italic.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/left.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/new.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/open.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/paste.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/rabbit.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/rabbit2.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/right.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/save.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/Stylepad/src/resources/underline.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet/README.txt
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet/SwingApplet.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet/SwingApplet.jar
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingApplet/src/SwingApplet.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/README.txt
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/SwingSet2.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/SwingSet2.jar
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/AquaTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/BezierAnimationPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ButtonDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/CharcoalTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/CodeViewer.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ColorChooserDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ComboBoxDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ContrastTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/DemoModule.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/DirectionPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/EmeraldTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ExampleFileView.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/FileChooserDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/HtmlDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/InternalFrameDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/LayoutControlPanel.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ListDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/OptionPaneDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/Permuter.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ProgressBarDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/RubyTheme.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ScrollPaneDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/SliderDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/SplitPaneDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/SwingSet2.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/SwingSet2Applet.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/TabbedPaneDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/TableDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/ToolTipDemo.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/TreeDemo.java
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/ant.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/bug.html
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/About.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/COPYRIGHT
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/apple.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/asparagus.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/banana.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/broccoli.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/cantaloupe.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/carrot.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/corn.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/grapefruit.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/grapes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/kiwi.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/onion.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/peach.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/pear.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/pepper.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/pickle.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/pineapple.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/raspberry.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/strawberry.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/tomato.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/food/watermelon.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/cab.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/cab_small.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/fish.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/fish_small.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/moon.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/moon_small.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/sun.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/ImageClub/misc/sun_small.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/COPYRIGHT
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/ant.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/book.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/bug.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/bug2.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/crest.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/king.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/micro.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/Octavo/seaweed.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b1.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b1d.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b1p.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b1r.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b2.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b2d.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b2p.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b2r.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b3.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b3d.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b3p.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/b3r.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/bl.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/bldn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/bm.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/bmdn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/br.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/brdn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/c.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/cb.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/cbr.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/cbrs.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/cbs.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/cdn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/ml.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/mldn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/mr.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/mrdn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/rb.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/rbp.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/rbr.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/rbrs.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/rbs.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/tl.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/tldn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/tm.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/tmdn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/toggle.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/toggledn.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/tr.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/buttons/trdn.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/brenteyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/brenthair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/brentmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/georgeseyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/georgeshair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/georgesmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/hanseyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/hanshair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/hansmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/howardeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/howardhair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/howardmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jameseyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jameshair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jamesmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jeffeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jeffhair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jeffmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/joneyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jonhair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/jonmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/laraeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/larahair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/laramouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/larryeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/larryhair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/larrymouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/lisaeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/lisahair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/lisamouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/michaeleyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/michaelhair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/michaelmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/philipeyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/philiphair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/philipmouth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/scotteyes.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/scotthair.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/combobox/scottmouth.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/filechooser
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/filechooser/find.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/filechooser/gifIcon.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/filechooser/help.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/filechooser/jpgIcon.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/htmldemo
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/htmldemo/back.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/htmldemo/forward.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/htmldemo/header.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/blue.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/cyan.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/gray.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/green.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/magenta.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/red.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/list/yellow.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/optionpane
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/optionpane/bottle.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/optionpane/ibd.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/optionpane/ibu.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/COPYRIGHT
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/colheader.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/crayons.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/lowerleft.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/rowheader.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/upperleft.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/scrollpane/upperright.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/splash.png
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/splitpane
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/splitpane/README
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/splitpane/earth.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/splitpane/moon.jpg
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/blake.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/brooke.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/david.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/ewan.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/ewan.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/hania.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/laine.jpg
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/matthew.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tabbedpane/stephen.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JButton.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JColorChooser.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JComboBox.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JDesktop.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JDialog.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JEditorPane.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JFileChooser.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JList.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JMenu.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JOptionPane.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JProgressBar.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JRadioButton.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JScrollBar.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JScrollPane.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JSlider.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JSplitPane.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JTabbedPane.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JTable.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/JTree.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/toolbar/ToolTip.gif
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tooltip
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/images/tooltip/cow.gif
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/index.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/king.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/preface.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/seaweed.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/swingset.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/swingset_ja.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/swingset_zh_CN.properties
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/title.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet2/src/resources/tree.txt
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet3
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet3/readme.html
/usr/java/jdk1.6.0_26/demo/plugin/jfc/SwingSet3/swingset3.png
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/README.txt
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/TableExample.jar
%dir /usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/JDBCAdapter.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/OldJTable.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableExample.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableExample2.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableExample3.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableExample4.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableMap.java
/usr/java/jdk1.6.0_26/demo/plugin/jfc/TableExample/src/TableSorter.java
%dir /usr/java/jdk1.6.0_26/demo/scripting
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/README.txt
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/build.xml
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/jconsole-plugin.jar
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/META-INF
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/META-INF/services
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/META-INF/services/com.sun.tools.jconsole.JConsolePlugin
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo/scripting
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo/scripting/jconsole
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo/scripting/jconsole/EditableAtEndDocument.java
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo/scripting/jconsole/ScriptJConsolePlugin.java
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/com/sun/demo/scripting/jconsole/ScriptShellPanel.java
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/resources
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/resources/jconsole.js
%dir /usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/heapdump.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/hello.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/invoke.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/jstack.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/jtop.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/sysprops.js
/usr/java/jdk1.6.0_26/demo/scripting/jconsole-plugin/src/scripts/verbose.js
%dir /usr/java/jdk1.6.0_26/include
/usr/java/jdk1.6.0_26/include/classfile_constants.h
/usr/java/jdk1.6.0_26/include/jawt.h
/usr/java/jdk1.6.0_26/include/jdwpTransport.h
/usr/java/jdk1.6.0_26/include/jni.h
/usr/java/jdk1.6.0_26/include/jvmti.h
%dir /usr/java/jdk1.6.0_26/include/linux
/usr/java/jdk1.6.0_26/include/linux/jawt_md.h
/usr/java/jdk1.6.0_26/include/linux/jni_md.h
%dir /usr/java/jdk1.6.0_26/jre
%doc /usr/java/jdk1.6.0_26/jre/COPYRIGHT
%doc /usr/java/jdk1.6.0_26/jre/LICENSE
%doc /usr/java/jdk1.6.0_26/jre/README
%doc /usr/java/jdk1.6.0_26/jre/THIRDPARTYLICENSEREADME.txt
%doc /usr/java/jdk1.6.0_26/jre/Welcome.html
%dir /usr/java/jdk1.6.0_26/jre/bin
/usr/java/jdk1.6.0_26/jre/bin/ControlPanel
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/java
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/java_vm
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/javaws
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/jcontrol
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/keytool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/orbd
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/pack200
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/policytool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/rmid
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/rmiregistry
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/servertool
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/tnameserv
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/bin/unpack200
%dir /usr/java/jdk1.6.0_26/jre/javaws
/usr/java/jdk1.6.0_26/jre/javaws/javaws
%dir /usr/java/jdk1.6.0_26/jre/lib
/usr/java/jdk1.6.0_26/jre/lib/alt-rt.jar
/usr/java/jdk1.6.0_26/jre/lib/alt-string.jar
%dir /usr/java/jdk1.6.0_26/jre/lib/applet
%dir /usr/java/jdk1.6.0_26/jre/lib/audio
/usr/java/jdk1.6.0_26/jre/lib/audio/soundbank.gm
/usr/java/jdk1.6.0_26/jre/lib/calendars.properties
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/charsets.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/charsets.pack
/usr/java/jdk1.6.0_26/jre/lib/classlist
%dir /usr/java/jdk1.6.0_26/jre/lib/cmm
/usr/java/jdk1.6.0_26/jre/lib/cmm/CIEXYZ.pf
/usr/java/jdk1.6.0_26/jre/lib/cmm/GRAY.pf
/usr/java/jdk1.6.0_26/jre/lib/cmm/LINEAR_RGB.pf
/usr/java/jdk1.6.0_26/jre/lib/cmm/PYCC.pf
/usr/java/jdk1.6.0_26/jre/lib/cmm/sRGB.pf
/usr/java/jdk1.6.0_26/jre/lib/content-types.properties
%dir /usr/java/jdk1.6.0_26/jre/lib/deploy
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/deploy.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/deploy.pack
/usr/java/jdk1.6.0_26/jre/lib/deploy/ffjcext.zip
/usr/java/jdk1.6.0_26/jre/lib/deploy/java-icon.ico
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_de.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_es.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_fr.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_it.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_ja.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_ko.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_pt_BR.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_sv.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_zh_CN.properties
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/deploy/messages_zh_HK.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/messages_zh_TW.properties
/usr/java/jdk1.6.0_26/jre/lib/deploy/splash.gif
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/applications
/usr/java/jdk1.6.0_26/jre/lib/desktop/applications/sun-java.desktop
/usr/java/jdk1.6.0_26/jre/lib/desktop/applications/sun-javaws.desktop
/usr/java/jdk1.6.0_26/jre/lib/desktop/applications/sun_java.desktop
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/16x16/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrast/48x48/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/16x16/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/HighContrastInverse/48x48/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/16x16/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/LowContrast/48x48/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/16x16/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/apps
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/apps/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/apps/sun-javaws.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/apps/sun-jcontrol.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/mimetypes
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/mimetypes/gnome-mime-application-x-java-archive.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/mimetypes/gnome-mime-application-x-java-jnlp-file.png
/usr/java/jdk1.6.0_26/jre/lib/desktop/icons/hicolor/48x48/mimetypes/gnome-mime-text-x-java.png
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/mime
%dir /usr/java/jdk1.6.0_26/jre/lib/desktop/mime/packages
/usr/java/jdk1.6.0_26/jre/lib/desktop/mime/packages/x-java-archive.xml
/usr/java/jdk1.6.0_26/jre/lib/desktop/mime/packages/x-java-jnlp-file.xml
%dir /usr/java/jdk1.6.0_26/jre/lib/ext
/usr/java/jdk1.6.0_26/jre/lib/ext/dnsns.jar
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/ext/localedata.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/ext/localedata.pack
/usr/java/jdk1.6.0_26/jre/lib/ext/meta-index
/usr/java/jdk1.6.0_26/jre/lib/ext/sunjce_provider.jar
/usr/java/jdk1.6.0_26/jre/lib/ext/sunpkcs11.jar
/usr/java/jdk1.6.0_26/jre/lib/flavormap.properties
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.2.1.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.2.1.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.3.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.3.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.4.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.4.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.6.0.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.6.0.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.RedHat.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.SuSE.11.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.SuSE.11.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.SuSE.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.SuSE.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Sun.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Sun.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Turbo.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Turbo.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Ubuntu.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.Ubuntu.properties.src
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.bfc
/usr/java/jdk1.6.0_26/jre/lib/fontconfig.properties.src
%dir /usr/java/jdk1.6.0_26/jre/lib/fonts
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaBrightDemiBold.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaBrightDemiItalic.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaBrightItalic.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaBrightRegular.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaSansDemiBold.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaSansRegular.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaTypewriterBold.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/LucidaTypewriterRegular.ttf
/usr/java/jdk1.6.0_26/jre/lib/fonts/fonts.dir
%dir /usr/java/jdk1.6.0_26/jre/lib/i386
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/client
/usr/java/jdk1.6.0_26/jre/lib/i386/client/Xusage.txt
%attr(0444,root,root) %ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/i386/client/classes.jsa
/usr/java/jdk1.6.0_26/jre/lib/i386/client/libjsig.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/client/libjvm.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/headless
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/headless/libmawt.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/jli
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/jli/libjli.so
/usr/java/jdk1.6.0_26/jre/lib/i386/jvm.cfg
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libJdbcOdbc.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libattach.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libawt.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libcmm.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libdcpr.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libdeploy.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libdt_socket.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libfontmanager.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libhprof.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libinstrument.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libioser12.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libj2gss.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libj2pcsc.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libj2pkcs11.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjaas_unix.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjava.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjava_crw_demo.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjavaplugin_jni.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjavaplugin_nscp.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjavaplugin_nscp_gcc29.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjawt.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjdwp.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjpeg.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjsig.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjsound.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libjsoundalsa.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libmanagement.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libmlib_image.so
/usr/java/jdk1.6.0_26/jre/lib/i386/libnative_chmod.so
/usr/java/jdk1.6.0_26/jre/lib/i386/libnative_chmod_g.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libnet.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libnio.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libnpjp2.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libnpt.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/librmi.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libsaproc.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libsplashscreen.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libunpack.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libverify.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/libzip.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/motif21
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/motif21/libmawt.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/native_threads
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/native_threads/libhpi.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/server
/usr/java/jdk1.6.0_26/jre/lib/i386/server/Xusage.txt
/usr/java/jdk1.6.0_26/jre/lib/i386/server/libjsig.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/server/libjvm.so
%dir /usr/java/jdk1.6.0_26/jre/lib/i386/xawt
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/i386/xawt/libmawt.so
%dir /usr/java/jdk1.6.0_26/jre/lib/im
/usr/java/jdk1.6.0_26/jre/lib/im/indicim.jar
/usr/java/jdk1.6.0_26/jre/lib/im/thaiim.jar
%dir /usr/java/jdk1.6.0_26/jre/lib/images
%dir /usr/java/jdk1.6.0_26/jre/lib/images/cursors
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/cursors.properties
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/invalid32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_CopyDrop32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_CopyNoDrop32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_LinkDrop32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_LinkNoDrop32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_MoveDrop32x32.gif
/usr/java/jdk1.6.0_26/jre/lib/images/cursors/motif_MoveNoDrop32x32.gif
%dir /usr/java/jdk1.6.0_26/jre/lib/images/icons
/usr/java/jdk1.6.0_26/jre/lib/images/icons/sun-java.png
/usr/java/jdk1.6.0_26/jre/lib/images/icons/sun-java_HighContrast.png
/usr/java/jdk1.6.0_26/jre/lib/images/icons/sun-java_HighContrastInverse.png
/usr/java/jdk1.6.0_26/jre/lib/images/icons/sun-java_LowContrast.png
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/javaws.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/javaws.pack
/usr/java/jdk1.6.0_26/jre/lib/jce.jar
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/lib/jexec
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/jsse.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/jsse.pack
/usr/java/jdk1.6.0_26/jre/lib/jvm.hprof.txt
%dir /usr/java/jdk1.6.0_26/jre/lib/locale
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/de
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/de/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/de/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/es
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/es/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/es/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/fr
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/fr/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/fr/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/it
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/it/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/it/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ja
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ja/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/ja/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ko
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ko.UTF-8
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ko.UTF-8/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/ko.UTF-8/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/ko/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/ko/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/sv
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/sv/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/sv/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh.GBK
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh.GBK/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/zh.GBK/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/zh/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_HK.BIG5HK
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_HK.BIG5HK/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/zh_HK.BIG5HK/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW.BIG5
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW.BIG5/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW.BIG5/LC_MESSAGES/sunw_java_plugin.mo
%dir /usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW/LC_MESSAGES
/usr/java/jdk1.6.0_26/jre/lib/locale/zh_TW/LC_MESSAGES/sunw_java_plugin.mo
/usr/java/jdk1.6.0_26/jre/lib/logging.properties
%dir /usr/java/jdk1.6.0_26/jre/lib/management
/usr/java/jdk1.6.0_26/jre/lib/management-agent.jar
/usr/java/jdk1.6.0_26/jre/lib/management/jmxremote.access
/usr/java/jdk1.6.0_26/jre/lib/management/jmxremote.password.template
/usr/java/jdk1.6.0_26/jre/lib/management/management.properties
/usr/java/jdk1.6.0_26/jre/lib/management/snmp.acl.template
/usr/java/jdk1.6.0_26/jre/lib/meta-index
/usr/java/jdk1.6.0_26/jre/lib/net.properties
%dir /usr/java/jdk1.6.0_26/jre/lib/oblique-fonts
/usr/java/jdk1.6.0_26/jre/lib/oblique-fonts/LucidaSansDemiOblique.ttf
/usr/java/jdk1.6.0_26/jre/lib/oblique-fonts/LucidaSansOblique.ttf
/usr/java/jdk1.6.0_26/jre/lib/oblique-fonts/LucidaTypewriterBoldOblique.ttf
/usr/java/jdk1.6.0_26/jre/lib/oblique-fonts/LucidaTypewriterOblique.ttf
/usr/java/jdk1.6.0_26/jre/lib/oblique-fonts/fonts.dir
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/plugin.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/plugin.pack
/usr/java/jdk1.6.0_26/jre/lib/psfont.properties.ja
/usr/java/jdk1.6.0_26/jre/lib/psfontj2d.properties
/usr/java/jdk1.6.0_26/jre/lib/resources.jar
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/jre/lib/rt.jar
%config(missingok) /usr/java/jdk1.6.0_26/jre/lib/rt.pack
%dir /usr/java/jdk1.6.0_26/jre/lib/security
/usr/java/jdk1.6.0_26/jre/lib/security/US_export_policy.jar
/usr/java/jdk1.6.0_26/jre/lib/security/blacklist
/usr/java/jdk1.6.0_26/jre/lib/security/cacerts
/usr/java/jdk1.6.0_26/jre/lib/security/java.policy
/usr/java/jdk1.6.0_26/jre/lib/security/java.security
/usr/java/jdk1.6.0_26/jre/lib/security/javaws.policy
/usr/java/jdk1.6.0_26/jre/lib/security/local_policy.jar
/usr/java/jdk1.6.0_26/jre/lib/security/trusted.libraries
%dir /usr/java/jdk1.6.0_26/jre/lib/servicetag
/usr/java/jdk1.6.0_26/jre/lib/servicetag/jdk_header.png
/usr/java/jdk1.6.0_26/jre/lib/sound.properties
%dir /usr/java/jdk1.6.0_26/jre/lib/zi
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Africa
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Abidjan
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Accra
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Addis_Ababa
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Algiers
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Asmara
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Bamako
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Bangui
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Banjul
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Bissau
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Blantyre
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Brazzaville
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Bujumbura
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Cairo
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Casablanca
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Ceuta
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Conakry
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Dakar
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Dar_es_Salaam
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Djibouti
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Douala
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/El_Aaiun
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Freetown
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Gaborone
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Harare
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Johannesburg
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Kampala
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Khartoum
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Kigali
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Kinshasa
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Lagos
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Libreville
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Lome
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Luanda
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Lubumbashi
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Lusaka
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Malabo
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Maputo
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Maseru
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Mbabane
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Mogadishu
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Monrovia
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Nairobi
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Ndjamena
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Niamey
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Nouakchott
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Ouagadougou
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Porto-Novo
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Sao_Tome
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Tripoli
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Tunis
/usr/java/jdk1.6.0_26/jre/lib/zi/Africa/Windhoek
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/America
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Adak
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Anchorage
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Anguilla
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Antigua
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Araguaina
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Buenos_Aires
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Catamarca
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Cordoba
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Jujuy
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/La_Rioja
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Mendoza
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Rio_Gallegos
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Salta
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/San_Juan
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/San_Luis
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Tucuman
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Argentina/Ushuaia
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Aruba
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Asuncion
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Atikokan
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Bahia
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Bahia_Banderas
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Barbados
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Belem
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Belize
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Blanc-Sablon
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Boa_Vista
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Bogota
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Boise
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Cambridge_Bay
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Campo_Grande
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Cancun
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Caracas
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Cayenne
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Cayman
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Chicago
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Chihuahua
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Costa_Rica
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Cuiaba
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Curacao
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Danmarkshavn
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Dawson
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Dawson_Creek
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Denver
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Detroit
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Dominica
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Edmonton
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Eirunepe
/usr/java/jdk1.6.0_26/jre/lib/zi/America/El_Salvador
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Fortaleza
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Glace_Bay
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Godthab
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Goose_Bay
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Grand_Turk
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Grenada
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Guadeloupe
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Guatemala
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Guayaquil
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Guyana
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Halifax
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Havana
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Hermosillo
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Indianapolis
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Knox
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Marengo
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Petersburg
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Tell_City
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Vevay
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Vincennes
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Indiana/Winamac
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Inuvik
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Iqaluit
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Jamaica
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Juneau
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/America/Kentucky
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Kentucky/Louisville
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Kentucky/Monticello
/usr/java/jdk1.6.0_26/jre/lib/zi/America/La_Paz
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Lima
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Los_Angeles
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Maceio
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Managua
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Manaus
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Martinique
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Matamoros
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Mazatlan
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Menominee
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Merida
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Metlakatla
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Mexico_City
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Miquelon
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Moncton
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Monterrey
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Montevideo
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Montreal
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Montserrat
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Nassau
/usr/java/jdk1.6.0_26/jre/lib/zi/America/New_York
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Nipigon
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Nome
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Noronha
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/America/North_Dakota
/usr/java/jdk1.6.0_26/jre/lib/zi/America/North_Dakota/Beulah
/usr/java/jdk1.6.0_26/jre/lib/zi/America/North_Dakota/Center
/usr/java/jdk1.6.0_26/jre/lib/zi/America/North_Dakota/New_Salem
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Ojinaga
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Panama
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Pangnirtung
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Paramaribo
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Phoenix
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Port-au-Prince
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Port_of_Spain
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Porto_Velho
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Puerto_Rico
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Rainy_River
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Rankin_Inlet
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Recife
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Regina
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Resolute
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Rio_Branco
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Santa_Isabel
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Santarem
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Santiago
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Santo_Domingo
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Sao_Paulo
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Scoresbysund
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Sitka
/usr/java/jdk1.6.0_26/jre/lib/zi/America/St_Johns
/usr/java/jdk1.6.0_26/jre/lib/zi/America/St_Kitts
/usr/java/jdk1.6.0_26/jre/lib/zi/America/St_Lucia
/usr/java/jdk1.6.0_26/jre/lib/zi/America/St_Thomas
/usr/java/jdk1.6.0_26/jre/lib/zi/America/St_Vincent
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Swift_Current
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Tegucigalpa
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Thule
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Thunder_Bay
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Tijuana
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Toronto
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Tortola
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Vancouver
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Whitehorse
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Winnipeg
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Yakutat
/usr/java/jdk1.6.0_26/jre/lib/zi/America/Yellowknife
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Casey
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Davis
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/DumontDUrville
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Macquarie
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Mawson
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/McMurdo
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Palmer
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Rothera
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Syowa
/usr/java/jdk1.6.0_26/jre/lib/zi/Antarctica/Vostok
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Asia
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Aden
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Almaty
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Amman
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Anadyr
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Aqtau
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Aqtobe
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Ashgabat
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Baghdad
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Bahrain
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Baku
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Bangkok
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Beirut
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Bishkek
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Brunei
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Choibalsan
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Chongqing
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Colombo
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Damascus
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Dhaka
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Dili
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Dubai
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Dushanbe
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Gaza
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Harbin
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Ho_Chi_Minh
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Hong_Kong
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Hovd
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Irkutsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Jakarta
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Jayapura
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Jerusalem
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kabul
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kamchatka
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Karachi
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kashgar
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kathmandu
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kolkata
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Krasnoyarsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kuala_Lumpur
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kuching
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Kuwait
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Macau
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Magadan
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Makassar
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Manila
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Muscat
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Nicosia
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Novokuznetsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Novosibirsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Omsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Oral
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Phnom_Penh
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Pontianak
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Pyongyang
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Qatar
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Qyzylorda
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Rangoon
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Riyadh
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Riyadh87
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Riyadh88
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Riyadh89
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Sakhalin
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Samarkand
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Seoul
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Shanghai
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Singapore
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Taipei
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Tashkent
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Tbilisi
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Tehran
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Thimphu
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Tokyo
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Ulaanbaatar
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Urumqi
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Vientiane
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Vladivostok
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Yakutsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Yekaterinburg
/usr/java/jdk1.6.0_26/jre/lib/zi/Asia/Yerevan
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Azores
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Bermuda
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Canary
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Cape_Verde
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Faroe
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Madeira
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Reykjavik
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/South_Georgia
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/St_Helena
/usr/java/jdk1.6.0_26/jre/lib/zi/Atlantic/Stanley
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Australia
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Adelaide
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Brisbane
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Broken_Hill
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Currie
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Darwin
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Eucla
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Hobart
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Lindeman
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Lord_Howe
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Melbourne
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Perth
/usr/java/jdk1.6.0_26/jre/lib/zi/Australia/Sydney
/usr/java/jdk1.6.0_26/jre/lib/zi/CET
/usr/java/jdk1.6.0_26/jre/lib/zi/CST6CDT
/usr/java/jdk1.6.0_26/jre/lib/zi/EET
/usr/java/jdk1.6.0_26/jre/lib/zi/EST
/usr/java/jdk1.6.0_26/jre/lib/zi/EST5EDT
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Etc
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+1
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+10
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+11
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+12
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+2
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+3
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+4
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+5
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+6
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+7
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+8
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT+9
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-1
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-10
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-11
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-12
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-13
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-14
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-2
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-3
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-4
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-5
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-6
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-7
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-8
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/GMT-9
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/UCT
/usr/java/jdk1.6.0_26/jre/lib/zi/Etc/UTC
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Europe
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Amsterdam
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Andorra
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Athens
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Belgrade
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Berlin
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Brussels
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Bucharest
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Budapest
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Chisinau
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Copenhagen
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Dublin
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Gibraltar
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Helsinki
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Istanbul
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Kaliningrad
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Kiev
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Lisbon
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/London
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Luxembourg
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Madrid
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Malta
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Minsk
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Monaco
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Moscow
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Oslo
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Paris
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Prague
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Riga
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Rome
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Samara
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Simferopol
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Sofia
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Stockholm
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Tallinn
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Tirane
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Uzhgorod
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Vaduz
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Vienna
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Vilnius
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Volgograd
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Warsaw
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Zaporozhye
/usr/java/jdk1.6.0_26/jre/lib/zi/Europe/Zurich
/usr/java/jdk1.6.0_26/jre/lib/zi/GMT
/usr/java/jdk1.6.0_26/jre/lib/zi/HST
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Indian
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Antananarivo
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Chagos
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Christmas
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Cocos
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Comoro
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Kerguelen
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Mahe
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Maldives
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Mauritius
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Mayotte
/usr/java/jdk1.6.0_26/jre/lib/zi/Indian/Reunion
/usr/java/jdk1.6.0_26/jre/lib/zi/MET
/usr/java/jdk1.6.0_26/jre/lib/zi/MST
/usr/java/jdk1.6.0_26/jre/lib/zi/MST7MDT
/usr/java/jdk1.6.0_26/jre/lib/zi/PST8PDT
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/Pacific
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Apia
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Auckland
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Chatham
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Chuuk
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Easter
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Efate
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Enderbury
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Fakaofo
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Fiji
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Funafuti
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Galapagos
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Gambier
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Guadalcanal
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Guam
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Honolulu
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Johnston
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Kiritimati
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Kosrae
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Kwajalein
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Majuro
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Marquesas
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Midway
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Nauru
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Niue
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Norfolk
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Noumea
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Pago_Pago
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Palau
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Pitcairn
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Pohnpei
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Port_Moresby
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Rarotonga
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Saipan
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Tahiti
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Tarawa
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Tongatapu
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Wake
/usr/java/jdk1.6.0_26/jre/lib/zi/Pacific/Wallis
%dir /usr/java/jdk1.6.0_26/jre/lib/zi/SystemV
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/AST4
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/AST4ADT
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/CST6
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/CST6CDT
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/EST5
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/EST5EDT
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/HST10
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/MST7
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/MST7MDT
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/PST8
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/PST8PDT
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/YST9
/usr/java/jdk1.6.0_26/jre/lib/zi/SystemV/YST9YDT
/usr/java/jdk1.6.0_26/jre/lib/zi/WET
/usr/java/jdk1.6.0_26/jre/lib/zi/ZoneInfoMappings
%dir /usr/java/jdk1.6.0_26/jre/plugin
%dir /usr/java/jdk1.6.0_26/jre/plugin/desktop
/usr/java/jdk1.6.0_26/jre/plugin/desktop/sun_java.desktop
/usr/java/jdk1.6.0_26/jre/plugin/desktop/sun_java.png
%dir /usr/java/jdk1.6.0_26/jre/plugin/i386
%dir /usr/java/jdk1.6.0_26/jre/plugin/i386/ns7
%dir /usr/java/jdk1.6.0_26/jre/plugin/i386/ns7-gcc29
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/plugin/i386/ns7-gcc29/libjavaplugin_oji.so
%attr(0755,root,root) /usr/java/jdk1.6.0_26/jre/plugin/i386/ns7/libjavaplugin_oji.so
%dir /usr/java/jdk1.6.0_26/lib
/usr/java/jdk1.6.0_26/lib/ct.sym
/usr/java/jdk1.6.0_26/lib/dt.jar
/usr/java/jdk1.6.0_26/lib/htmlconverter.jar
/usr/java/jdk1.6.0_26/lib/ir.idl
/usr/java/jdk1.6.0_26/lib/jconsole.jar
%attr(0755,root,root) /usr/java/jdk1.6.0_26/lib/jexec
/usr/java/jdk1.6.0_26/lib/orb.idl
/usr/java/jdk1.6.0_26/lib/sa-jdi.jar
%ghost %verify(group user mode rdev) /usr/java/jdk1.6.0_26/lib/tools.jar
%config(missingok) /usr/java/jdk1.6.0_26/lib/tools.pack
%dir /usr/java/jdk1.6.0_26/lib/visualvm
%dir /usr/java/jdk1.6.0_26/lib/visualvm/etc
/usr/java/jdk1.6.0_26/lib/visualvm/etc/visualvm.clusters
/usr/java/jdk1.6.0_26/lib/visualvm/etc/visualvm.conf
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform
/usr/java/jdk1.6.0_26/lib/visualvm/platform/.lastModified
/usr/java/jdk1.6.0_26/lib/visualvm/platform/VERSION.txt
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/config
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-netbeans-core.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-netbeans-modules-options-api.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-netbeans-modules-queries.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-execution.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-explorer.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-loaders.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-modules.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-text.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/ModuleAutoDeps/org-openide-util.xml
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-api-annotations-common.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-api-progress.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-api-visual.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-execution.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-io-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-multiview.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-output2.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core-windows.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-core.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-applemenu.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-autoupdate-services.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-autoupdate-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-core-kit.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-editor-mimelookup-impl.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-editor-mimelookup.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-favorites.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-javahelp.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-keyring-impl.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-keyring.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-masterfs.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-options-api.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-options-keymap.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-print.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-progress-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-queries.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-sendopts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-settings.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-modules-spi-actions.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-spi-quicksearch.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-swing-outline.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-swing-plaf.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-netbeans-swing-tabcontrol.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-actions.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-awt.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-compat.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-dialogs.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-execution.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-explorer.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-io.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-loaders.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-nodes.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-options.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-text.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-util-enumerations.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/config/Modules/org-openide-windows.xml
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/core
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/core.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/core/locale
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/locale/core_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/locale/core_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/locale/org-openide-filesystems_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/locale/org-openide-filesystems_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/core/org-openide-filesystems.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/docs
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/lib
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/boot.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/boot_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/boot_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-modules_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-modules_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-util-lookup_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-util-lookup_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-util_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/locale/org-openide-util_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/nbexec
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/org-openide-modules.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/org-openide-util-lookup.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/lib/org-openide-util.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/modules
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext/jh-2.0_05.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext/locale
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext/locale/updater_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext/locale/updater_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/ext/updater.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-annotations-common_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-annotations-common_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-progress_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-progress_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-visual_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-api-visual_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-execution_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-execution_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-io-ui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-io-ui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-multiview_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-multiview_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-output2_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-output2_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-ui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-ui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-windows_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core-windows_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-core_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-applemenu_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-applemenu_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-autoupdate-services_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-autoupdate-services_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-autoupdate-ui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-autoupdate-ui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-core-kit_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-core-kit_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-editor-mimelookup-impl_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-editor-mimelookup-impl_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-editor-mimelookup_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-editor-mimelookup_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-favorites_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-favorites_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-javahelp_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-javahelp_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-keyring-impl_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-keyring-impl_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-keyring_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-keyring_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-masterfs_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-masterfs_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-options-api_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-options-api_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-options-keymap_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-options-keymap_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-print_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-print_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-progress-ui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-progress-ui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-queries_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-queries_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-sendopts_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-sendopts_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-settings_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-settings_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-spi-actions_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-spi-actions_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-templates_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-modules-templates_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-spi-quicksearch_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-spi-quicksearch_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-outline_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-outline_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-plaf_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-plaf_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-tabcontrol_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-netbeans-swing-tabcontrol_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-actions_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-actions_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-awt_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-awt_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-compat_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-compat_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-dialogs_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-dialogs_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-execution_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-execution_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-explorer_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-explorer_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-io_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-io_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-loaders_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-loaders_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-nodes_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-nodes_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-options_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-options_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-text_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-text_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-util-enumerations_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-util-enumerations_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-windows_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/locale/org-openide-windows_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-api-annotations-common.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-api-progress.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-api-visual.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-execution.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-io-ui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-multiview.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-output2.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-ui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core-windows.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-core.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-applemenu.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-autoupdate-services.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-autoupdate-ui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-core-kit.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-editor-mimelookup-impl.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-editor-mimelookup.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-favorites.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-javahelp.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-keyring-impl.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-keyring.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-masterfs.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-options-api.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-options-keymap.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-print.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-progress-ui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-queries.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-sendopts.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-settings.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-modules-spi-actions.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-spi-quicksearch.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-swing-outline.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-swing-plaf.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-netbeans-swing-tabcontrol.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-actions.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-awt.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-compat.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-dialogs.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-execution.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-explorer.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-io.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-loaders.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-nodes.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-options.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-text.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-util-enumerations.jar
/usr/java/jdk1.6.0_26/lib/visualvm/platform/modules/org-openide-windows.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-api-annotations-common.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-api-progress.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-api-visual.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-bootstrap.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-execution.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-io-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-multiview.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-output2.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-startup.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core-windows.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-core.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-applemenu.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-autoupdate-services.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-autoupdate-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-core-kit.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-editor-mimelookup-impl.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-editor-mimelookup.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-favorites.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-javahelp.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-keyring-impl.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-keyring.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-masterfs.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-options-api.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-options-keymap.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-print.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-progress-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-queries.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-sendopts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-settings.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-modules-spi-actions.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-spi-quicksearch.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-swing-outline.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-swing-plaf.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-netbeans-swing-tabcontrol.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-actions.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-awt.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-compat.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-dialogs.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-execution.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-explorer.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-filesystems.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-io.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-loaders.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-modules.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-nodes.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-options.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-text.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-util-enumerations.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-util-lookup.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-util.xml
/usr/java/jdk1.6.0_26/lib/visualvm/platform/update_tracking/org-openide-windows.xml
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/.lastModified
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/VERSION.txt
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/config
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-lib-profiler-charts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-lib-profiler-common.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-lib-profiler-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-lib-profiler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-modules-profiler-oql.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/config/Modules/org-netbeans-modules-profiler.xml
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk15
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk15/linux
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk15/linux/libprofilerinterface.so
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk16
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk16/linux
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/deployed/jdk16/linux/libprofilerinterface.so
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/jfluid-server-15.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/jfluid-server.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/locale
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/locale/jfluid-server_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/lib/locale/jfluid-server_zh_CN.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-charts_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-charts_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-common_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-common_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-ui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler-ui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-lib-profiler_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-modules-profiler-oql_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-modules-profiler-oql_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-modules-profiler_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/locale/org-netbeans-modules-profiler_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-lib-profiler-charts.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-lib-profiler-common.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-lib-profiler-ui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-lib-profiler.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-modules-profiler-oql.jar
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/modules/org-netbeans-modules-profiler.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-lib-profiler-charts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-lib-profiler-common.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-lib-profiler-ui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-lib-profiler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-modules-profiler-oql.xml
/usr/java/jdk1.6.0_26/lib/visualvm/profiler/update_tracking/org-netbeans-modules-profiler.xml
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/.lastModified
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-api-caching.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-application-views.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-application.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-attach.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-charts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-core.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-coredump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-heapdump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-host-remote.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-host-views.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-host.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-jmx.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-jvm.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-jvmstat.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-modules-appui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-profiler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-profiling.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-sa.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-sampler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-threaddump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-tools.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/com-sun-tools-visualvm-uisupport.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-api-visual.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-core-execution.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-core-output2.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-modules-core-kit.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-modules-favorites.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-modules-options-keymap.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-netbeans-modules-spi-actions.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-openide-compat.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-openide-options.xml_hidden
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/config/Modules/org-openide-util-enumerations.xml_hidden
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core/com-sun-tools-visualvm-modules-startup.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core/locale
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core/locale/com-sun-tools-visualvm-modules-startup_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core/locale/com-sun-tools-visualvm-modules-startup_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/core/locale/core_visualvm.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-api-caching.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-application-views.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-application.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-attach.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-charts.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-core.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-coredump.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-heapdump.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-host-remote.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-host-views.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-host.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-jmx.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-jvm.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-jvmstat.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-modules-appui.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-profiler.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-profiling.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-sa.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-sampler.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-threaddump.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-tools.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/com-sun-tools-visualvm-uisupport.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-api-caching_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-api-caching_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-application-views_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-application-views_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-application_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-application_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-attach_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-attach_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-charts_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-charts_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-core_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-core_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-coredump_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-coredump_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-heapdump_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-heapdump_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host-remote_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host-remote_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host-views_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host-views_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-host_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jmx_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jmx_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jvm_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jvm_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jvmstat_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-jvmstat_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-modules-appui_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-modules-appui_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-profiler_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-profiler_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-profiling_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-profiling_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-sa_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-sa_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-sampler_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-sampler_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-threaddump_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-threaddump_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-tools_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-tools_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-uisupport_ja.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/com-sun-tools-visualvm-uisupport_zh_CN.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/org-netbeans-core-windows_visualvm.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/org-netbeans-core_visualvm.jar
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/modules/locale/org-netbeans-modules-profiler_visualvm.jar
%dir /usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-api-caching.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-application-views.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-application.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-attach.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-charts.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-core.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-coredump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-heapdump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-host-remote.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-host-views.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-host.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-jmx.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-jvm.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-jvmstat.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-modules-appui.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-modules-startup.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-profiler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-profiling.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-sa.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-sampler.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-threaddump.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-tools.xml
/usr/java/jdk1.6.0_26/lib/visualvm/visualvm/update_tracking/com-sun-tools-visualvm-uisupport.xml
%dir /usr/java/jdk1.6.0_26/man
/usr/java/jdk1.6.0_26/man/ja
%dir /usr/java/jdk1.6.0_26/man/ja_JP.eucJP
%dir /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/appletviewer.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/apt.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/extcheck.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/idlj.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jar.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jarsigner.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/java.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/javac.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/javadoc.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/javah.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/javap.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/javaws.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jconsole.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jdb.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jhat.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jinfo.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jmap.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jps.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jrunscript.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jsadebugd.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jstack.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jstat.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jstatd.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/jvisualvm.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/keytool.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/native2ascii.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/orbd.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/pack200.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/policytool.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/rmic.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/rmid.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/rmiregistry.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/schemagen.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/serialver.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/servertool.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/tnameserv.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/unpack200.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/wsgen.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/wsimport.1
%doc /usr/java/jdk1.6.0_26/man/ja_JP.eucJP/man1/xjc.1
%dir /usr/java/jdk1.6.0_26/man/man1
%doc /usr/java/jdk1.6.0_26/man/man1/appletviewer.1
%doc /usr/java/jdk1.6.0_26/man/man1/apt.1
%doc /usr/java/jdk1.6.0_26/man/man1/extcheck.1
%doc /usr/java/jdk1.6.0_26/man/man1/idlj.1
%doc /usr/java/jdk1.6.0_26/man/man1/jar.1
%doc /usr/java/jdk1.6.0_26/man/man1/jarsigner.1
%doc /usr/java/jdk1.6.0_26/man/man1/java.1
%doc /usr/java/jdk1.6.0_26/man/man1/javac.1
%doc /usr/java/jdk1.6.0_26/man/man1/javadoc.1
%doc /usr/java/jdk1.6.0_26/man/man1/javah.1
%doc /usr/java/jdk1.6.0_26/man/man1/javap.1
%doc /usr/java/jdk1.6.0_26/man/man1/javaws.1
%doc /usr/java/jdk1.6.0_26/man/man1/jconsole.1
%doc /usr/java/jdk1.6.0_26/man/man1/jdb.1
%doc /usr/java/jdk1.6.0_26/man/man1/jhat.1
%doc /usr/java/jdk1.6.0_26/man/man1/jinfo.1
%doc /usr/java/jdk1.6.0_26/man/man1/jmap.1
%doc /usr/java/jdk1.6.0_26/man/man1/jps.1
%doc /usr/java/jdk1.6.0_26/man/man1/jrunscript.1
%doc /usr/java/jdk1.6.0_26/man/man1/jsadebugd.1
%doc /usr/java/jdk1.6.0_26/man/man1/jstack.1
%doc /usr/java/jdk1.6.0_26/man/man1/jstat.1
%doc /usr/java/jdk1.6.0_26/man/man1/jstatd.1
%doc /usr/java/jdk1.6.0_26/man/man1/jvisualvm.1
%doc /usr/java/jdk1.6.0_26/man/man1/keytool.1
%doc /usr/java/jdk1.6.0_26/man/man1/native2ascii.1
%doc /usr/java/jdk1.6.0_26/man/man1/orbd.1
%doc /usr/java/jdk1.6.0_26/man/man1/pack200.1
%doc /usr/java/jdk1.6.0_26/man/man1/policytool.1
%doc /usr/java/jdk1.6.0_26/man/man1/rmic.1
%doc /usr/java/jdk1.6.0_26/man/man1/rmid.1
%doc /usr/java/jdk1.6.0_26/man/man1/rmiregistry.1
%doc /usr/java/jdk1.6.0_26/man/man1/schemagen.1
%doc /usr/java/jdk1.6.0_26/man/man1/serialver.1
%doc /usr/java/jdk1.6.0_26/man/man1/servertool.1
%doc /usr/java/jdk1.6.0_26/man/man1/tnameserv.1
%doc /usr/java/jdk1.6.0_26/man/man1/unpack200.1
%doc /usr/java/jdk1.6.0_26/man/man1/wsgen.1
%doc /usr/java/jdk1.6.0_26/man/man1/wsimport.1
%doc /usr/java/jdk1.6.0_26/man/man1/xjc.1
%dir /usr/java/jdk1.6.0_26/sample
%dir /usr/java/jdk1.6.0_26/sample/javac
%dir /usr/java/jdk1.6.0_26/sample/javac/processing
%dir /usr/java/jdk1.6.0_26/sample/javac/processing/src
/usr/java/jdk1.6.0_26/sample/javac/processing/src/CheckNamesProcessor.java
%dir /usr/java/jdk1.6.0_26/sample/jmx
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/build.properties
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/build.xml
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/connect-local-ant-run.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/connect-local-java-jar.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/connect-local.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/remote-connection-failed.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/remote-connection.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/scandir-config.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/scandir-result.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/scandir-start.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/docfiles/scandir-start2.jpg
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/index.html
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/keystore
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/logging.properties
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/manifest.mf
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/nbproject
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/DirectoryScanner.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/DirectoryScannerMXBean.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ResultLogManager.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ResultLogManagerMXBean.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirAgent.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirClient.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirConfig.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanDirConfigMXBean.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanManager.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/ScanManagerMXBean.java
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/DirectoryScannerConfig.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/FileMatch.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ResultLogConfig.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ResultRecord.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/ScanManagerConfig.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/XmlConfigUtils.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/config/package.html
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/com/sun/jmx/examples/scandir/package.html
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/etc
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/etc/access.properties
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/etc/management.properties
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/etc/password.properties
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/src/etc/testconfig.xml
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/DirectoryScannerTest.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/ScanDirConfigTest.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/ScanManagerTest.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/TestUtils.java
%dir /usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/config
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/test/com/sun/jmx/examples/scandir/config/XmlConfigUtilsTest.java
/usr/java/jdk1.6.0_26/sample/jmx/jmx-scandir/truststore
%dir /usr/java/jdk1.6.0_26/sample/jnlp
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba
/usr/java/jdk1.6.0_26/sample/jnlp/corba/GNUmakefile
/usr/java/jdk1.6.0_26/sample/jnlp/corba/README
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/src
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/src/core
/usr/java/jdk1.6.0_26/sample/jnlp/corba/src/core/HelloClient.java
/usr/java/jdk1.6.0_26/sample/jnlp/corba/src/core/HelloServer.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/src/stubs
/usr/java/jdk1.6.0_26/sample/jnlp/corba/src/stubs/HelloImpl.java
/usr/java/jdk1.6.0_26/sample/jnlp/corba/src/stubs/HelloInterface.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/war
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/war/WEB-INF
/usr/java/jdk1.6.0_26/sample/jnlp/corba/war/WEB-INF/web.xml
%dir /usr/java/jdk1.6.0_26/sample/jnlp/corba/war/app
/usr/java/jdk1.6.0_26/sample/jnlp/corba/war/app/helloworld.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/corba/war/index.html
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/README
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/GNUmakefile
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/j2re1_4_2
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/j2re1_4_2/GNUmakefile
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/resources
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/resources/javaws-1_0_1-j2re-1_4_2-linux-i586.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/jreinstallers/resources/version.xml_linux-i586_1.4.2
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/minclude
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/linux/minclude/linux.defs
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share/Platform.gmk
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share/jreinstallers
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share/jreinstallers/bundle.unix.gmk
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share/jreinstallers/components.gmk
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/share/jreinstallers/installer.gmk
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/GNUmakefile
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/j2re1_4_2
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/j2re1_4_2/GNUmakefile
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/resources
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/resources/javaws-1_0_1-j2re-1_4_2-solaris-sparc.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/jreinstallers/resources/version.xml_solaris-sparc_1.4.2
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/minclude
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/solaris/minclude/solaris.defs
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/GNUmakefile
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/bundle.win.gmk
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/j2re1_4_2
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/j2re1_4_2/GNUmakefile
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/resources
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/resources/javaws-1_0_1-j2re-1_4_2-windows-i586.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/jreinstallers/resources/version.xml_windows-i586_1.4.2
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/minclude
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/build/win32/minclude/windows.defs
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/Config.java
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/Main.java
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/SolarisInstaller.java
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/WinRegistry.java
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/WindowsInstaller.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_de.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_es.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_fr.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_it.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_ja.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_ko.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_pt_BR.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_sv.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_zh_CN.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/strings_zh_TW.properties
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/share/classes/jnlp/sample/JreInstaller/resources/sunlogo.png
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/win32
%dir /usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/win32/jreinstallers
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/win32/jreinstallers/WindowsInstaller.c
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/win32/jreinstallers/registry.cpp
/usr/java/jdk1.6.0_26/sample/jnlp/jreinstaller/src/win32/jreinstallers/versionChecker.c
%dir /usr/java/jdk1.6.0_26/sample/jnlp/raf
/usr/java/jdk1.6.0_26/sample/jnlp/raf/GNUmakefile
/usr/java/jdk1.6.0_26/sample/jnlp/raf/README
%dir /usr/java/jdk1.6.0_26/sample/jnlp/raf/src
/usr/java/jdk1.6.0_26/sample/jnlp/raf/src/randomFile.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/raf/war
%dir /usr/java/jdk1.6.0_26/sample/jnlp/raf/war/WEB-INF
/usr/java/jdk1.6.0_26/sample/jnlp/raf/war/WEB-INF/web.xml
%dir /usr/java/jdk1.6.0_26/sample/jnlp/raf/war/app
/usr/java/jdk1.6.0_26/sample/jnlp/raf/war/app/randomFile.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/raf/war/index.html
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/GNUmakefile
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/README
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/jardiff.jar
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/jnlp-servlet.jar
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/jnlp.jar
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/JarDiff.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/JarDiffConstants.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/JarDiffPatcher.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/Patcher.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/resources
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/jardiff/resources/strings.properties
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/DownloadRequest.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/DownloadResponse.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/ErrorResponseException.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/JarDiffHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/JnlpDownloadServlet.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/JnlpFileHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/JnlpResource.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/Logger.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/ResourceCatalog.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/XMLAttribute.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/XMLNode.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/XMLParsing.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/resources
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/servlet/resources/strings.properties
%dir /usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/util
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/util/VersionID.java
/usr/java/jdk1.6.0_26/sample/jnlp/servlet/src/classes/jnlp/sample/util/VersionString.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/GNUmakefile
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/README
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/src
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/servlet
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/servlet/TxtServlet.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/AboutAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/ClipboardHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/CopyAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/CutAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/ExitAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/FileHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/HelpAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/HelpHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/JLFAbstractAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/OpenAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/PasteAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/PrintAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/PublishAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/SaveAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/SaveAsAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/ShowAction.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/WebHandler.java
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/src/version1/WebPad.java
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/war
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/WEB-INF
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/WEB-INF/web.xml
%dir /usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/README
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/holidays__V1.0.jar
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/javahelp.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/jhcore__V1.0.jar
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/jlfgr__V1.0.jar
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/version.xml
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/app/webpad.jnlp
/usr/java/jdk1.6.0_26/sample/jnlp/webpad/war/index.html
%dir /usr/java/jdk1.6.0_26/sample/nbproject
/usr/java/jdk1.6.0_26/sample/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/sample/nio
%dir /usr/java/jdk1.6.0_26/sample/nio/server
/usr/java/jdk1.6.0_26/sample/nio/server/AcceptHandler.java
/usr/java/jdk1.6.0_26/sample/nio/server/Acceptor.java
/usr/java/jdk1.6.0_26/sample/nio/server/B1.java
/usr/java/jdk1.6.0_26/sample/nio/server/BN.java
/usr/java/jdk1.6.0_26/sample/nio/server/BP.java
/usr/java/jdk1.6.0_26/sample/nio/server/ChannelIO.java
/usr/java/jdk1.6.0_26/sample/nio/server/ChannelIOSecure.java
/usr/java/jdk1.6.0_26/sample/nio/server/Content.java
/usr/java/jdk1.6.0_26/sample/nio/server/Dispatcher.java
/usr/java/jdk1.6.0_26/sample/nio/server/Dispatcher1.java
/usr/java/jdk1.6.0_26/sample/nio/server/DispatcherN.java
/usr/java/jdk1.6.0_26/sample/nio/server/FileContent.java
/usr/java/jdk1.6.0_26/sample/nio/server/Handler.java
/usr/java/jdk1.6.0_26/sample/nio/server/MalformedRequestException.java
/usr/java/jdk1.6.0_26/sample/nio/server/N1.java
/usr/java/jdk1.6.0_26/sample/nio/server/N2.java
/usr/java/jdk1.6.0_26/sample/nio/server/README.txt
/usr/java/jdk1.6.0_26/sample/nio/server/Reply.java
/usr/java/jdk1.6.0_26/sample/nio/server/Request.java
/usr/java/jdk1.6.0_26/sample/nio/server/RequestHandler.java
/usr/java/jdk1.6.0_26/sample/nio/server/RequestServicer.java
/usr/java/jdk1.6.0_26/sample/nio/server/Sendable.java
/usr/java/jdk1.6.0_26/sample/nio/server/Server.java
/usr/java/jdk1.6.0_26/sample/nio/server/StringContent.java
/usr/java/jdk1.6.0_26/sample/nio/server/URLDumper.java
%dir /usr/java/jdk1.6.0_26/sample/scripting
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/README.txt
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/build.properties
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/build.xml
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/nbproject
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/META-INF
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/META-INF/manifest.mf
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/com
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/com/sun
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/com/sun/sample
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/com/sun/sample/scriptpad
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/com/sun/sample/scriptpad/Main.java
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources/Main.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources/conc.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources/gui.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources/mm.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/resources/scriptpad.js
%dir /usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/README.txt
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/browse.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/insertfile.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/linewrap.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/mail.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/memmonitor.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/memory.bat
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/memory.js
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/memory.sh
/usr/java/jdk1.6.0_26/sample/scripting/scriptpad/src/scripts/textcolor.js
%dir /usr/java/jdk1.6.0_26/sample/webservices
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/build.properties
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/build.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/eBaySvc.wsdl
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/ebay.properties
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/index.html
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/jax-ws-catalog.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/manifest.mf
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient/nbproject
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay/client
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay/client/MainGUIApp.java
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay/client/ViewItemDetails.java
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay/client/handler
/usr/java/jdk1.6.0_26/sample/webservices/EbayClient/src/ebay/client/handler/RequesterCredentials.java
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/build.properties
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/build.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/eBaySvc.wsdl
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer/images
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/images/8d_2.jpg
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/images/Sun_Fire_E20K_Server.jpg
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/images/sun_blade_1000_h400px.jpg
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/index.html
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/manifest.mf
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer/nbproject
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/nbproject/file-targets.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/nbproject/jdk.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/nbproject/netbeans-targets.xml
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/nbproject/project.xml
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src/ebay
%dir /usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src/ebay/server
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src/ebay/server/Ebay.java
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src/ebay/server/ImageProvider.java
/usr/java/jdk1.6.0_26/sample/webservices/EbayServer/src/ebay/server/Main.java
/usr/java/jdk1.6.0_26/src.zip




%post -p /bin/sh
#
    # Make sure any new files are created with a secure access mask.  Do not use
    # chmod, since that would also change the rights of any existing files, and
    # we are only interested in setting the rights for new files.
    #
    umask 022

    #
    # The package assumes that Gnome is either installed, or going to be
    # installed, so if nothing currently exists, then install in the default
    # location.
    #
    # NOTE: These variables must be defined before all the shell function macros
    #       are included.
    #
    if [ -z "${GNOMEDIR}" ]; then
        GNOMEDIR=/usr
    fi

    #
    # RPM_INSTALL_PREFIX doesn't seem to be set by "alien" so the following
    # minor kludge allows some functionality on debian-like systems (such
    # a Ubuntu) which don't support packages.
    #
    if [ -z "${RPM_INSTALL_PREFIX}" ]; then
	RPM_INSTALL_PREFIX="/usr/java"
    fi

    #
    # Gross kludge for old SuSE distros: Even though they set the environment
    # variable GNOMEDIR to /opt/gnome, Gnome may really be in /opt/gnome2.
    # Go figure,... (I feel so unclean....)
    #
    if [ "${GNOMEDIR}" = "/opt/gnome" ] && [ -d "/opt/gnome2" ]; then
	GNOMEDIR="/opt/gnome2"
    fi

    INSTALL_JRE_PATH=${RPM_INSTALL_PREFIX}/jdk1.6.0_26
    if [ -e ${INSTALL_JRE_PATH}/jre/bin/java ]; then
	INSTALL_JRE_PATH=${INSTALL_JRE_PATH}/jre
    fi

    #
    # Add the shell function and related variables used by the post-install.
    #
    ERROR_MISSING_PARAM=1000
ERROR_MISSING_PACKED_JAR=1001
ERROR_BAD_PARAM=1002
ERROR_MISSING_UNPACK200=1003
unpack_jars() {
    status=0
    if [ $# -lt 3 ]; then
        printf "Error: usage - no packed files specified, nothing to do:\n\n" \
								>> /dev/stderr
        printf "\t unpack_jars\n" "$*"                          >> /dev/stderr
        status=${ERROR_MISSING_PARAM}
    else
        unpack200=$1
        root=$2
        shift 2
        if [ -f ${unpack200} ]; then
            if [ -d ${root} ]; then                
                printf "Unpacking JAR files...\n"
                for file in $*; do
                    pack_file=`basename ${file} .jar`.pack
                    pack_src=${root}/`dirname ${file}`/${pack_file}
                    jar_dest=${root}/${file}
                    printf "\t%s...\n" "`basename ${file}`"
                    ${unpack200} ${pack_src} ${jar_dest}
                    if [ ! -f ${jar_dest} ]; then
                        printf "Error: unpack could not create JAR file:\n\n" \
								>> /dev/stderr
                        printf "\t%s\n\n" "${jar_dest}"		>> /dev/stderr
                        printf "Please refer to the "		>> /dev/stderr
			printf "Troubleshooting section of "    >> /dev/stderr
                        printf "the Installation "              >> /dev/stderr
                        printf "Instructions\n"                 >> /dev/stderr
                        printf "on the download page.\n"        >> /dev/stderr
                        status=${ERROR_MISSING_PACKED_JAR}
                    fi
                    rm -f ${pack_src}
                done
            else
                printf "Error: usage - the base path for the "  >> /dev/stderr
                printf "packed JAR files is invalid:\n\n"	>> /dev/stderr
                printf "\tunpack_jars %s\n" "$*"		>> /dev/stderr
                status=${ERROR_BAD_PARAM}
            fi
        else
            printf "Error: unpack200 - command could not be found.\n\n" \
								>> /dev/stderr
            printf "Please refer to the Troubleshooting "       >> /dev/stderr
            printf "section of the"                             >> /dev/stderr
            printf "Installation Instructions\n"                >> /dev/stderr
            printf "on the download page.\n"                    >> /dev/stderr
            status=${ERROR_MISSING_UNPACK200}
        fi
    fi
    return ${status}
}
    NS_COMMENT1="#--Netscape Communications Corporation MIME Information"
NS_COMMENT2="#Do not delete the above line. It is used to identify the file type."
NS_COMMENT3="#mime types added by Netscape Helper"
UpdateMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    command="$3"
    if [ -z "`grep -E \"^${mime_type}; ${command}$\" \"${mailcap_file}\" 2> /dev/null`" ]; then
        mc_comment="# Java Web Start"
        mc_text=
        if [ -w "${mailcap_file}" ]; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
        fi
        if [ -w "`dirname \"${mailcap_file}\"`" ]; then
            mc_text="${mc_text:+${mc_text}\n}${mime_type}; ${command}"
            printf "%s" "${mc_text}" > "${mailcap_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mailcap_file}"
            echo "Check permissions."
        fi
    fi
}
RemoveMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    mc_comment="# Java Web Start"
    if [ -w "${mailcap_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mailcap_file}\"`" ] ; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
            if [ `echo "${mc_text}" | tr -d '[:space:]' | wc -c` -gt 0 ]; then
                echo "${mc_text}" > "${mailcap_file}"
            else
                rm -f "${mailcap_file}"
            fi
        fi
    fi
}
UpdateMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    desc="$3"
    shift 3
    exts="$*"
    JNLP_ENTRY="type=${mime_type} desc=\"${desc}\" exts=\"${exts}\""
    if [ ! -w "${mime_file}" ]; then
        if [ -w `dirname ${mime_file}` ]; then
            echo "${NS_COMMENT1}"  > "${mime_file}"
            echo "${NS_COMMENT2}" >> "${mime_file}"
            echo "${NS_COMMENT3}" >> "${mime_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mime_file}"
            echo "Check permissions."
            return
        fi
    fi
    if [ -z "`grep -E \"^[^#]*${mime_type}\" \"${mime_file}\"`" ]; then
        echo ${JNLP_ENTRY} >> "${mime_file}"
    fi
}
RemoveMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    if [ -w "${mime_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mime_file}\"`" ]; then
            regexp="(${mime_type})|(^${NS_COMMENT1}$)|(^${NS_COMMENT2}$)|(^${NS_COMMENT3}$)"
            if [ `grep -Ev "${regexp}" "${mime_file}" | \
                 tr -d '[:space:]' | wc -c` -gt 0 ]
            then
                mt_text="`grep -v \"${mime_type}\" \"${mime_file}\"`"
                echo "${mt_text}" > "${mime_file}"
            else
                rm -f "${mime_file}"
            fi
        fi
    fi
}
    JDK_DESKTOP="${INSTALL_JRE_PATH}/lib/desktop"
JDK_ICONS="${JDK_DESKTOP}/icons"
JDK_APPS="${JDK_DESKTOP}/applications"
JDK_MIME="${JDK_DESKTOP}/mime"
SHARE_PATH="${GNOMEDIR}/share"
SHARE_ICONS="${SHARE_PATH}/icons"
SHARE_MIME="${SHARE_PATH}/mime"
SHARE_APPS="${SHARE_PATH}/applications"
HICOLOR=hicolor
HIGHCONTRAST=HighContrast
HIGHCONTRASTINVERSE=HighContrastInverse
LOWCONTRAST=LowContrast
THEMES="${HICOLOR} ${HIGHCONTRAST} ${HIGHCONTRASTINVERSE} ${LOWCONTRAST}"
RESOLUTIONS="16x16 48x48"
TEXT_ICON="gnome-mime-text-x-java.png"
JAR_ICON="gnome-mime-application-x-java-archive.png"
JNLP_ICON="gnome-mime-application-x-java-jnlp-file.png"
JAVA_ICON="sun-java.png"
JAVAWS_ICON="sun-javaws.png"
JCONTROL_ICON="sun-jcontrol.png"
APPS_ICONS="${JAVA_ICON} ${JAVAWS_ICON} ${JCONTROL_ICON}"
MIME_ICONS="${TEXT_ICON} ${JAR_ICON} ${JNLP_ICON}"
ICONS="${APPS_ICONS} ${MIME_ICONS}"
GNOME_UTILS_DIRS="/usr/bin /opt/gnome/bin"
UPDATE_MIME_DATABASE="update-mime-database"
UPDATE_DESKTOP_DATABASE="update-desktop-database"
GTK_UPDATE_ICON_CACHE="gtk-update-icon-cache"
SHARE_CONTROL_CENTER="${SHARE_PATH}/control-center-2.0"
SHARE_CAPPLETS="${SHARE_CONTROL_CENTER}/capplets"
SHARE_MIME_INFO="${SHARE_PATH}/mime-info"
SHARE_APP_REGISTRY="${SHARE_PATH}/application-registry"
SHARE_PIXMAPS="${SHARE_PATH}/pixmaps"
UpdateIconCache() {
    _icon_theme_root=$1
    if [ -f ${_icon_theme_root}/icon-theme.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${GTK_UPDATE_ICON_CACHE} ]; then
		${_dir}/${GTK_UPDATE_ICON_CACHE} ${_icon_theme_root} \
		    > /dev/null 2>&1
		break
	    fi
	done
	touch ${_icon_theme_root}
	for _dir in ${RESOLUTIONS}; do
	    if [ -d ${_icon_theme_root}/${_dir} ]; then
		touch ${_icon_theme_root}/${_dir}
	    fi
        done
    fi
}
UpdateDesktopDatabase() {
    _desktop_root=$1
    if [ -f ${_desktop_root}/mimeinfo.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_DESKTOP_DATABASE} ]; then
		${_dir}/${UPDATE_DESKTOP_DATABASE} ${_desktop_root} \
		   > /dev/null 2>&1
		break
	    fi
	done
    fi
}
UpdateMimeDatabase() {
    _mime_root=$1
    if [ -d ${_mime_root}/packages ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_MIME_DATABASE} ]; then
		${_dir}/${UPDATE_MIME_DATABASE} ${_mime_root} > /dev/null 2>&1
		break
	    fi
	done
    fi
}
InstallGnomeIcons() {
    for _theme in ${THEMES}; do
	if [ -d ${SHARE_ICONS}/${_theme} ]; then
	    for _res in ${RESOLUTIONS}; do
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/apps
		for _icon in ${APPS_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/apps/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
		done
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/mimetypes
		for _icon in ${MIME_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/mimetypes/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
		done
	    done
	    UpdateIconCache ${SHARE_ICONS}/${_theme}
	fi
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    cp -f ${JDK_ICONS}/${HICOLOR}/48x48/apps/${_icon} \
		  ${SHARE_PIXMAPS}/${_icon}
	done
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${TEXT_ICON} \
	      ${SHARE_PIXMAPS}/x-java.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JAR_ICON} \
	      ${SHARE_PIXMAPS}/x-java-archive.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JNLP_ICON} \
	      ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
RemoveGnomeIcons() {
    for _theme in ${THEMES}; do
	for _res in ${RESOLUTIONS}; do
	    for _icon in ${APPS_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
	    done
	    for _icon in ${MIME_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
	    done
	done
	UpdateIconCache ${SHARE_ICONS}/${_theme}
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    rm -f ${SHARE_PIXMAPS}/${_icon}
	done
	rm -f ${SHARE_PIXMAPS}/x-java.png
	rm -f ${SHARE_PIXMAPS}/x-java-archive.png
	rm -f ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
InstallGnomeDesktop() {
    _file=$1
    mkdir -p ${SHARE_APPS}
    cp -f ${JDK_APPS}/${_file} ${SHARE_APPS}/${_file}
    if [ "${_file}" = "sun_java.desktop" ]; then
	if [ -d ${SHARE_CAPPLETS} ]; then
	    cp -f ${JDK_APPS}/${_file} ${SHARE_CAPPLETS}/${_file}
	fi
    fi
}
RemoveGnomeDesktop() {
    _file=$1
    rm -f ${SHARE_APPS}/${_file}
    rm -f ${SHARE_CAPPLETS}/${_file}
}
InstallLegacyMimetype() {
    _mime_type=$1
    _extension=$2
    _name=$3
    _command=$4
    _icon=$5
    _description=$6
    cat <<- end_of_keys_file > ${SHARE_MIME_INFO}/${_name}.keys
	${_mime_type}:
	    description=${_description}
	    icon_filename=${_icon}
	    default_action_type=application
	    default_application_id=${_name}
	    short_list_application_user_additions=${_name}
	end_of_keys_file
    cat <<- end_of_mime_file > ${SHARE_MIME_INFO}/${_name}.mime
	${_mime_type}
	    ext: ${_extension}
	end_of_mime_file
    cat <<- end_of_apps_file > ${SHARE_APP_REGISTRY}/${_name}.applications
	${_name}
	    command=${_command}
	    name=${_name}
	    can_open_multiple_files=false
	    requires_terminal=false
	    mime_types=${_mime_type}
	end_of_apps_file
}
RemoveLegacyMimetype() {
    _name=$1
    rm -f ${SHARE_MIME_INFO}/${_name}.keys
    rm -f ${SHARE_MIME_INFO}/${_name}.mime
    rm -f ${SHARE_APP_REGISTRY}/${_name}.applications
}
InstallGnomeMimetypes() {
    if [ -d ${SHARE_MIME} ]; then
	cp -f ${JDK_MIME}/packages/x-java-archive.xml \
	      ${SHARE_MIME}/packages/x-java-archive.xml
	cp -f ${JDK_MIME}/packages/x-java-jnlp-file.xml \
	      ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    fi
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	mkdir -p ${SHARE_MIME_INFO}
	mkdir -p ${SHARE_APP_REGISTRY}
	InstallLegacyMimetype application/x-java-archive \
                 jar              \
                 java-archive     \
                 "java -jar"      \
                 x-java-archive.png     \
		 "Java Archive"
	InstallLegacyMimetype application/x-java-jnlp-file \
                 jnlp                \
                 java-web-start      \
                 javaws              \
                 x-java-jnlp-file.png        \
                 "Java Web Start Application"
    fi
}
RemoveGnomeMimetypes() {
    rm -f ${SHARE_MIME}/packages/x-java-archive.xml
    rm -f ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	RemoveLegacyMimetype java-archive
	RemoveLegacyMimetype java-web-start
    fi
}
IntegrateWithGnome() {
    InstallGnomeIcons
    InstallGnomeDesktop sun_java.desktop
    InstallGnomeDesktop sun-java.desktop
    InstallGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    InstallGnomeMimetypes
}
DisintegrateWithGnome() {
    RemoveGnomeIcons
    RemoveGnomeDesktop sun_java.desktop
    RemoveGnomeDesktop sun-java.desktop
    RemoveGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    RemoveGnomeMimetypes
}
    MOST_DIGITS="[1-9]"
ALL_DIGITS="[0-9]"
COUNTING_NUMBER="${MOST_DIGITS}${ALL_DIGITS}*\|0"
VALID_NON_NUMERIC="[-_.a-zA-Z]"
VALID_CHARS="[-_.a-zA-Z0-9]"
MAJOR_RULE="\(${MOST_DIGITS}${ALL_DIGITS}*\)"
MINOR_RULE="\(${COUNTING_NUMBER}\)"
MICRO_RULE="\(${COUNTING_NUMBER}\)"
UPDATE_RULE="\(${MOST_DIGITS}${ALL_DIGITS}\|0${ALL_DIGITS}\)"
NON_FCS_ID_RULE="\([a-zA-Z0-9]*\)"
MIN_VERSION_ID_RULE="${MAJOR_RULE}\.${MINOR_RULE}\.${MICRO_RULE}"
FCS_VERSION_ID_RULE="${MIN_VERSION_ID_RULE}\(_${UPDATE_RULE}\)\?"
VERSION_ID_RULE="${FCS_VERSION_ID_RULE}\(-${NON_FCS_ID_RULE}\)\?"
NAME_ID_RULE="${VALID_CHARS}*${VALID_NON_NUMERIC}"
KNOWN_GOOD_NAME_LIST="java jdk jre j2sdk j2re"
PRS_ERROR_BAD_PARAMS=2000
expand_version() {
    status=0
    if [ $# -eq 0 ]; then
        read release remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${release}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${release}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        release=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        \printf "\t expand_version\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        format="%d\t%d\t%d\t%d\n"
        echo ${release} | sed -e "s/_/\./g" | \
          awk -v format="${format}" 'BEGIN { FS = "." } { printf format, $1, $2, $3, $4 }'
    fi
    return ${status}
}
parse_release() {
    status=0
    if [ $# -eq 0 ]; then
        read string remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${string}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${string}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        string=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t parse_release %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        version_id=`expr "${string}" : "${NAME_ID_RULE}\(${VERSION_ID_RULE}\)\$"`
        if [ -n "${version_id}" ]; then
            name_id=`expr "${string}" : "\(${NAME_ID_RULE}\)${VERSION_ID_RULE}\$"`
            fcs_part=`expr "${string}" : "${NAME_ID_RULE}\(${FCS_VERSION_ID_RULE}\).*\$"`
            non_fcs_part=`expr "${version_id}" : "[^-]*-\(${NON_FCS_ID_RULE}\)\$"`
	    printf "%s\t%s\t%s\n" "${name_id}" "${fcs_part}" "${non_fcs_part}"
        fi
    fi
    return ${status}
}
UNKNOWN_NAME_WEIGHT=1000
get_name_weight() {
    status=0
    if [ "$1" = "-" ]; then
        read name good_names
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        else
            shift 1
            if [ $# -gt 0 ]; then
                good_names="$*"
            fi
            if [ -z "${name}" ]; then
                printf "Error: usage - function requires input!\n" >> /dev/stderr
                status=${PRS_ERROR_BAD_PARAMS}
            fi
        fi
    elif [ $# -gt 1 ]; then
        name=$1
        shift 1
        good_names="$*"
    else
        printf "Error: usage - function takes 2+ parameters:\n\n" >> /dev/stderr
        printf "\t get_name_weight %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -n "${good_names}" ]; then
            length=`expr length "${good_names}"`
            pos=`expr "${good_names}" : ".*\<${name}\>"`
            if [ ${pos} -gt 0 ]; then
                expr substr "${good_names}" 1 ${pos} | wc -w | tr -d "[:space:]"
            else
                echo ${UNKNOWN_NAME_WEIGHT}
            fi
        else
            echo ${UNKNOWN_NAME_WEIGHT}
        fi
    fi
    return ${status}
}
HAS_FCS_WEIGHT=0
HAS_ODD_FCS_WEIGHT=1
HAS_RC_WEIGHT=100
HAS_ODD_RC_WEIGHT=101
HAS_BETA_WEIGHT=300
HAS_ODD_BETA_WEIGHT=301
HAS_EA_WEIGHT=500
HAS_ODD_EA_WEIGHT=501
HAS_INTRNAL_WEIGHT=2000
HAS_VERY_ODD_WEIGHT=9999
get_non_fcs_weight() {
    status=0
    if [ $# -eq 0 ]; then
        read non_fcs_part remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${non_fcs_part}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        non_fcs_part=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t get_non_fcs_weight \n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -z "${non_fcs_part}" ]; then
            echo ${HAS_FCS_WEIGHT}
        else
            case "${non_fcs_part}" in
                fcs)
                    echo ${HAS_ODD_FCS_WEIGHT}
                    ;;
                rc)
                    echo ${HAS_RC_WEIGHT}
                    ;;
                rc[0-9] | rc[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "rc\([0-9]*\)$"`
                    echo `expr ${HAS_RC_WEIGHT} - ${count}`
                    ;;
                rc*)
                    echo ${HAS_ODD_RC_WEIGHT}
                    ;;
                beta)
                    echo ${HAS_BETA_WEIGHT}
                    ;;
                beta[0-9] | beta[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "beta\([0-9]*\)$"`
                    echo `expr ${HAS_BETA_WEIGHT} - ${count}`
                    ;;
                beta*)
                    echo ${HAS_ODD_BETA_WEIGHT}
                    ;;
                ea)
                    echo ${HAS_EA_WEIGHT}
                    ;;
                ea[0-9] | ea[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "ea\([0-9]*\)$"`
                    echo `expr ${HAS_EA_WEIGHT} - ${count}`
                    ;;
                ea*)
                    echo ${HAS_ODD_EA_WEIGHT}
                    ;;
                internal)
                    echo ${HAS_INTRNAL_WEIGHT}
                    ;;
                internal[0-9] | internal[0-9][0-9] | internal[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "internal\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                b[0-9] | b[0-9][0-9] | b[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "b\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                *)
                    echo ${HAS_VERY_ODD_WEIGHT}
                    ;;
            esac
        fi
    fi
    return ${status}
}
    get_path_weight() {
    good_list="$1"
    path=$2
    release=`basename ${path}`
    parts="`parse_release ${release}`"
    if [ $? -eq 0 ]; then
        name=`echo "${parts}" | cut -f1`
        version=`echo "${parts}" | cut -f2`
        non_fcs=`echo "${parts}" | cut -f3`
        if [ -n "${version}" ]; then
           v_weight=`echo ${version} | expand_version`
           n_weight=`echo ${name} | get_name_weight - "${good_list}"`
           o_weight=`echo ${non_fcs} | get_non_fcs_weight`
           printf "%4d  %4d  %4d  %4d  %4d  %4d  %s\n" \
                  ${v_weight} ${n_weight} ${o_weight} "${path}"
        fi
    fi
}
get_weighted_list() {
    good_list=
    verify=
    stdio=
    status=0
    check=true
    while [ -n "${check}" ]; do
        if [ $# -gt 0 ]; then
            case "$1" in
                -g)
                    good_list="$2"
                    shift 2
                    ;;
                --good-list=*)
                    length=`expr length "$1"`
                    remove=`expr \( length "--good-list=" \) + 1`
                    good_list="`expr substr \"$1\" ${remove} ${length}`"
                    shift 1
                    ;;
                -v | --verify)
                    verify=true
                    shift 1
                    ;;
                --)
                    shift 1
                    check=
                    ;;
                -)
                    shift 1
                    stdio=true
                    ;;
                -*)
                    printf "Error: usage - unknown parameter:\n\n" \
								>> /dev/stderr
                    printf "\t%s : %s\n" "$1" "$*"		>> /dev/stderr
                    status=${PRS_ERROR_BAD_PARAMS}
                    check=
                    ;;
                *)
                    check=
                    ;;
            esac
        else
            check=
        fi
    done
    if [ $# -eq 0 ] || [ -n "${stdio}" ]; then
        read line
        while [ -n "${line}" ]; do
            if [ -z "${verify}" ] || [ -f ${line}/bin/java ]; then
                get_path_weight "${good_list}" ${line}
            fi
            read line
        done
    fi
    while [ $# -gt 0 ]; do
        if [ -z "${verify}" ] || [ -f $1/bin/java ]; then
            get_path_weight "${good_list}" $1
        fi
        shift 1
    done
    return ${status}
}
_compare_java_by_weight() {
    compare=0
    if [ $# -ne 0 ]; then
        if [ $# -eq 1 ]; then
            compare=1
        else
            left=$1
            right=$2
            shift 2
            good="$*"
            list=`get_weighted_list --good-list="${good}" \
                    ${left} ${right} | sort -u -k1n -k2n -k3n -k4n -k5rn -k6rn`
            if [ `echo "${list}" | wc -l | tr -d "[:space:]"` -ne 1 ]; then
                compare=-1
                latest=`echo "${list}" | tail -n 1 | cut -c 37-`
                if [ "${left}" = "${latest}" ]; then
                    compare=1
                fi
            fi
        fi
    fi
    echo ${compare}
}
compare_java_by_version() {
    _compare_java_by_weight $1 $2
}
compare_java_by_release() {
    _compare_java_by_weight $1 $2 ${KNOWN_GOOD_NAME_LIST}
}
find_latest_release() {
    if [ -d /usr/java ]; then
        latest_release=`find /usr/java/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
    fi
    if [ -d "${RPM_INSTALL_PREFIX}" ] && \
       [ "/usr/java" != "${RPM_INSTALL_PREFIX}" ]
    then 
        prefix_release=`find ${RPM_INSTALL_PREFIX}/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
        if [ `compare_java_by_release ${latest_release} ${prefix_release}` -lt 0 ]; then
            latest_release=${prefix_release}
        fi
    fi
    echo ${latest_release}
}
get_javaws() {
    path=$1
    if [ `compare_java_by_version ${path} version-1.5.0` -ge 0 ] &&
       [ -f ${path}/bin/javaws ]
    then
        path=${path}/bin/javaws
    elif [ `compare_java_by_version ${path} version-1.4.2` -ge 0 ]; then
        if [ -f ${path}/jre/javaws/javaws ]; then
            path=${path}/jre/javaws/javaws
        elif [ -f ${path}/javaws/javaws ]; then
            path=${path}/javaws/javaws
        else
            path=
        fi
    else
        path=
    fi
    echo ${path}
}
    LINK_ERROR_BAD_PARAMS=3000
LINK_ERROR_DEAD_LINK=3001
LINK_ERROR_FILE_NOT_FOUND=3002
dereference() {
    status=0
    if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
        follow="--follow"
        shift 1
    fi
    if [ $# -ge 1 ]; then
        path="$*"
        if [ -e "${path}" ]; then
            parent="`cd \`dirname \"${path}\"\`; pwd`"
            child="`basename \"${path}\"`"
            if [ "${parent}" != "${child}" ]; then
                path="${parent}/${child}"
            fi
            if [ -h "${path}" ]; then
                path=`ls -l "${path}" | sed -e "s#^.*${path} -> ##"`
                if [ "`expr substr \"${path}\" 1 1`" != "/" ]; then
                    path="${parent}/${path}"
                fi
                if [ -n "${follow}" ]; then
                    path="`dereference ${follow} ${path}`"
                fi                    
            fi
        else
            status=${LINK_ERROR_FILE_NOT_FOUND}
        fi
    fi
    echo ${path}
    return ${status}
}
setup_latest_link() {
    latest=$1
    link=$2
    if [ -h "${link}" ]; then
        reference="`dereference --follow ${link}`"
        if [ $? -eq 0 ]; then
            update=`compare_java_by_release "${latest}" "${reference}"`
        else
            update=1
        fi
        if [ ${update} -gt 0 ]; then
            rm -f "${link}"
        fi
    fi
    if [ ! -e "${link}" ]; then
        ln -s "${latest}" "${link}"
    fi
}
setup_default_links() {
    if [ $# -ge 2 ]; then
        latest_link="$1"
        default_link="$2"
        if [ ! -e "${default_link}" ]; then
            ln -s "${latest_link}" "${default_link}"
        fi
    fi
    if [ $# -gt 3 ]; then
        bindir="$3"
        shift 3
        for file in $*; do
            reference="`dereference --follow ${bindir}/${file}`"
            if [ $? -ne 0 ]; then
                rm -f "${bindir}/${file}"
            fi
            source="${default_link}/bin/${file}"
            if [ "${file}" = "javaws" ]; then
                source="`get_javaws \"${default_link}\"`"
            fi
            if [ -n "${source}" ] && [ ! -e "${bindir}/${file}" ]; then
                ln -s "${source}" "${bindir}/${file}"
            fi
        done
    fi
}
cleanup_default_links() {
    if [ $# -ge 1 ]; then
        default_link=$1
        if [ $# -gt 2 ]; then
            bindir="$2"
            shift 2
            for file in $*; do
                reference="`dereference \"${bindir}/${file}\"`"
                if [ $? -ne 0 ] ||
                   [ "${reference}" = "${default_link}/bin/${file}" ]
                then
                    rm -f "${bindir}/${file}"
                fi
            done
        fi
        rm -f "${default_link}"
    fi
}

    #
    # Unpack the packed JAR files.
    #
    unpack_jars "${RPM_INSTALL_PREFIX}/jdk1.6.0_26/bin/unpack200" \
                "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" \
                jre/lib/rt.jar jre/lib/jsse.jar jre/lib/charsets.jar lib/tools.jar jre/lib/ext/localedata.jar jre/lib/plugin.jar jre/lib/javaws.jar jre/lib/deploy.jar

    # fix for: 4728032 - Install needs to generate shared class files
    ${RPM_INSTALL_PREFIX}/jdk1.6.0_26/bin/java -client -Xshare:dump > /dev/null 2>&1

    # Create a service tag if supported on the system.
    # No product registration is done.
    #
    # If the package is being relocated, the installer will not create 
    # a service tag since the service tag registry client 
    # (see /usr/bin/stclient) only supports local system use.
    # A RFE# 6576434 is created for stclient to support the remote installation
    # support.
    #
    if [ "${RPM_INSTALL_PREFIX}" = "/usr/java" ]; then
         ${RPM_INSTALL_PREFIX}/jdk1.6.0_26/bin/java com.sun.servicetag.Installer -source "jdk" > /dev/null 2>&1
    fi

    #
    # Find out what version of Java is the latest.  Don't do any system
    # integration unless this is the latest version.  Otherwise, we make it
    # difficult for future installers.
    #
    LATEST_JAVA_PATH="`find_latest_release`"
    if [ "${LATEST_JAVA_PATH}" == "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" ] ||
       [ "${LATEST_JAVA_PATH}" == "/usr/java/jdk1.6.0_26" ]
    then
        #
        # Make sure the /usr/java/latest link points to LATEST_JAVA_PATH, and
	# update it if it doesn't.
        #
        setup_latest_link "${LATEST_JAVA_PATH}" "/usr/java/latest"

        #
        # Make sure the /usr/java/default and java javaws jcontrol javac jar javadoc exist.
	# If anything is missing, create it.
        #
        setup_default_links "/usr/java/latest" "/usr/java/default" \
                            "/usr/bin" java javaws jcontrol javac jar javadoc

        #
        # If the "latest" link is a JDK, then the latest JRE is a subdir;
	# otherwise it is the same dir.
        #
        DEFAULT_JRE_PATH="/usr/java/default"
        if [ -e "/usr/java/default/jre/bin/java" ]; then
            DEFAULT_JRE_PATH="/usr/java/default/jre"
        fi

	#
	# Perform all integrations with the freedesktop.org desktop integration
	# specifications and Gnome legacy implementations.
	#
	IntegrateWithGnome

        # setup the mailcap file
        UpdateMailcap /etc/mailcap application/x-java-jnlp-file "/usr/bin/javaws %s"

        # setup the mime.type file
        UpdateMimeTypes /etc/mime.types application/x-java-jnlp-file \
			"Java Web Start" jnlp
    fi

    #
    # If the package is being relocated, then create a link in the default
    # location (/usr/java) to the actual install directory.  Do this
    # last, so it doesn't add unnecessary complexity to the search for the
    # latest release.
    #
    if [ "${RPM_INSTALL_PREFIX}" != "/usr/java" ] &&
       ( [ ! -e "/usr/java/jdk1.6.0_26" ] || [ -h "/usr/java/jdk1.6.0_26" ] )
    then
        rm -f "/usr/java/jdk1.6.0_26"
        ln -s "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" "/usr/java/jdk1.6.0_26"
    fi

    #
    # Next, make sure the files required for the Prferences API are setup
    # correctly.  Any files from an old, uninstalled version will have left
    # files with a .rpmsave extension.  If there was an older version currently
    # installed when this version installed, there will be a set of files with
    # a .rpmnew extension.  Try to use the best possible file (i.e. save old
    # preference settings).
    #
    if [ -f /etc/.java/.systemPrefs/.system.lock.rpmsave ] &&
       [ ! -s /etc/.java/.systemPrefs/.system.lock ]
    then
        #
        # Only overwrite if old file is empty (rpmsave is only created if it is
        # non-empty).
        #
        rm -f /etc/.java/.systemPrefs/.system.lock
        mv /etc/.java/.systemPrefs/.system.lock.rpmsave \
           /etc/.java/.systemPrefs/.system.lock
    elif [ -f /etc/.java/.systemPrefs/.system.lock.rpmnew ]
    then
        if [ -s /etc/.java/.systemPrefs/.system.lock ]; then
            #
            # The existing lock is non-empty, so there is no reason to keep the
            # .rpmnew one created during this install.
            #
            rm -f /etc/.java/.systemPrefs/.system.lock.rpmnew
        else
            #
            # The existing lock is empty, so replace it with the new one.  This
            # makes future installs a little cleaner, since the file in use is
            # the file in the RPM database.
            #
            rm -f /etc/.java/.systemPrefs/.system.lock
            mv /etc/.java/.systemPrefs/.system.lock.rpmnew \
               /etc/.java/.systemPrefs/.system.lock
        fi
    fi

    if [ -f /etc/.java/.systemPrefs/.systemRootModFile.rpmsave ] &&
       [ ! -s /etc/.java/.systemPrefs/.systemRootModFile ]
    then
        #
        # Only overwrite if old file is empty (rpmsave is only created if it is
        # non-empty).
        #
        rm -f /etc/.java/.systemPrefs/.systemRootModFile
        mv /etc/.java/.systemPrefs/.systemRootModFile.rpmsave \
           /etc/.java/.systemPrefs/.systemRootModFile
    elif [ -f /etc/.java/.systemPrefs/.systemRootModFile.rpmnew ]
    then
        if [ -s /etc/.java/.systemPrefs/.systemRootModFile ]; then
            #
            # The existing lock is non-empty, so there is no reason to keep the
            # .rpmnew one created during this install.
            #
            rm -f /etc/.java/.systemPrefs/.systemRootModFile.rpmnew
        else
            #
            # The existing lock is empty, so replace it with the new one.  This
            # makes future installs a little cleaner, since the file in use is
            # the file in the RPM database.
            #
            rm -f /etc/.java/.systemPrefs/.systemRootModFile
            mv /etc/.java/.systemPrefs/.systemRootModFile.rpmnew \
               /etc/.java/.systemPrefs/.systemRootModFile
        fi
    fi

    #
    # Try to register the init script to the various run levels.  If possible
    # this is accomplished using an LSB defined install tool.  If that isn't
    # available, then try to use chkconfig, which is supported by Red Hat and
    # Debian.  The feature of automatic jar file execution is not support on
    # systems which don't support either of these interfaces.
    #
    if [ -x /usr/lib/lsb/install_initd ]; then
        /usr/lib/lsb/install_initd jexec > /dev/null 2>&1

        # start the service for the current session
        /etc/init.d/jexec start > /dev/null 2>&1
    elif [ -x /sbin/chkconfig ]; then
        /sbin/chkconfig --add jexec > /dev/null 2>&1

        # start the service for the current session
        /etc/init.d/jexec start > /dev/null 2>&1
    fi


%preun -p /bin/sh
#
    # Add the shell function and related variables used by the pre-uninstall.
    #
    MOST_DIGITS="[1-9]"
ALL_DIGITS="[0-9]"
COUNTING_NUMBER="${MOST_DIGITS}${ALL_DIGITS}*\|0"
VALID_NON_NUMERIC="[-_.a-zA-Z]"
VALID_CHARS="[-_.a-zA-Z0-9]"
MAJOR_RULE="\(${MOST_DIGITS}${ALL_DIGITS}*\)"
MINOR_RULE="\(${COUNTING_NUMBER}\)"
MICRO_RULE="\(${COUNTING_NUMBER}\)"
UPDATE_RULE="\(${MOST_DIGITS}${ALL_DIGITS}\|0${ALL_DIGITS}\)"
NON_FCS_ID_RULE="\([a-zA-Z0-9]*\)"
MIN_VERSION_ID_RULE="${MAJOR_RULE}\.${MINOR_RULE}\.${MICRO_RULE}"
FCS_VERSION_ID_RULE="${MIN_VERSION_ID_RULE}\(_${UPDATE_RULE}\)\?"
VERSION_ID_RULE="${FCS_VERSION_ID_RULE}\(-${NON_FCS_ID_RULE}\)\?"
NAME_ID_RULE="${VALID_CHARS}*${VALID_NON_NUMERIC}"
KNOWN_GOOD_NAME_LIST="java jdk jre j2sdk j2re"
PRS_ERROR_BAD_PARAMS=2000
expand_version() {
    status=0
    if [ $# -eq 0 ]; then
        read release remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${release}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${release}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        release=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        \printf "\t expand_version\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        format="%d\t%d\t%d\t%d\n"
        echo ${release} | sed -e "s/_/\./g" | \
          awk -v format="${format}" 'BEGIN { FS = "." } { printf format, $1, $2, $3, $4 }'
    fi
    return ${status}
}
parse_release() {
    status=0
    if [ $# -eq 0 ]; then
        read string remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${string}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${string}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        string=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t parse_release %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        version_id=`expr "${string}" : "${NAME_ID_RULE}\(${VERSION_ID_RULE}\)\$"`
        if [ -n "${version_id}" ]; then
            name_id=`expr "${string}" : "\(${NAME_ID_RULE}\)${VERSION_ID_RULE}\$"`
            fcs_part=`expr "${string}" : "${NAME_ID_RULE}\(${FCS_VERSION_ID_RULE}\).*\$"`
            non_fcs_part=`expr "${version_id}" : "[^-]*-\(${NON_FCS_ID_RULE}\)\$"`
	    printf "%s\t%s\t%s\n" "${name_id}" "${fcs_part}" "${non_fcs_part}"
        fi
    fi
    return ${status}
}
UNKNOWN_NAME_WEIGHT=1000
get_name_weight() {
    status=0
    if [ "$1" = "-" ]; then
        read name good_names
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        else
            shift 1
            if [ $# -gt 0 ]; then
                good_names="$*"
            fi
            if [ -z "${name}" ]; then
                printf "Error: usage - function requires input!\n" >> /dev/stderr
                status=${PRS_ERROR_BAD_PARAMS}
            fi
        fi
    elif [ $# -gt 1 ]; then
        name=$1
        shift 1
        good_names="$*"
    else
        printf "Error: usage - function takes 2+ parameters:\n\n" >> /dev/stderr
        printf "\t get_name_weight %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -n "${good_names}" ]; then
            length=`expr length "${good_names}"`
            pos=`expr "${good_names}" : ".*\<${name}\>"`
            if [ ${pos} -gt 0 ]; then
                expr substr "${good_names}" 1 ${pos} | wc -w | tr -d "[:space:]"
            else
                echo ${UNKNOWN_NAME_WEIGHT}
            fi
        else
            echo ${UNKNOWN_NAME_WEIGHT}
        fi
    fi
    return ${status}
}
HAS_FCS_WEIGHT=0
HAS_ODD_FCS_WEIGHT=1
HAS_RC_WEIGHT=100
HAS_ODD_RC_WEIGHT=101
HAS_BETA_WEIGHT=300
HAS_ODD_BETA_WEIGHT=301
HAS_EA_WEIGHT=500
HAS_ODD_EA_WEIGHT=501
HAS_INTRNAL_WEIGHT=2000
HAS_VERY_ODD_WEIGHT=9999
get_non_fcs_weight() {
    status=0
    if [ $# -eq 0 ]; then
        read non_fcs_part remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${non_fcs_part}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        non_fcs_part=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t get_non_fcs_weight \n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -z "${non_fcs_part}" ]; then
            echo ${HAS_FCS_WEIGHT}
        else
            case "${non_fcs_part}" in
                fcs)
                    echo ${HAS_ODD_FCS_WEIGHT}
                    ;;
                rc)
                    echo ${HAS_RC_WEIGHT}
                    ;;
                rc[0-9] | rc[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "rc\([0-9]*\)$"`
                    echo `expr ${HAS_RC_WEIGHT} - ${count}`
                    ;;
                rc*)
                    echo ${HAS_ODD_RC_WEIGHT}
                    ;;
                beta)
                    echo ${HAS_BETA_WEIGHT}
                    ;;
                beta[0-9] | beta[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "beta\([0-9]*\)$"`
                    echo `expr ${HAS_BETA_WEIGHT} - ${count}`
                    ;;
                beta*)
                    echo ${HAS_ODD_BETA_WEIGHT}
                    ;;
                ea)
                    echo ${HAS_EA_WEIGHT}
                    ;;
                ea[0-9] | ea[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "ea\([0-9]*\)$"`
                    echo `expr ${HAS_EA_WEIGHT} - ${count}`
                    ;;
                ea*)
                    echo ${HAS_ODD_EA_WEIGHT}
                    ;;
                internal)
                    echo ${HAS_INTRNAL_WEIGHT}
                    ;;
                internal[0-9] | internal[0-9][0-9] | internal[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "internal\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                b[0-9] | b[0-9][0-9] | b[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "b\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                *)
                    echo ${HAS_VERY_ODD_WEIGHT}
                    ;;
            esac
        fi
    fi
    return ${status}
}
    get_path_weight() {
    good_list="$1"
    path=$2
    release=`basename ${path}`
    parts="`parse_release ${release}`"
    if [ $? -eq 0 ]; then
        name=`echo "${parts}" | cut -f1`
        version=`echo "${parts}" | cut -f2`
        non_fcs=`echo "${parts}" | cut -f3`
        if [ -n "${version}" ]; then
           v_weight=`echo ${version} | expand_version`
           n_weight=`echo ${name} | get_name_weight - "${good_list}"`
           o_weight=`echo ${non_fcs} | get_non_fcs_weight`
           printf "%4d  %4d  %4d  %4d  %4d  %4d  %s\n" \
                  ${v_weight} ${n_weight} ${o_weight} "${path}"
        fi
    fi
}
get_weighted_list() {
    good_list=
    verify=
    stdio=
    status=0
    check=true
    while [ -n "${check}" ]; do
        if [ $# -gt 0 ]; then
            case "$1" in
                -g)
                    good_list="$2"
                    shift 2
                    ;;
                --good-list=*)
                    length=`expr length "$1"`
                    remove=`expr \( length "--good-list=" \) + 1`
                    good_list="`expr substr \"$1\" ${remove} ${length}`"
                    shift 1
                    ;;
                -v | --verify)
                    verify=true
                    shift 1
                    ;;
                --)
                    shift 1
                    check=
                    ;;
                -)
                    shift 1
                    stdio=true
                    ;;
                -*)
                    printf "Error: usage - unknown parameter:\n\n" \
								>> /dev/stderr
                    printf "\t%s : %s\n" "$1" "$*"		>> /dev/stderr
                    status=${PRS_ERROR_BAD_PARAMS}
                    check=
                    ;;
                *)
                    check=
                    ;;
            esac
        else
            check=
        fi
    done
    if [ $# -eq 0 ] || [ -n "${stdio}" ]; then
        read line
        while [ -n "${line}" ]; do
            if [ -z "${verify}" ] || [ -f ${line}/bin/java ]; then
                get_path_weight "${good_list}" ${line}
            fi
            read line
        done
    fi
    while [ $# -gt 0 ]; do
        if [ -z "${verify}" ] || [ -f $1/bin/java ]; then
            get_path_weight "${good_list}" $1
        fi
        shift 1
    done
    return ${status}
}
_compare_java_by_weight() {
    compare=0
    if [ $# -ne 0 ]; then
        if [ $# -eq 1 ]; then
            compare=1
        else
            left=$1
            right=$2
            shift 2
            good="$*"
            list=`get_weighted_list --good-list="${good}" \
                    ${left} ${right} | sort -u -k1n -k2n -k3n -k4n -k5rn -k6rn`
            if [ `echo "${list}" | wc -l | tr -d "[:space:]"` -ne 1 ]; then
                compare=-1
                latest=`echo "${list}" | tail -n 1 | cut -c 37-`
                if [ "${left}" = "${latest}" ]; then
                    compare=1
                fi
            fi
        fi
    fi
    echo ${compare}
}
compare_java_by_version() {
    _compare_java_by_weight $1 $2
}
compare_java_by_release() {
    _compare_java_by_weight $1 $2 ${KNOWN_GOOD_NAME_LIST}
}
find_latest_release() {
    if [ -d /usr/java ]; then
        latest_release=`find /usr/java/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
    fi
    if [ -d "${RPM_INSTALL_PREFIX}" ] && \
       [ "/usr/java" != "${RPM_INSTALL_PREFIX}" ]
    then 
        prefix_release=`find ${RPM_INSTALL_PREFIX}/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
        if [ `compare_java_by_release ${latest_release} ${prefix_release}` -lt 0 ]; then
            latest_release=${prefix_release}
        fi
    fi
    echo ${latest_release}
}
get_javaws() {
    path=$1
    if [ `compare_java_by_version ${path} version-1.5.0` -ge 0 ] &&
       [ -f ${path}/bin/javaws ]
    then
        path=${path}/bin/javaws
    elif [ `compare_java_by_version ${path} version-1.4.2` -ge 0 ]; then
        if [ -f ${path}/jre/javaws/javaws ]; then
            path=${path}/jre/javaws/javaws
        elif [ -f ${path}/javaws/javaws ]; then
            path=${path}/javaws/javaws
        else
            path=
        fi
    else
        path=
    fi
    echo ${path}
}
    LINK_ERROR_BAD_PARAMS=3000
LINK_ERROR_DEAD_LINK=3001
LINK_ERROR_FILE_NOT_FOUND=3002
dereference() {
    status=0
    if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
        follow="--follow"
        shift 1
    fi
    if [ $# -ge 1 ]; then
        path="$*"
        if [ -e "${path}" ]; then
            parent="`cd \`dirname \"${path}\"\`; pwd`"
            child="`basename \"${path}\"`"
            if [ "${parent}" != "${child}" ]; then
                path="${parent}/${child}"
            fi
            if [ -h "${path}" ]; then
                path=`ls -l "${path}" | sed -e "s#^.*${path} -> ##"`
                if [ "`expr substr \"${path}\" 1 1`" != "/" ]; then
                    path="${parent}/${path}"
                fi
                if [ -n "${follow}" ]; then
                    path="`dereference ${follow} ${path}`"
                fi                    
            fi
        else
            status=${LINK_ERROR_FILE_NOT_FOUND}
        fi
    fi
    echo ${path}
    return ${status}
}
setup_latest_link() {
    latest=$1
    link=$2
    if [ -h "${link}" ]; then
        reference="`dereference --follow ${link}`"
        if [ $? -eq 0 ]; then
            update=`compare_java_by_release "${latest}" "${reference}"`
        else
            update=1
        fi
        if [ ${update} -gt 0 ]; then
            rm -f "${link}"
        fi
    fi
    if [ ! -e "${link}" ]; then
        ln -s "${latest}" "${link}"
    fi
}
setup_default_links() {
    if [ $# -ge 2 ]; then
        latest_link="$1"
        default_link="$2"
        if [ ! -e "${default_link}" ]; then
            ln -s "${latest_link}" "${default_link}"
        fi
    fi
    if [ $# -gt 3 ]; then
        bindir="$3"
        shift 3
        for file in $*; do
            reference="`dereference --follow ${bindir}/${file}`"
            if [ $? -ne 0 ]; then
                rm -f "${bindir}/${file}"
            fi
            source="${default_link}/bin/${file}"
            if [ "${file}" = "javaws" ]; then
                source="`get_javaws \"${default_link}\"`"
            fi
            if [ -n "${source}" ] && [ ! -e "${bindir}/${file}" ]; then
                ln -s "${source}" "${bindir}/${file}"
            fi
        done
    fi
}
cleanup_default_links() {
    if [ $# -ge 1 ]; then
        default_link=$1
        if [ $# -gt 2 ]; then
            bindir="$2"
            shift 2
            for file in $*; do
                reference="`dereference \"${bindir}/${file}\"`"
                if [ $? -ne 0 ] ||
                   [ "${reference}" = "${default_link}/bin/${file}" ]
                then
                    rm -f "${bindir}/${file}"
                fi
            done
        fi
        rm -f "${default_link}"
    fi
}

    # Delete a service tag if exists 
    #
    # If the package is being relocated, the installer will not create 
    # a service tag since the service tag registry client 
    # (see /usr/bin/stclient) only supports local system use.
    # A RFE# 6576434 is created for stclient to support the remote installation
    # support.
    #
    if [ "${RPM_INSTALL_PREFIX}" = "/usr/java" ]; then 
        ${RPM_INSTALL_PREFIX}/jdk1.6.0_26/bin/java com.sun.servicetag.Installer -delete 
    fi

    #
    # Dereference and follow any links that might have been created when this
    # package was installed.  If a link ultimately points to this installation
    # or the link is dead, then we should remove the link.  Important links,
    # like default and latest can be remade in post-uninstall (%postun).
    #
    # This is done in the reverse order the links were initially created in, in
    # case there are any partial loops.
    #
    if [ -h "/usr/java/default" ]; then
        DEFAULT_LINK="`dereference --follow \"/usr/java/default\"`"
        if [ $? -ne 0 ] ||
           [ "${DEFAULT_LINK}" = "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" ]
        then
            cleanup_default_links "/usr/java/default" \
                                  "/usr/bin" java javaws jcontrol javac jar javadoc
        fi
    fi

    #
    # If the latest link still points to this installation it must mean one of
    # the following:
    #
    #     * No newer version of Java has been installed.  This is known because
    #       any such version would have already changed the latest to point
    #       to itself.
    #
    #     * No older version is installed.  We don't check this now, but if this
    #       is the case, now is the best time to remove the latest link, since
    #       anything pointing to this installation in post-uninstall will be a
    #       dead link.
    #
    #     * There is an older version of Java installed.  In this case we need
    #       to handle the latest link differently depending on what version
    #       remains.
    #
    if [ -h "/usr/java/latest" ]; then
        LATEST_LINK="`dereference --follow \"/usr/java/latest\"`"
        if [ $? -ne 0 ] ||
           [ "${LATEST_LINK}" = "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" ]
        then
            #
            # If this version is the latest, and the first version with jexec
            # support, then stop and remove the jexec service.  If this isn't
            # done now, there might not be an init script left when %postun is
            # called, and if there is, we can restart/reinstall the service
            # easy enough then.
            #
            if [ `compare_java_by_version ${LATEST_LINK} \
                                  version-1.6.0` -ge 0 ] &&
               [ -x /etc/init.d/jexec ]
            then
                /etc/init.d/jexec stop > /dev/null 2>&1

                if [ -x /usr/lib/lsb/remove_initd ]; then
                    /usr/lib/lsb/remove_initd jexec > /dev/null 2>&1
                elif [ -x /sbin/chkconfig ]; then
                    /sbin/chkconfig --del jexec > /dev/null 2>&1
                fi
            fi

            rm -f "/usr/java/latest" 2> /dev/null
        fi
    fi

    #
    # If the package was relocated when it was installed, there should be a link
    # in /usr/java.  So, if there is a link named /usr/java/jdk1.6.0_26 that is
    # dead, or points back to ${RPM_INSTALL_PREFIX}, delete it.
    #
    if [ "${RPM_INSTALL_PREFIX}" != "/usr/java" ] &&
       [ -h "/usr/java/jdk1.6.0_26" ]
    then
        THIS_LINK="`dereference --follow \"/usr/java/jdk1.6.0_26\"`"
        if [ $? -ne 0 ] ||
           [ "${THIS_LINK}" = "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" ]
        then
            rm -f "/usr/java/jdk1.6.0_26" 2> /dev/null
        fi
    fi


%postun -p /bin/sh
#
    # Make sure any new files are created with a secure access mask.  Do not use
    # chmod, since that would also change the rights of any existing files, and
    # we are only interested in setting the rights for new files.
    #
    umask 022

    #
    # The package assumes that Gnome is either installed, or going to be
    # installed, so if nothing currently exists, then install in the default
    # location.
    #
    # NOTE: These variables must be defined before all the shell function macros
    #       are included.
    #
    if [ -z "${GNOMEDIR}" ]; then
        GNOMEDIR=/usr
    fi

    #
    # RPM_INSTALL_PREFIX doesn't seem to be set by "alien" so the following
    # minor kludge allows some functionality on debian-like systems (such
    # a Ubuntu) which don't support packages.
    #
    if [ -z "${RPM_INSTALL_PREFIX}" ]; then
	RPM_INSTALL_PREFIX="/usr/java"
    fi

    #
    # Gross kludge for old SuSE distros: Even though they set the environment
    # variable GNOMEDIR to /opt/gnome, Gnome may really be in /opt/gnome2.
    # Go figure,... (I feel so unclean....)
    #
    if [ "${GNOMEDIR}" = "/opt/gnome" ] && [ -d "/opt/gnome2" ]; then
	GNOMEDIR="/opt/gnome2"
    fi

    INSTALL_JRE_PATH=${RPM_INSTALL_PREFIX}/jdk1.6.0_26
    if [ -e ${INSTALL_JRE_PATH}/jre/bin/java ]; then
	INSTALL_JRE_PATH=${INSTALL_JRE_PATH}/jre
    fi

    #
    # Add the shell function and related variables used by the post-uninstall.
    #
    NS_COMMENT1="#--Netscape Communications Corporation MIME Information"
NS_COMMENT2="#Do not delete the above line. It is used to identify the file type."
NS_COMMENT3="#mime types added by Netscape Helper"
UpdateMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    command="$3"
    if [ -z "`grep -E \"^${mime_type}; ${command}$\" \"${mailcap_file}\" 2> /dev/null`" ]; then
        mc_comment="# Java Web Start"
        mc_text=
        if [ -w "${mailcap_file}" ]; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
        fi
        if [ -w "`dirname \"${mailcap_file}\"`" ]; then
            mc_text="${mc_text:+${mc_text}\n}${mime_type}; ${command}"
            printf "%s" "${mc_text}" > "${mailcap_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mailcap_file}"
            echo "Check permissions."
        fi
    fi
}
RemoveMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    mc_comment="# Java Web Start"
    if [ -w "${mailcap_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mailcap_file}\"`" ] ; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
            if [ `echo "${mc_text}" | tr -d '[:space:]' | wc -c` -gt 0 ]; then
                echo "${mc_text}" > "${mailcap_file}"
            else
                rm -f "${mailcap_file}"
            fi
        fi
    fi
}
UpdateMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    desc="$3"
    shift 3
    exts="$*"
    JNLP_ENTRY="type=${mime_type} desc=\"${desc}\" exts=\"${exts}\""
    if [ ! -w "${mime_file}" ]; then
        if [ -w `dirname ${mime_file}` ]; then
            echo "${NS_COMMENT1}"  > "${mime_file}"
            echo "${NS_COMMENT2}" >> "${mime_file}"
            echo "${NS_COMMENT3}" >> "${mime_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mime_file}"
            echo "Check permissions."
            return
        fi
    fi
    if [ -z "`grep -E \"^[^#]*${mime_type}\" \"${mime_file}\"`" ]; then
        echo ${JNLP_ENTRY} >> "${mime_file}"
    fi
}
RemoveMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    if [ -w "${mime_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mime_file}\"`" ]; then
            regexp="(${mime_type})|(^${NS_COMMENT1}$)|(^${NS_COMMENT2}$)|(^${NS_COMMENT3}$)"
            if [ `grep -Ev "${regexp}" "${mime_file}" | \
                 tr -d '[:space:]' | wc -c` -gt 0 ]
            then
                mt_text="`grep -v \"${mime_type}\" \"${mime_file}\"`"
                echo "${mt_text}" > "${mime_file}"
            else
                rm -f "${mime_file}"
            fi
        fi
    fi
}
    JDK_DESKTOP="${INSTALL_JRE_PATH}/lib/desktop"
JDK_ICONS="${JDK_DESKTOP}/icons"
JDK_APPS="${JDK_DESKTOP}/applications"
JDK_MIME="${JDK_DESKTOP}/mime"
SHARE_PATH="${GNOMEDIR}/share"
SHARE_ICONS="${SHARE_PATH}/icons"
SHARE_MIME="${SHARE_PATH}/mime"
SHARE_APPS="${SHARE_PATH}/applications"
HICOLOR=hicolor
HIGHCONTRAST=HighContrast
HIGHCONTRASTINVERSE=HighContrastInverse
LOWCONTRAST=LowContrast
THEMES="${HICOLOR} ${HIGHCONTRAST} ${HIGHCONTRASTINVERSE} ${LOWCONTRAST}"
RESOLUTIONS="16x16 48x48"
TEXT_ICON="gnome-mime-text-x-java.png"
JAR_ICON="gnome-mime-application-x-java-archive.png"
JNLP_ICON="gnome-mime-application-x-java-jnlp-file.png"
JAVA_ICON="sun-java.png"
JAVAWS_ICON="sun-javaws.png"
JCONTROL_ICON="sun-jcontrol.png"
APPS_ICONS="${JAVA_ICON} ${JAVAWS_ICON} ${JCONTROL_ICON}"
MIME_ICONS="${TEXT_ICON} ${JAR_ICON} ${JNLP_ICON}"
ICONS="${APPS_ICONS} ${MIME_ICONS}"
GNOME_UTILS_DIRS="/usr/bin /opt/gnome/bin"
UPDATE_MIME_DATABASE="update-mime-database"
UPDATE_DESKTOP_DATABASE="update-desktop-database"
GTK_UPDATE_ICON_CACHE="gtk-update-icon-cache"
SHARE_CONTROL_CENTER="${SHARE_PATH}/control-center-2.0"
SHARE_CAPPLETS="${SHARE_CONTROL_CENTER}/capplets"
SHARE_MIME_INFO="${SHARE_PATH}/mime-info"
SHARE_APP_REGISTRY="${SHARE_PATH}/application-registry"
SHARE_PIXMAPS="${SHARE_PATH}/pixmaps"
UpdateIconCache() {
    _icon_theme_root=$1
    if [ -f ${_icon_theme_root}/icon-theme.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${GTK_UPDATE_ICON_CACHE} ]; then
		${_dir}/${GTK_UPDATE_ICON_CACHE} ${_icon_theme_root} \
		    > /dev/null 2>&1
		break
	    fi
	done
	touch ${_icon_theme_root}
	for _dir in ${RESOLUTIONS}; do
	    if [ -d ${_icon_theme_root}/${_dir} ]; then
		touch ${_icon_theme_root}/${_dir}
	    fi
        done
    fi
}
UpdateDesktopDatabase() {
    _desktop_root=$1
    if [ -f ${_desktop_root}/mimeinfo.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_DESKTOP_DATABASE} ]; then
		${_dir}/${UPDATE_DESKTOP_DATABASE} ${_desktop_root} \
		   > /dev/null 2>&1
		break
	    fi
	done
    fi
}
UpdateMimeDatabase() {
    _mime_root=$1
    if [ -d ${_mime_root}/packages ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_MIME_DATABASE} ]; then
		${_dir}/${UPDATE_MIME_DATABASE} ${_mime_root} > /dev/null 2>&1
		break
	    fi
	done
    fi
}
InstallGnomeIcons() {
    for _theme in ${THEMES}; do
	if [ -d ${SHARE_ICONS}/${_theme} ]; then
	    for _res in ${RESOLUTIONS}; do
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/apps
		for _icon in ${APPS_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/apps/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
		done
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/mimetypes
		for _icon in ${MIME_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/mimetypes/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
		done
	    done
	    UpdateIconCache ${SHARE_ICONS}/${_theme}
	fi
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    cp -f ${JDK_ICONS}/${HICOLOR}/48x48/apps/${_icon} \
		  ${SHARE_PIXMAPS}/${_icon}
	done
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${TEXT_ICON} \
	      ${SHARE_PIXMAPS}/x-java.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JAR_ICON} \
	      ${SHARE_PIXMAPS}/x-java-archive.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JNLP_ICON} \
	      ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
RemoveGnomeIcons() {
    for _theme in ${THEMES}; do
	for _res in ${RESOLUTIONS}; do
	    for _icon in ${APPS_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
	    done
	    for _icon in ${MIME_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
	    done
	done
	UpdateIconCache ${SHARE_ICONS}/${_theme}
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    rm -f ${SHARE_PIXMAPS}/${_icon}
	done
	rm -f ${SHARE_PIXMAPS}/x-java.png
	rm -f ${SHARE_PIXMAPS}/x-java-archive.png
	rm -f ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
InstallGnomeDesktop() {
    _file=$1
    mkdir -p ${SHARE_APPS}
    cp -f ${JDK_APPS}/${_file} ${SHARE_APPS}/${_file}
    if [ "${_file}" = "sun_java.desktop" ]; then
	if [ -d ${SHARE_CAPPLETS} ]; then
	    cp -f ${JDK_APPS}/${_file} ${SHARE_CAPPLETS}/${_file}
	fi
    fi
}
RemoveGnomeDesktop() {
    _file=$1
    rm -f ${SHARE_APPS}/${_file}
    rm -f ${SHARE_CAPPLETS}/${_file}
}
InstallLegacyMimetype() {
    _mime_type=$1
    _extension=$2
    _name=$3
    _command=$4
    _icon=$5
    _description=$6
    cat <<- end_of_keys_file > ${SHARE_MIME_INFO}/${_name}.keys
	${_mime_type}:
	    description=${_description}
	    icon_filename=${_icon}
	    default_action_type=application
	    default_application_id=${_name}
	    short_list_application_user_additions=${_name}
	end_of_keys_file
    cat <<- end_of_mime_file > ${SHARE_MIME_INFO}/${_name}.mime
	${_mime_type}
	    ext: ${_extension}
	end_of_mime_file
    cat <<- end_of_apps_file > ${SHARE_APP_REGISTRY}/${_name}.applications
	${_name}
	    command=${_command}
	    name=${_name}
	    can_open_multiple_files=false
	    requires_terminal=false
	    mime_types=${_mime_type}
	end_of_apps_file
}
RemoveLegacyMimetype() {
    _name=$1
    rm -f ${SHARE_MIME_INFO}/${_name}.keys
    rm -f ${SHARE_MIME_INFO}/${_name}.mime
    rm -f ${SHARE_APP_REGISTRY}/${_name}.applications
}
InstallGnomeMimetypes() {
    if [ -d ${SHARE_MIME} ]; then
	cp -f ${JDK_MIME}/packages/x-java-archive.xml \
	      ${SHARE_MIME}/packages/x-java-archive.xml
	cp -f ${JDK_MIME}/packages/x-java-jnlp-file.xml \
	      ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    fi
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	mkdir -p ${SHARE_MIME_INFO}
	mkdir -p ${SHARE_APP_REGISTRY}
	InstallLegacyMimetype application/x-java-archive \
                 jar              \
                 java-archive     \
                 "java -jar"      \
                 x-java-archive.png     \
		 "Java Archive"
	InstallLegacyMimetype application/x-java-jnlp-file \
                 jnlp                \
                 java-web-start      \
                 javaws              \
                 x-java-jnlp-file.png        \
                 "Java Web Start Application"
    fi
}
RemoveGnomeMimetypes() {
    rm -f ${SHARE_MIME}/packages/x-java-archive.xml
    rm -f ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	RemoveLegacyMimetype java-archive
	RemoveLegacyMimetype java-web-start
    fi
}
IntegrateWithGnome() {
    InstallGnomeIcons
    InstallGnomeDesktop sun_java.desktop
    InstallGnomeDesktop sun-java.desktop
    InstallGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    InstallGnomeMimetypes
}
DisintegrateWithGnome() {
    RemoveGnomeIcons
    RemoveGnomeDesktop sun_java.desktop
    RemoveGnomeDesktop sun-java.desktop
    RemoveGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    RemoveGnomeMimetypes
}
    MOST_DIGITS="[1-9]"
ALL_DIGITS="[0-9]"
COUNTING_NUMBER="${MOST_DIGITS}${ALL_DIGITS}*\|0"
VALID_NON_NUMERIC="[-_.a-zA-Z]"
VALID_CHARS="[-_.a-zA-Z0-9]"
MAJOR_RULE="\(${MOST_DIGITS}${ALL_DIGITS}*\)"
MINOR_RULE="\(${COUNTING_NUMBER}\)"
MICRO_RULE="\(${COUNTING_NUMBER}\)"
UPDATE_RULE="\(${MOST_DIGITS}${ALL_DIGITS}\|0${ALL_DIGITS}\)"
NON_FCS_ID_RULE="\([a-zA-Z0-9]*\)"
MIN_VERSION_ID_RULE="${MAJOR_RULE}\.${MINOR_RULE}\.${MICRO_RULE}"
FCS_VERSION_ID_RULE="${MIN_VERSION_ID_RULE}\(_${UPDATE_RULE}\)\?"
VERSION_ID_RULE="${FCS_VERSION_ID_RULE}\(-${NON_FCS_ID_RULE}\)\?"
NAME_ID_RULE="${VALID_CHARS}*${VALID_NON_NUMERIC}"
KNOWN_GOOD_NAME_LIST="java jdk jre j2sdk j2re"
PRS_ERROR_BAD_PARAMS=2000
expand_version() {
    status=0
    if [ $# -eq 0 ]; then
        read release remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${release}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${release}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        release=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        \printf "\t expand_version\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        format="%d\t%d\t%d\t%d\n"
        echo ${release} | sed -e "s/_/\./g" | \
          awk -v format="${format}" 'BEGIN { FS = "." } { printf format, $1, $2, $3, $4 }'
    fi
    return ${status}
}
parse_release() {
    status=0
    if [ $# -eq 0 ]; then
        read string remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${string}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${string}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        string=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t parse_release %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        version_id=`expr "${string}" : "${NAME_ID_RULE}\(${VERSION_ID_RULE}\)\$"`
        if [ -n "${version_id}" ]; then
            name_id=`expr "${string}" : "\(${NAME_ID_RULE}\)${VERSION_ID_RULE}\$"`
            fcs_part=`expr "${string}" : "${NAME_ID_RULE}\(${FCS_VERSION_ID_RULE}\).*\$"`
            non_fcs_part=`expr "${version_id}" : "[^-]*-\(${NON_FCS_ID_RULE}\)\$"`
	    printf "%s\t%s\t%s\n" "${name_id}" "${fcs_part}" "${non_fcs_part}"
        fi
    fi
    return ${status}
}
UNKNOWN_NAME_WEIGHT=1000
get_name_weight() {
    status=0
    if [ "$1" = "-" ]; then
        read name good_names
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        else
            shift 1
            if [ $# -gt 0 ]; then
                good_names="$*"
            fi
            if [ -z "${name}" ]; then
                printf "Error: usage - function requires input!\n" >> /dev/stderr
                status=${PRS_ERROR_BAD_PARAMS}
            fi
        fi
    elif [ $# -gt 1 ]; then
        name=$1
        shift 1
        good_names="$*"
    else
        printf "Error: usage - function takes 2+ parameters:\n\n" >> /dev/stderr
        printf "\t get_name_weight %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -n "${good_names}" ]; then
            length=`expr length "${good_names}"`
            pos=`expr "${good_names}" : ".*\<${name}\>"`
            if [ ${pos} -gt 0 ]; then
                expr substr "${good_names}" 1 ${pos} | wc -w | tr -d "[:space:]"
            else
                echo ${UNKNOWN_NAME_WEIGHT}
            fi
        else
            echo ${UNKNOWN_NAME_WEIGHT}
        fi
    fi
    return ${status}
}
HAS_FCS_WEIGHT=0
HAS_ODD_FCS_WEIGHT=1
HAS_RC_WEIGHT=100
HAS_ODD_RC_WEIGHT=101
HAS_BETA_WEIGHT=300
HAS_ODD_BETA_WEIGHT=301
HAS_EA_WEIGHT=500
HAS_ODD_EA_WEIGHT=501
HAS_INTRNAL_WEIGHT=2000
HAS_VERY_ODD_WEIGHT=9999
get_non_fcs_weight() {
    status=0
    if [ $# -eq 0 ]; then
        read non_fcs_part remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${non_fcs_part}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        non_fcs_part=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t get_non_fcs_weight \n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -z "${non_fcs_part}" ]; then
            echo ${HAS_FCS_WEIGHT}
        else
            case "${non_fcs_part}" in
                fcs)
                    echo ${HAS_ODD_FCS_WEIGHT}
                    ;;
                rc)
                    echo ${HAS_RC_WEIGHT}
                    ;;
                rc[0-9] | rc[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "rc\([0-9]*\)$"`
                    echo `expr ${HAS_RC_WEIGHT} - ${count}`
                    ;;
                rc*)
                    echo ${HAS_ODD_RC_WEIGHT}
                    ;;
                beta)
                    echo ${HAS_BETA_WEIGHT}
                    ;;
                beta[0-9] | beta[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "beta\([0-9]*\)$"`
                    echo `expr ${HAS_BETA_WEIGHT} - ${count}`
                    ;;
                beta*)
                    echo ${HAS_ODD_BETA_WEIGHT}
                    ;;
                ea)
                    echo ${HAS_EA_WEIGHT}
                    ;;
                ea[0-9] | ea[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "ea\([0-9]*\)$"`
                    echo `expr ${HAS_EA_WEIGHT} - ${count}`
                    ;;
                ea*)
                    echo ${HAS_ODD_EA_WEIGHT}
                    ;;
                internal)
                    echo ${HAS_INTRNAL_WEIGHT}
                    ;;
                internal[0-9] | internal[0-9][0-9] | internal[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "internal\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                b[0-9] | b[0-9][0-9] | b[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "b\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                *)
                    echo ${HAS_VERY_ODD_WEIGHT}
                    ;;
            esac
        fi
    fi
    return ${status}
}
    get_path_weight() {
    good_list="$1"
    path=$2
    release=`basename ${path}`
    parts="`parse_release ${release}`"
    if [ $? -eq 0 ]; then
        name=`echo "${parts}" | cut -f1`
        version=`echo "${parts}" | cut -f2`
        non_fcs=`echo "${parts}" | cut -f3`
        if [ -n "${version}" ]; then
           v_weight=`echo ${version} | expand_version`
           n_weight=`echo ${name} | get_name_weight - "${good_list}"`
           o_weight=`echo ${non_fcs} | get_non_fcs_weight`
           printf "%4d  %4d  %4d  %4d  %4d  %4d  %s\n" \
                  ${v_weight} ${n_weight} ${o_weight} "${path}"
        fi
    fi
}
get_weighted_list() {
    good_list=
    verify=
    stdio=
    status=0
    check=true
    while [ -n "${check}" ]; do
        if [ $# -gt 0 ]; then
            case "$1" in
                -g)
                    good_list="$2"
                    shift 2
                    ;;
                --good-list=*)
                    length=`expr length "$1"`
                    remove=`expr \( length "--good-list=" \) + 1`
                    good_list="`expr substr \"$1\" ${remove} ${length}`"
                    shift 1
                    ;;
                -v | --verify)
                    verify=true
                    shift 1
                    ;;
                --)
                    shift 1
                    check=
                    ;;
                -)
                    shift 1
                    stdio=true
                    ;;
                -*)
                    printf "Error: usage - unknown parameter:\n\n" \
								>> /dev/stderr
                    printf "\t%s : %s\n" "$1" "$*"		>> /dev/stderr
                    status=${PRS_ERROR_BAD_PARAMS}
                    check=
                    ;;
                *)
                    check=
                    ;;
            esac
        else
            check=
        fi
    done
    if [ $# -eq 0 ] || [ -n "${stdio}" ]; then
        read line
        while [ -n "${line}" ]; do
            if [ -z "${verify}" ] || [ -f ${line}/bin/java ]; then
                get_path_weight "${good_list}" ${line}
            fi
            read line
        done
    fi
    while [ $# -gt 0 ]; do
        if [ -z "${verify}" ] || [ -f $1/bin/java ]; then
            get_path_weight "${good_list}" $1
        fi
        shift 1
    done
    return ${status}
}
_compare_java_by_weight() {
    compare=0
    if [ $# -ne 0 ]; then
        if [ $# -eq 1 ]; then
            compare=1
        else
            left=$1
            right=$2
            shift 2
            good="$*"
            list=`get_weighted_list --good-list="${good}" \
                    ${left} ${right} | sort -u -k1n -k2n -k3n -k4n -k5rn -k6rn`
            if [ `echo "${list}" | wc -l | tr -d "[:space:]"` -ne 1 ]; then
                compare=-1
                latest=`echo "${list}" | tail -n 1 | cut -c 37-`
                if [ "${left}" = "${latest}" ]; then
                    compare=1
                fi
            fi
        fi
    fi
    echo ${compare}
}
compare_java_by_version() {
    _compare_java_by_weight $1 $2
}
compare_java_by_release() {
    _compare_java_by_weight $1 $2 ${KNOWN_GOOD_NAME_LIST}
}
find_latest_release() {
    if [ -d /usr/java ]; then
        latest_release=`find /usr/java/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
    fi
    if [ -d "${RPM_INSTALL_PREFIX}" ] && \
       [ "/usr/java" != "${RPM_INSTALL_PREFIX}" ]
    then 
        prefix_release=`find ${RPM_INSTALL_PREFIX}/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
        if [ `compare_java_by_release ${latest_release} ${prefix_release}` -lt 0 ]; then
            latest_release=${prefix_release}
        fi
    fi
    echo ${latest_release}
}
get_javaws() {
    path=$1
    if [ `compare_java_by_version ${path} version-1.5.0` -ge 0 ] &&
       [ -f ${path}/bin/javaws ]
    then
        path=${path}/bin/javaws
    elif [ `compare_java_by_version ${path} version-1.4.2` -ge 0 ]; then
        if [ -f ${path}/jre/javaws/javaws ]; then
            path=${path}/jre/javaws/javaws
        elif [ -f ${path}/javaws/javaws ]; then
            path=${path}/javaws/javaws
        else
            path=
        fi
    else
        path=
    fi
    echo ${path}
}
    LINK_ERROR_BAD_PARAMS=3000
LINK_ERROR_DEAD_LINK=3001
LINK_ERROR_FILE_NOT_FOUND=3002
dereference() {
    status=0
    if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
        follow="--follow"
        shift 1
    fi
    if [ $# -ge 1 ]; then
        path="$*"
        if [ -e "${path}" ]; then
            parent="`cd \`dirname \"${path}\"\`; pwd`"
            child="`basename \"${path}\"`"
            if [ "${parent}" != "${child}" ]; then
                path="${parent}/${child}"
            fi
            if [ -h "${path}" ]; then
                path=`ls -l "${path}" | sed -e "s#^.*${path} -> ##"`
                if [ "`expr substr \"${path}\" 1 1`" != "/" ]; then
                    path="${parent}/${path}"
                fi
                if [ -n "${follow}" ]; then
                    path="`dereference ${follow} ${path}`"
                fi                    
            fi
        else
            status=${LINK_ERROR_FILE_NOT_FOUND}
        fi
    fi
    echo ${path}
    return ${status}
}
setup_latest_link() {
    latest=$1
    link=$2
    if [ -h "${link}" ]; then
        reference="`dereference --follow ${link}`"
        if [ $? -eq 0 ]; then
            update=`compare_java_by_release "${latest}" "${reference}"`
        else
            update=1
        fi
        if [ ${update} -gt 0 ]; then
            rm -f "${link}"
        fi
    fi
    if [ ! -e "${link}" ]; then
        ln -s "${latest}" "${link}"
    fi
}
setup_default_links() {
    if [ $# -ge 2 ]; then
        latest_link="$1"
        default_link="$2"
        if [ ! -e "${default_link}" ]; then
            ln -s "${latest_link}" "${default_link}"
        fi
    fi
    if [ $# -gt 3 ]; then
        bindir="$3"
        shift 3
        for file in $*; do
            reference="`dereference --follow ${bindir}/${file}`"
            if [ $? -ne 0 ]; then
                rm -f "${bindir}/${file}"
            fi
            source="${default_link}/bin/${file}"
            if [ "${file}" = "javaws" ]; then
                source="`get_javaws \"${default_link}\"`"
            fi
            if [ -n "${source}" ] && [ ! -e "${bindir}/${file}" ]; then
                ln -s "${source}" "${bindir}/${file}"
            fi
        done
    fi
}
cleanup_default_links() {
    if [ $# -ge 1 ]; then
        default_link=$1
        if [ $# -gt 2 ]; then
            bindir="$2"
            shift 2
            for file in $*; do
                reference="`dereference \"${bindir}/${file}\"`"
                if [ $? -ne 0 ] ||
                   [ "${reference}" = "${default_link}/bin/${file}" ]
                then
                    rm -f "${bindir}/${file}"
                fi
            done
        fi
        rm -f "${default_link}"
    fi
}

    #
    # The RPM update command installs a given version of a package, and then
    # uninstalls all other versions of a package.
    #
    # The command does the following:
    #
    #     1) Run the %pre for the package being installed
    #     2) Install the new package's files
    #     3) Run the %post for the package being installed
    #     4) Run the %preun for each package being uninstalled
    #     5) Delete any old files not overwitten by the package being installed
    #     6) Run the %postun for each package being uninstalled
    #
    # Note: Because each version of Java installs into its own unique directory,
    #       the only files in step 5 that might not be deleted are the files in
    #       /etc/.java/.systemPrefs that are used for the Preferences API.
    #
    # Note: The order described above is also the same order that occurs when a
    #       user installs a new version, then uninstalls an old version at a
    #       later date.  The only difference is the ammount of time that passes
    #       between steps 3 and 4.
    #
    # Because of this order, all changes made to the system by the package
    # being installed are made *before* any changes made by packages being
    # uninstalled. This means that it is important that the %preun and %postun
    # scriptlets are written in a way that does not break any integration just
    # setup by the new package.  This makes it very difficult to determine what
    # should and shouldn't be removed during %preun and %postun scriptlets.
    #
    # Packages written in the past have no idea what the future will hold.  This
    # is obvious, but it doesn't make it easy.  One option is to assume users
    # will always install newer versions over older versions, and will never
    # keep multiple versions of the same package installed at the same time.
    # This is actually the assumption that RPM is designed upon.
    #
    # However, the --force option can be used to force RPM to install an older
    # package; a so called downgrade.  In the past, Java RPM packages have
    # always attempted to provide special support for downgrades.  This can
    # cause a lot of trouble given the design of RPM.
    #
    # This spec follows the recomended RPM practice.  If the version being
    # uninstalled is not the latest version, then nothing is done.  However, if
    # the version being uninstalled is the latest, then anything setup by the
    # %post scriptlet that is not also tracked by the RPM database is removed.
    #
    # Unfortunately there are two damned kinds of Java installations for every
    # given release, i.e. a JDK and a JRE.  Because of this, it is possible that
    # this version being uninstalled is the latest version, and that the version
    # being left behind is the *same* version as this!
    #
    # In this case, it is necessary to fix anything just broken by the %preun
    # scriptlet.  This will only happen when the JDK is uninstalled, and the
    # JRE of the same version is still on the system.  For this, all that needs
    # to be done is to repair the default and latest links.

    #
    # Determine if a new latest link should be created.  This is done if
    # there is still an installed version of Java that is 1.6 up to the
    # the version of this package.
    #
    LATEST_JAVA_PATH="`find_latest_release`"
    if [ -n "${LATEST_JAVA_PATH}" ] &&
       [ `compare_java_by_version ${LATEST_JAVA_PATH} \
                                  version-1.6.0_26` -lt 0 ]
    then
        #
        # Only maintain the latest link if the latest version left on
        # the system is the ugly stepsister to this one, i.e. this is
	# the JDK, and the JRE of the same version remains.
        #
        # Note: if the latest is higher than the version of this
        #       package, then latest will either A) already exist,
        #       so there is nothing that needs to be done, or B) the
        #       latest link is no longer supported buy those versions,
        #       so this package shouldn't set it up.
        #
        setup_latest_link "${LATEST_JAVA_PATH}" "/usr/java/latest"
    fi

    if [ -z "${LATEST_JAVA_PATH}" ] ||
       [ `compare_java_by_version ${LATEST_JAVA_PATH} \
                                  version-1.6.0_26` -lt 0 ]
    then
        #
        # Only maintain the latest link if the latest version left on
        # the system is the ugly stepsister to this one, i.e. this is
	# the JDK, and the JRE of the same version remains.
        #
        # Note: again, the best policy is to assume that higher
        #       releases can take better care of themselves
        #

        #
        # Remove all system integration.
        #
        RemoveMailcap /etc/mailcap application/x-java-jnlp-file
        RemoveMimeTypes /etc/mime.types application/x-java-jnlp-file
	DisintegrateWithGnome
    fi

    if [ -n "${LATEST_JAVA_PATH}" ]; then
        #
        # We just removed the Prefernce API files, so restore them since there
        # is still a version of Java installed.
        #
        mkdir -p /etc/.java/.systemPrefs
        if [ -f /etc/.java/.systemPrefs/.system.lock.rpmsave ]; then
            mv /etc/.java/.systemPrefs/.system.lock.rpmsave \
               /etc/.java/.systemPrefs/.system.lock
        elif [ ! -f /etc/.java/.systemPrefs/.system.lock ]; then
            touch /etc/.java/.systemPrefs/.system.lock
        fi
        if [ -f /etc/.java/.systemPrefs/.systemRootModFile.rpmsave ]; then
            mv /etc/.java/.systemPrefs/.systemRootModFile.rpmsave \
               /etc/.java/.systemPrefs/.systemRootModFile
        elif [ ! -f /etc/.java/.systemPrefs/.systemRootModFile ]; then
            touch /etc/.java/.systemPrefs/.systemRootModFile
        fi
    fi

    if [ -e "/usr/java/latest" ]; then
        #
        # If the latest link exists, then make sure the default link exists.
        #
        # Note: instead of trying to determine whether or not the current latest
        #       installation is a JDK or a JRE, just assume it's a JDK.
        #
        setup_default_links "/usr/java/latest" "/usr/java/default" \
                            "/usr/bin" "java javaws jcontrol javac jar javadoc"

        #
        # If there is still an init script kicking around then restart/reinstall
        # it in case it was stopped/uninstalled during %preun.
        #
        if [ -x /etc/init.d/jexec ]; then
            #
            # Try to register the init script to the various run levels.  If
            # possible this is accomplished using an LSB defined install tool.
            # If that isn't available, then try to use chkconfig, which is
            # supported by Red Hat and Debian.  Otherwise it is up to the user
            # to get the script setup for their distribution.
            #
            if [ -x /usr/lib/lsb/install_initd ]; then
                /usr/lib/lsb/install_initd jexec > /dev/null 2>&1

                # start the service for the current session
                /etc/init.d/jexec start > /dev/null 2>&1
            elif [ -x /sbin/chkconfig ]; then
                /sbin/chkconfig --add jexec > /dev/null 2>&1

                # start the service for the current session
                /etc/init.d/jexec start > /dev/null 2>&1
            fi
        fi
    fi






%verifyscript -p /bin/sh
#
    # Make sure any new files are created with a secure access mask.  Do not use
    # chmod, since that would also change the rights of any existing files, and
    # we are only interested in setting the rights for new files.
    #
    umask 022

    #
    # The package assumes that Gnome is either installed, or going to be
    # installed, so if nothing currently exists, then install in the default
    # location.
    #
    # NOTE: These variables must be defined before all the shell function macros
    #       are included.
    #
    if [ -z "${GNOMEDIR}" ]; then
        GNOMEDIR=/usr
    fi

    #
    # RPM_INSTALL_PREFIX doesn't seem to be set by "alien" so the following
    # minor kludge allows some functionality on debian-like systems (such
    # a Ubuntu) which don't support packages.
    #
    if [ -z "${RPM_INSTALL_PREFIX}" ]; then
	RPM_INSTALL_PREFIX="/usr/java"
    fi

    #
    # Gross kludge for old SuSE distros: Even though they set the environment
    # variable GNOMEDIR to /opt/gnome, Gnome may really be in /opt/gnome2.
    # Go figure,... (I feel so unclean....)
    #
    if [ "${GNOMEDIR}" = "/opt/gnome" ] && [ -d "/opt/gnome2" ]; then
	GNOMEDIR="/opt/gnome2"
    fi

    INSTALL_JRE_PATH=${RPM_INSTALL_PREFIX}/jdk1.6.0_26
    if [ -e ${INSTALL_JRE_PATH}/jre/bin/java ]; then
	INSTALL_JRE_PATH=${INSTALL_JRE_PATH}/jre
    fi
    #
    # Add the shell function and related variables used by the verify script.
    #
    NS_COMMENT1="#--Netscape Communications Corporation MIME Information"
NS_COMMENT2="#Do not delete the above line. It is used to identify the file type."
NS_COMMENT3="#mime types added by Netscape Helper"
UpdateMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    command="$3"
    if [ -z "`grep -E \"^${mime_type}; ${command}$\" \"${mailcap_file}\" 2> /dev/null`" ]; then
        mc_comment="# Java Web Start"
        mc_text=
        if [ -w "${mailcap_file}" ]; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
        fi
        if [ -w "`dirname \"${mailcap_file}\"`" ]; then
            mc_text="${mc_text:+${mc_text}\n}${mime_type}; ${command}"
            printf "%s" "${mc_text}" > "${mailcap_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mailcap_file}"
            echo "Check permissions."
        fi
    fi
}
RemoveMailcap() {
    mailcap_file="$1"
    mime_type="$2"
    mc_comment="# Java Web Start"
    if [ -w "${mailcap_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mailcap_file}\"`" ] ; then
            regexp="(${mime_type})|(${mc_comment})"
            mc_text=`grep -Ev "${regexp}" "${mailcap_file}"`
            if [ `echo "${mc_text}" | tr -d '[:space:]' | wc -c` -gt 0 ]; then
                echo "${mc_text}" > "${mailcap_file}"
            else
                rm -f "${mailcap_file}"
            fi
        fi
    fi
}
UpdateMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    desc="$3"
    shift 3
    exts="$*"
    JNLP_ENTRY="type=${mime_type} desc=\"${desc}\" exts=\"${exts}\""
    if [ ! -w "${mime_file}" ]; then
        if [ -w `dirname ${mime_file}` ]; then
            echo "${NS_COMMENT1}"  > "${mime_file}"
            echo "${NS_COMMENT2}" >> "${mime_file}"
            echo "${NS_COMMENT3}" >> "${mime_file}"
        else
            echo "WARNING - cannot write to file:"
            echo "       ${mime_file}"
            echo "Check permissions."
            return
        fi
    fi
    if [ -z "`grep -E \"^[^#]*${mime_type}\" \"${mime_file}\"`" ]; then
        echo ${JNLP_ENTRY} >> "${mime_file}"
    fi
}
RemoveMimeTypes() {
    mime_file="$1"
    mime_type="$2"
    if [ -w "${mime_file}" ]; then
        if [ -n "`grep \"${mime_type}\" \"${mime_file}\"`" ]; then
            regexp="(${mime_type})|(^${NS_COMMENT1}$)|(^${NS_COMMENT2}$)|(^${NS_COMMENT3}$)"
            if [ `grep -Ev "${regexp}" "${mime_file}" | \
                 tr -d '[:space:]' | wc -c` -gt 0 ]
            then
                mt_text="`grep -v \"${mime_type}\" \"${mime_file}\"`"
                echo "${mt_text}" > "${mime_file}"
            else
                rm -f "${mime_file}"
            fi
        fi
    fi
}
    JDK_DESKTOP="${INSTALL_JRE_PATH}/lib/desktop"
JDK_ICONS="${JDK_DESKTOP}/icons"
JDK_APPS="${JDK_DESKTOP}/applications"
JDK_MIME="${JDK_DESKTOP}/mime"
SHARE_PATH="${GNOMEDIR}/share"
SHARE_ICONS="${SHARE_PATH}/icons"
SHARE_MIME="${SHARE_PATH}/mime"
SHARE_APPS="${SHARE_PATH}/applications"
HICOLOR=hicolor
HIGHCONTRAST=HighContrast
HIGHCONTRASTINVERSE=HighContrastInverse
LOWCONTRAST=LowContrast
THEMES="${HICOLOR} ${HIGHCONTRAST} ${HIGHCONTRASTINVERSE} ${LOWCONTRAST}"
RESOLUTIONS="16x16 48x48"
TEXT_ICON="gnome-mime-text-x-java.png"
JAR_ICON="gnome-mime-application-x-java-archive.png"
JNLP_ICON="gnome-mime-application-x-java-jnlp-file.png"
JAVA_ICON="sun-java.png"
JAVAWS_ICON="sun-javaws.png"
JCONTROL_ICON="sun-jcontrol.png"
APPS_ICONS="${JAVA_ICON} ${JAVAWS_ICON} ${JCONTROL_ICON}"
MIME_ICONS="${TEXT_ICON} ${JAR_ICON} ${JNLP_ICON}"
ICONS="${APPS_ICONS} ${MIME_ICONS}"
GNOME_UTILS_DIRS="/usr/bin /opt/gnome/bin"
UPDATE_MIME_DATABASE="update-mime-database"
UPDATE_DESKTOP_DATABASE="update-desktop-database"
GTK_UPDATE_ICON_CACHE="gtk-update-icon-cache"
SHARE_CONTROL_CENTER="${SHARE_PATH}/control-center-2.0"
SHARE_CAPPLETS="${SHARE_CONTROL_CENTER}/capplets"
SHARE_MIME_INFO="${SHARE_PATH}/mime-info"
SHARE_APP_REGISTRY="${SHARE_PATH}/application-registry"
SHARE_PIXMAPS="${SHARE_PATH}/pixmaps"
UpdateIconCache() {
    _icon_theme_root=$1
    if [ -f ${_icon_theme_root}/icon-theme.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${GTK_UPDATE_ICON_CACHE} ]; then
		${_dir}/${GTK_UPDATE_ICON_CACHE} ${_icon_theme_root} \
		    > /dev/null 2>&1
		break
	    fi
	done
	touch ${_icon_theme_root}
	for _dir in ${RESOLUTIONS}; do
	    if [ -d ${_icon_theme_root}/${_dir} ]; then
		touch ${_icon_theme_root}/${_dir}
	    fi
        done
    fi
}
UpdateDesktopDatabase() {
    _desktop_root=$1
    if [ -f ${_desktop_root}/mimeinfo.cache ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_DESKTOP_DATABASE} ]; then
		${_dir}/${UPDATE_DESKTOP_DATABASE} ${_desktop_root} \
		   > /dev/null 2>&1
		break
	    fi
	done
    fi
}
UpdateMimeDatabase() {
    _mime_root=$1
    if [ -d ${_mime_root}/packages ]; then
	for _dir in ${GNOME_UTILS_DIRS}; do
	    if [ -x ${_dir}/${UPDATE_MIME_DATABASE} ]; then
		${_dir}/${UPDATE_MIME_DATABASE} ${_mime_root} > /dev/null 2>&1
		break
	    fi
	done
    fi
}
InstallGnomeIcons() {
    for _theme in ${THEMES}; do
	if [ -d ${SHARE_ICONS}/${_theme} ]; then
	    for _res in ${RESOLUTIONS}; do
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/apps
		for _icon in ${APPS_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/apps/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
		done
		mkdir -p ${SHARE_ICONS}/${_theme}/${_res}/mimetypes
		for _icon in ${MIME_ICONS}; do
		    cp -f ${JDK_ICONS}/${_theme}/${_res}/mimetypes/${_icon} \
			  ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
		done
	    done
	    UpdateIconCache ${SHARE_ICONS}/${_theme}
	fi
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    cp -f ${JDK_ICONS}/${HICOLOR}/48x48/apps/${_icon} \
		  ${SHARE_PIXMAPS}/${_icon}
	done
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${TEXT_ICON} \
	      ${SHARE_PIXMAPS}/x-java.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JAR_ICON} \
	      ${SHARE_PIXMAPS}/x-java-archive.png
	cp -f ${JDK_ICONS}/${HICOLOR}/48x48/mimetypes/${JNLP_ICON} \
	      ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
RemoveGnomeIcons() {
    for _theme in ${THEMES}; do
	for _res in ${RESOLUTIONS}; do
	    for _icon in ${APPS_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/apps/${_icon}
	    done
	    for _icon in ${MIME_ICONS}; do
		rm -f ${SHARE_ICONS}/${_theme}/${_res}/mimetypes/${_icon}
	    done
	done
	UpdateIconCache ${SHARE_ICONS}/${_theme}
    done
    if [ -d ${SHARE_PIXMAPS} ]; then
	for _icon in ${APPS_ICONS}; do
	    rm -f ${SHARE_PIXMAPS}/${_icon}
	done
	rm -f ${SHARE_PIXMAPS}/x-java.png
	rm -f ${SHARE_PIXMAPS}/x-java-archive.png
	rm -f ${SHARE_PIXMAPS}/x-java-jnlp-file.png
    fi
}
InstallGnomeDesktop() {
    _file=$1
    mkdir -p ${SHARE_APPS}
    cp -f ${JDK_APPS}/${_file} ${SHARE_APPS}/${_file}
    if [ "${_file}" = "sun_java.desktop" ]; then
	if [ -d ${SHARE_CAPPLETS} ]; then
	    cp -f ${JDK_APPS}/${_file} ${SHARE_CAPPLETS}/${_file}
	fi
    fi
}
RemoveGnomeDesktop() {
    _file=$1
    rm -f ${SHARE_APPS}/${_file}
    rm -f ${SHARE_CAPPLETS}/${_file}
}
InstallLegacyMimetype() {
    _mime_type=$1
    _extension=$2
    _name=$3
    _command=$4
    _icon=$5
    _description=$6
    cat <<- end_of_keys_file > ${SHARE_MIME_INFO}/${_name}.keys
	${_mime_type}:
	    description=${_description}
	    icon_filename=${_icon}
	    default_action_type=application
	    default_application_id=${_name}
	    short_list_application_user_additions=${_name}
	end_of_keys_file
    cat <<- end_of_mime_file > ${SHARE_MIME_INFO}/${_name}.mime
	${_mime_type}
	    ext: ${_extension}
	end_of_mime_file
    cat <<- end_of_apps_file > ${SHARE_APP_REGISTRY}/${_name}.applications
	${_name}
	    command=${_command}
	    name=${_name}
	    can_open_multiple_files=false
	    requires_terminal=false
	    mime_types=${_mime_type}
	end_of_apps_file
}
RemoveLegacyMimetype() {
    _name=$1
    rm -f ${SHARE_MIME_INFO}/${_name}.keys
    rm -f ${SHARE_MIME_INFO}/${_name}.mime
    rm -f ${SHARE_APP_REGISTRY}/${_name}.applications
}
InstallGnomeMimetypes() {
    if [ -d ${SHARE_MIME} ]; then
	cp -f ${JDK_MIME}/packages/x-java-archive.xml \
	      ${SHARE_MIME}/packages/x-java-archive.xml
	cp -f ${JDK_MIME}/packages/x-java-jnlp-file.xml \
	      ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    fi
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	mkdir -p ${SHARE_MIME_INFO}
	mkdir -p ${SHARE_APP_REGISTRY}
	InstallLegacyMimetype application/x-java-archive \
                 jar              \
                 java-archive     \
                 "java -jar"      \
                 x-java-archive.png     \
		 "Java Archive"
	InstallLegacyMimetype application/x-java-jnlp-file \
                 jnlp                \
                 java-web-start      \
                 javaws              \
                 x-java-jnlp-file.png        \
                 "Java Web Start Application"
    fi
}
RemoveGnomeMimetypes() {
    rm -f ${SHARE_MIME}/packages/x-java-archive.xml
    rm -f ${SHARE_MIME}/packages/x-java-jnlp-file.xml
    UpdateMimeDatabase ${SHARE_MIME}
    if [ -d ${SHARE_MIME_INFO} ] || [ -d ${SHARE_APP_REGISTRY} ]; then
	RemoveLegacyMimetype java-archive
	RemoveLegacyMimetype java-web-start
    fi
}
IntegrateWithGnome() {
    InstallGnomeIcons
    InstallGnomeDesktop sun_java.desktop
    InstallGnomeDesktop sun-java.desktop
    InstallGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    InstallGnomeMimetypes
}
DisintegrateWithGnome() {
    RemoveGnomeIcons
    RemoveGnomeDesktop sun_java.desktop
    RemoveGnomeDesktop sun-java.desktop
    RemoveGnomeDesktop sun-javaws.desktop
    UpdateDesktopDatabase ${SHARE_APPS}
    RemoveGnomeMimetypes
}
    MOST_DIGITS="[1-9]"
ALL_DIGITS="[0-9]"
COUNTING_NUMBER="${MOST_DIGITS}${ALL_DIGITS}*\|0"
VALID_NON_NUMERIC="[-_.a-zA-Z]"
VALID_CHARS="[-_.a-zA-Z0-9]"
MAJOR_RULE="\(${MOST_DIGITS}${ALL_DIGITS}*\)"
MINOR_RULE="\(${COUNTING_NUMBER}\)"
MICRO_RULE="\(${COUNTING_NUMBER}\)"
UPDATE_RULE="\(${MOST_DIGITS}${ALL_DIGITS}\|0${ALL_DIGITS}\)"
NON_FCS_ID_RULE="\([a-zA-Z0-9]*\)"
MIN_VERSION_ID_RULE="${MAJOR_RULE}\.${MINOR_RULE}\.${MICRO_RULE}"
FCS_VERSION_ID_RULE="${MIN_VERSION_ID_RULE}\(_${UPDATE_RULE}\)\?"
VERSION_ID_RULE="${FCS_VERSION_ID_RULE}\(-${NON_FCS_ID_RULE}\)\?"
NAME_ID_RULE="${VALID_CHARS}*${VALID_NON_NUMERIC}"
KNOWN_GOOD_NAME_LIST="java jdk jre j2sdk j2re"
PRS_ERROR_BAD_PARAMS=2000
expand_version() {
    status=0
    if [ $# -eq 0 ]; then
        read release remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${release}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${release}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        release=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        \printf "\t expand_version\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        format="%d\t%d\t%d\t%d\n"
        echo ${release} | sed -e "s/_/\./g" | \
          awk -v format="${format}" 'BEGIN { FS = "." } { printf format, $1, $2, $3, $4 }'
    fi
    return ${status}
}
parse_release() {
    status=0
    if [ $# -eq 0 ]; then
        read string remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -z "${string}" ]; then
            printf "Error: usage - function requires input!\n"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${string}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        string=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t parse_release %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        version_id=`expr "${string}" : "${NAME_ID_RULE}\(${VERSION_ID_RULE}\)\$"`
        if [ -n "${version_id}" ]; then
            name_id=`expr "${string}" : "\(${NAME_ID_RULE}\)${VERSION_ID_RULE}\$"`
            fcs_part=`expr "${string}" : "${NAME_ID_RULE}\(${FCS_VERSION_ID_RULE}\).*\$"`
            non_fcs_part=`expr "${version_id}" : "[^-]*-\(${NON_FCS_ID_RULE}\)\$"`
	    printf "%s\t%s\t%s\n" "${name_id}" "${fcs_part}" "${non_fcs_part}"
        fi
    fi
    return ${status}
}
UNKNOWN_NAME_WEIGHT=1000
get_name_weight() {
    status=0
    if [ "$1" = "-" ]; then
        read name good_names
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        else
            shift 1
            if [ $# -gt 0 ]; then
                good_names="$*"
            fi
            if [ -z "${name}" ]; then
                printf "Error: usage - function requires input!\n" >> /dev/stderr
                status=${PRS_ERROR_BAD_PARAMS}
            fi
        fi
    elif [ $# -gt 1 ]; then
        name=$1
        shift 1
        good_names="$*"
    else
        printf "Error: usage - function takes 2+ parameters:\n\n" >> /dev/stderr
        printf "\t get_name_weight %s\n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -n "${good_names}" ]; then
            length=`expr length "${good_names}"`
            pos=`expr "${good_names}" : ".*\<${name}\>"`
            if [ ${pos} -gt 0 ]; then
                expr substr "${good_names}" 1 ${pos} | wc -w | tr -d "[:space:]"
            else
                echo ${UNKNOWN_NAME_WEIGHT}
            fi
        else
            echo ${UNKNOWN_NAME_WEIGHT}
        fi
    fi
    return ${status}
}
HAS_FCS_WEIGHT=0
HAS_ODD_FCS_WEIGHT=1
HAS_RC_WEIGHT=100
HAS_ODD_RC_WEIGHT=101
HAS_BETA_WEIGHT=300
HAS_ODD_BETA_WEIGHT=301
HAS_EA_WEIGHT=500
HAS_ODD_EA_WEIGHT=501
HAS_INTRNAL_WEIGHT=2000
HAS_VERY_ODD_WEIGHT=9999
get_non_fcs_weight() {
    status=0
    if [ $# -eq 0 ]; then
        read non_fcs_part remainder
        status=$?
        if [ ${status} -ne 0 ]; then
            printf "Error(%s): failed to read!\n" "${status}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        elif [ -n "${remainder}" ]; then
            printf "Error: too many words read:\n\n"		>> /dev/stderr
            printf "\t%s %s\n" "${non_fcs_part}" "${remainder}"	>> /dev/stderr
            status=${PRS_ERROR_BAD_PARAMS}
        fi
    elif [ $# -eq 1 ]; then
        non_fcs_part=$1
    else
        printf "Error: usage - function takes 1 parameter:\n\n"	>> /dev/stderr
        printf "\t get_non_fcs_weight \n" "$*"			>> /dev/stderr
        status=${PRS_ERROR_BAD_PARAMS}
    fi
    if [ ${status} -eq 0 ]; then
        if [ -z "${non_fcs_part}" ]; then
            echo ${HAS_FCS_WEIGHT}
        else
            case "${non_fcs_part}" in
                fcs)
                    echo ${HAS_ODD_FCS_WEIGHT}
                    ;;
                rc)
                    echo ${HAS_RC_WEIGHT}
                    ;;
                rc[0-9] | rc[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "rc\([0-9]*\)$"`
                    echo `expr ${HAS_RC_WEIGHT} - ${count}`
                    ;;
                rc*)
                    echo ${HAS_ODD_RC_WEIGHT}
                    ;;
                beta)
                    echo ${HAS_BETA_WEIGHT}
                    ;;
                beta[0-9] | beta[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "beta\([0-9]*\)$"`
                    echo `expr ${HAS_BETA_WEIGHT} - ${count}`
                    ;;
                beta*)
                    echo ${HAS_ODD_BETA_WEIGHT}
                    ;;
                ea)
                    echo ${HAS_EA_WEIGHT}
                    ;;
                ea[0-9] | ea[0-9][0-9])
                    count=`expr "${non_fcs_part}" : "ea\([0-9]*\)$"`
                    echo `expr ${HAS_EA_WEIGHT} - ${count}`
                    ;;
                ea*)
                    echo ${HAS_ODD_EA_WEIGHT}
                    ;;
                internal)
                    echo ${HAS_INTRNAL_WEIGHT}
                    ;;
                internal[0-9] | internal[0-9][0-9] | internal[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "internal\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                b[0-9] | b[0-9][0-9] | b[0-9][0-9][0-9])
                    count=`expr "${non_fcs_part}" : "b\([0-9]*\)$"`
                    echo `expr ${HAS_INTRNAL_WEIGHT} - ${count}`
                    ;;
                *)
                    echo ${HAS_VERY_ODD_WEIGHT}
                    ;;
            esac
        fi
    fi
    return ${status}
}
    get_path_weight() {
    good_list="$1"
    path=$2
    release=`basename ${path}`
    parts="`parse_release ${release}`"
    if [ $? -eq 0 ]; then
        name=`echo "${parts}" | cut -f1`
        version=`echo "${parts}" | cut -f2`
        non_fcs=`echo "${parts}" | cut -f3`
        if [ -n "${version}" ]; then
           v_weight=`echo ${version} | expand_version`
           n_weight=`echo ${name} | get_name_weight - "${good_list}"`
           o_weight=`echo ${non_fcs} | get_non_fcs_weight`
           printf "%4d  %4d  %4d  %4d  %4d  %4d  %s\n" \
                  ${v_weight} ${n_weight} ${o_weight} "${path}"
        fi
    fi
}
get_weighted_list() {
    good_list=
    verify=
    stdio=
    status=0
    check=true
    while [ -n "${check}" ]; do
        if [ $# -gt 0 ]; then
            case "$1" in
                -g)
                    good_list="$2"
                    shift 2
                    ;;
                --good-list=*)
                    length=`expr length "$1"`
                    remove=`expr \( length "--good-list=" \) + 1`
                    good_list="`expr substr \"$1\" ${remove} ${length}`"
                    shift 1
                    ;;
                -v | --verify)
                    verify=true
                    shift 1
                    ;;
                --)
                    shift 1
                    check=
                    ;;
                -)
                    shift 1
                    stdio=true
                    ;;
                -*)
                    printf "Error: usage - unknown parameter:\n\n" \
								>> /dev/stderr
                    printf "\t%s : %s\n" "$1" "$*"		>> /dev/stderr
                    status=${PRS_ERROR_BAD_PARAMS}
                    check=
                    ;;
                *)
                    check=
                    ;;
            esac
        else
            check=
        fi
    done
    if [ $# -eq 0 ] || [ -n "${stdio}" ]; then
        read line
        while [ -n "${line}" ]; do
            if [ -z "${verify}" ] || [ -f ${line}/bin/java ]; then
                get_path_weight "${good_list}" ${line}
            fi
            read line
        done
    fi
    while [ $# -gt 0 ]; do
        if [ -z "${verify}" ] || [ -f $1/bin/java ]; then
            get_path_weight "${good_list}" $1
        fi
        shift 1
    done
    return ${status}
}
_compare_java_by_weight() {
    compare=0
    if [ $# -ne 0 ]; then
        if [ $# -eq 1 ]; then
            compare=1
        else
            left=$1
            right=$2
            shift 2
            good="$*"
            list=`get_weighted_list --good-list="${good}" \
                    ${left} ${right} | sort -u -k1n -k2n -k3n -k4n -k5rn -k6rn`
            if [ `echo "${list}" | wc -l | tr -d "[:space:]"` -ne 1 ]; then
                compare=-1
                latest=`echo "${list}" | tail -n 1 | cut -c 37-`
                if [ "${left}" = "${latest}" ]; then
                    compare=1
                fi
            fi
        fi
    fi
    echo ${compare}
}
compare_java_by_version() {
    _compare_java_by_weight $1 $2
}
compare_java_by_release() {
    _compare_java_by_weight $1 $2 ${KNOWN_GOOD_NAME_LIST}
}
find_latest_release() {
    if [ -d /usr/java ]; then
        latest_release=`find /usr/java/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
    fi
    if [ -d "${RPM_INSTALL_PREFIX}" ] && \
       [ "/usr/java" != "${RPM_INSTALL_PREFIX}" ]
    then 
        prefix_release=`find ${RPM_INSTALL_PREFIX}/* -prune | \
            get_weighted_list -v --good-list="${KNOWN_GOOD_NAME_LIST}" | \
            sort -k1n -k2n -k3n -k4n -k5rn -k6rn | tail -n 1 | cut -c 37-`
        if [ `compare_java_by_release ${latest_release} ${prefix_release}` -lt 0 ]; then
            latest_release=${prefix_release}
        fi
    fi
    echo ${latest_release}
}
get_javaws() {
    path=$1
    if [ `compare_java_by_version ${path} version-1.5.0` -ge 0 ] &&
       [ -f ${path}/bin/javaws ]
    then
        path=${path}/bin/javaws
    elif [ `compare_java_by_version ${path} version-1.4.2` -ge 0 ]; then
        if [ -f ${path}/jre/javaws/javaws ]; then
            path=${path}/jre/javaws/javaws
        elif [ -f ${path}/javaws/javaws ]; then
            path=${path}/javaws/javaws
        else
            path=
        fi
    else
        path=
    fi
    echo ${path}
}
    LINK_ERROR_BAD_PARAMS=3000
LINK_ERROR_DEAD_LINK=3001
LINK_ERROR_FILE_NOT_FOUND=3002
dereference() {
    status=0
    if [ "$1" = "-f" ] || [ "$1" = "--follow" ]; then
        follow="--follow"
        shift 1
    fi
    if [ $# -ge 1 ]; then
        path="$*"
        if [ -e "${path}" ]; then
            parent="`cd \`dirname \"${path}\"\`; pwd`"
            child="`basename \"${path}\"`"
            if [ "${parent}" != "${child}" ]; then
                path="${parent}/${child}"
            fi
            if [ -h "${path}" ]; then
                path=`ls -l "${path}" | sed -e "s#^.*${path} -> ##"`
                if [ "`expr substr \"${path}\" 1 1`" != "/" ]; then
                    path="${parent}/${path}"
                fi
                if [ -n "${follow}" ]; then
                    path="`dereference ${follow} ${path}`"
                fi                    
            fi
        else
            status=${LINK_ERROR_FILE_NOT_FOUND}
        fi
    fi
    echo ${path}
    return ${status}
}
setup_latest_link() {
    latest=$1
    link=$2
    if [ -h "${link}" ]; then
        reference="`dereference --follow ${link}`"
        if [ $? -eq 0 ]; then
            update=`compare_java_by_release "${latest}" "${reference}"`
        else
            update=1
        fi
        if [ ${update} -gt 0 ]; then
            rm -f "${link}"
        fi
    fi
    if [ ! -e "${link}" ]; then
        ln -s "${latest}" "${link}"
    fi
}
setup_default_links() {
    if [ $# -ge 2 ]; then
        latest_link="$1"
        default_link="$2"
        if [ ! -e "${default_link}" ]; then
            ln -s "${latest_link}" "${default_link}"
        fi
    fi
    if [ $# -gt 3 ]; then
        bindir="$3"
        shift 3
        for file in $*; do
            reference="`dereference --follow ${bindir}/${file}`"
            if [ $? -ne 0 ]; then
                rm -f "${bindir}/${file}"
            fi
            source="${default_link}/bin/${file}"
            if [ "${file}" = "javaws" ]; then
                source="`get_javaws \"${default_link}\"`"
            fi
            if [ -n "${source}" ] && [ ! -e "${bindir}/${file}" ]; then
                ln -s "${source}" "${bindir}/${file}"
            fi
        done
    fi
}
cleanup_default_links() {
    if [ $# -ge 1 ]; then
        default_link=$1
        if [ $# -gt 2 ]; then
            bindir="$2"
            shift 2
            for file in $*; do
                reference="`dereference \"${bindir}/${file}\"`"
                if [ $? -ne 0 ] ||
                   [ "${reference}" = "${default_link}/bin/${file}" ]
                then
                    rm -f "${bindir}/${file}"
                fi
            done
        fi
        rm -f "${default_link}"
    fi
}

    #
    # It isn't possible to repair any missing packed JAR files from --verify.
    # This is because the PACK source files are removed during post-install.
    # If an administrator needs to restore missing packed JAR files, they will
    # need to do a --reinstall.
    #

    #
    # If the package was relocated, then temporarily remove the /usr/java
    # link, but only if it really points to this package.
    #
    if [ "${RPM_INSTALL_PREFIX}" != "/usr/java" ] &&
       [ "`dereference --follow \"/usr/java/jdk1.6.0_26\"`" = "${RPM_INSTALL_PREFIX}" ]
    then
        rm -f "/usr/java/jdk1.6.0_26"
    fi

    #
    # Find out what version of Java is the latest.  Don't do any system
    # integration unless this is the latest version.  Otherwise, we make
    # it difficult for future installers.
    #
    LATEST_JAVA_PATH="`find_latest_release`"
    if [ "${LATEST_JAVA_PATH}" == "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" ] ||
       [ "${LATEST_JAVA_PATH}" == "/usr/java/jdk1.6.0_26" ]
    then
        #
        # Make sure the /usr/java/latest link points to LATEST_JAVA_PATH, and
	# update it if it doesn't.
        #
        setup_latest_link "${LATEST_JAVA_PATH}" "/usr/java/latest"

        #
        # Make sure the /usr/java/default and java javaws jcontrol javac jar javadoc exist.
	# If anything is missing, create it.
        #
        setup_default_links "/usr/java/latest" "/usr/java/default" \
                            "/usr/bin" java javaws jcontrol javac jar javadoc

        #
        # If the "latest" link is a JDK, then the latest JRE is a subdir;
	# otherwise it is the same dir.
        #
        DEFAULT_JRE_PATH="/usr/java/default"
        if [ -e "/usr/java/default/jre/bin/java" ]; then
            DEFAULT_JRE_PATH="/usr/java/default/jre"
        fi

	#
	IntegrateWithGNOME

        # setup the mailcap file
        UpdateMailcap /etc/mailcap application/x-java-jnlp-file "/usr/bin/javaws %s"

        # setup the mime.type file
        UpdateMimeTypes /etc/mime.types	application/x-java-jnlp-file \
			"Java Web Start" jnlp
    fi

    #
    # If the package is being relocated, then create a link in the default
    # location (/usr/java) to the actual install directory.  Do this
    # last, so it doesn't add unnecessary complexity to the search for the
    # latest release.
    #
    if [ "${RPM_INSTALL_PREFIX}" != "/usr/java" ] &&
       ( [ ! -e "/usr/java/jdk1.6.0_26" ] || [ -h "/usr/java/jdk1.6.0_26" ] )
    then
        rm -f "/usr/java/jdk1.6.0_26"
        ln -s "${RPM_INSTALL_PREFIX}/jdk1.6.0_26" "/usr/java/jdk1.6.0_26"
    fi

    #
    # There should be an init script for jexec on the system.  If it is, then
    # make sure it's installed and running
    #
    if [ -x /etc/init.d/jexec ]; then
        #
        # Try to register the init script to the various run levels.  If
	# possible this is accomplished using an LSB defined install tool.
	# If that isn't available, then try to use chkconfig, which is
	# supported by Red Hat and Debian.  The feature of automatic jar
	# file execution is not support on systems which don't support
	# either of these interfaces.
        #
        if [ -x /usr/lib/lsb/install_initd ]; then
            /usr/lib/lsb/install_initd jexec > /dev/null 2>&1

            # start the service for the current session
            /etc/init.d/jexec start > /dev/null 2>&1
        elif [ -x /sbin/chkconfig ]; then
            /sbin/chkconfig --add jexec > /dev/null 2>&1

            # start the service for the current session
            /etc/init.d/jexec start > /dev/null 2>&1
        fi
    fi




%changelog
* Thu Oct 06 2011 matyas - 1.6.0_26-fcs.1
- Specfile created from binary rpm /scratch/matyas/jdk/jdk-1.6.0_26-fcs.i586.rpm
