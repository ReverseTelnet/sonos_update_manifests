# Sonos Old Versions and Update Manifests

This repository contains archived Sonos Update Manifest Files that can be used to find old versions of Sonos Desktop Software and Device Firmware files.<br>
<br>
These old versions are served directly from sonos.com and not a third-party website.


## About Sonos Manifest Files (Update Manifests)

Sonos Update Manifests are XML Files and have a .upm extension.  Each Release Version has a dedicated Manifest File.  Contained in the file is metadata information about the Release such as the System Version and Software Generation along with a list of Sonos Models supported for that release.  For each supported model, the manifest file contains either an explicit or implicit download URL for that model.<br>

## Sonos Version Numbers

**See The Following:**<br>

- [Sonos Version Numbers - README](./docs/about_sonos_version_numbers.md)


## Sonos Device Firmware

**See The Following:**<br>

- [Sonos Model Numbers - README](./docs/about_sonos_model_numbers.md)


## Sonos Desktop Software

The Manifest Files contain explicit URLs for the Sonos Desktop software.  Rather than downloading old versions from questionable locations online, rolling the dice that the file hasn't been modified somehow or isn't just a straight-up malware, Sonos Desktop Software can be downloaded directly from the the original Sonos URLs.<br>

**See The Following:**<br>

- [Download Specific Desktop Version - Script](./download_specific_desktop_version.py)


## Sonos Mobile Software

With the rare exception of Beta Releases, the Mobile Software Downloads always link to their respective App-Store which will display the latest version.  To download old versions of Sonos iOS Software, [ipatool](https://github.com/majd/ipatool) is preferred.  To download old versions of Sonos Android Software, there are endless flavors of `'apk*'` style websites (apkpure/apkmirror, etc).  However, the downloaded file is generally an .apkm file that has to be re-merged into a single .apk file to be of any practical use.<br>

Alternatively, as of this writing, Sonos provides a [direct .apk download](https://www.sonos.com/redir/controller_software_android2) for FireOS.<br>


## Verifying Manifest Files

**See The Following:**<br>

- [Manifest File Verification - README](./docs/manifest_file_verification.md)
- [Verify Manifest Files - Script](./verify_manifest_files.py)
- [Extract Manifest Validator Public Keys - Script](./extract_manifest_validator_public_keys.py)


## New Manifest Files

The GitHub Actions Workflow will check for new Manifest Files once a day, ensuring this repository stays up to date.<br>
The script used to check for new Manifest Files can be run locally as well.<br>

**See The Following:**<br>

- [Check For New Manifest Files - Script](./check_for_new_manifest_files.py)


## Details on Running this Code

Create a Python Virtual Environment.<br>
There are too many cross-dependencies to take the risk of not running a Virtual Environment.<br>

### Python Version

This repository uses Python 3.14.7 as the development version.
This script _should_ generally work on Python 3.11.3 and above.

### Accessing These Files

Ideally **Clone** the repo rather than downloading it.

```git clone https://github.com/ReverseTelnet/sonos_update_manifests.git```

## Virtual Environment Creation

1. After cloning (or downloading), change directories into the folder.<br>
2. Create a Virtual Environment.<br>

    **Windows and macOS**:
    `python -m venv .venv`


3. Activate the Virtual Environment.

    **macOS**:
    `source .venv/bin/activate`


    **Windows (From Cmder or CMD, not Powershell or GitBash)**:
    `cd .venv/Scripts && activate && cd ../../`


4. Install Requirements File:
    `pip install -r requirements.txt`