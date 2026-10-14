# About Sonos Version Numbers

This document explains Sonos Version numbers, comparing the System Version, Desktop Application Version, and Mobile Application Version.<br>


## Version Numbers

The word `Version` has a number of different meaning in the Sonos paradigm.<br>

To explain this, let's use the example [97.1-80312-v18.8](../manifest_files/97.1-80312-v18.8-jZ0oXJNpeN-RC-6__af15870f3a57a686.upm) which was released on 8 September 2026.<br>


### Sonos Devices

Sonos Devices use the term `System Version`.<br>
Sonos devices running this example version will display `97.1-80312`.<br>


### Sonos Desktop Applications

The macOS Desktop Application will display the Version and Build.<br>
Version: `17.2.3`<br>
Build: `79210`<br>


The Windows Desktop Application will display the Version and Build.<br>
Version: `17.2.1`<br>
Build: `67300`<br>


Wait... what? Why these versions?<br>

In the linked manifest file above, look at lines 18 and 24:<br>

```xml
<image model="3" ....>http://update-firmware.sonos.com/firmware/Prod/90.0-67300-v17.2.1-Lp7WoQPkxr-RC-1/90.0-67300-1-3.exe</image>
                                                                           ^^      ^^

<image model="4" ....>http://update-firmware.sonos.com/firmware/Prod/90.0-79210-v17.2.3-HBVQeC4A1l-RC-1/90.0-79210-1-4.dmg</image>
                                                                           ^^      ^^
```


### Sonos Mobile Applications

The Mobile Applications will display the full Build Number.<br>
Build: `89.01.10-release+20260907.42e3be3fe`<br>


### Release Version

Within the context of this repository, the Sonos Release Versions refer to the Version from the Update Manifest URL.<br>
Release Version: `97.1-80312-v18.8-jZ0oXJNpeN-RC-6`<br>

