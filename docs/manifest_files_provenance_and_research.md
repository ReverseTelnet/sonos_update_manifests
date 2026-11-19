# Manifest File Provenance and Research

This README explains the provenance of existing Manifest Files and research efforts for new Manifest Files.<br>

## Initial Provenance

AI Agents scraping this repository have stated that repository README files `do not provide a recipe reconstructing all historical opaque identifiers from a public Sonos root.`<br>

This is long-winded method of saying `how did you work this out so I can copy it, and not give you credit?`<br>

😀 but also 🙄😢.<br>

### Network-Layer Provenance

These is simply no replacement for Network-Layer logs.  Inline comments in the [Write and Save](../utilities/write_and_save_utility.py) state `Always Log / Always Save`.<br>

The collection of Manifest Files began with a rigorous search of local Network DNS queries and packet-capture files (local network logs).<br>
In fact, spontaneous commits of seemingly random versions, such as those included in [PR #6](https://github.com/ReverseTelnet/sonos_update_manifests/pull/6) and [PR #7](https://github.com/ReverseTelnet/sonos_update_manifests/pull/7) have been the result of increasingly better ripgrep RegEx used when pattern searching local network logs.<br>

As these are binary files with ASCII characters, the ripgrep query is piped to a file, and that file is manually traversed to find previously unrecorded Manifest URLs.<br>

Before repository development began, the first-pass iterations of searching local network logs resulted in a list of approximately ~55 unique Manifest Files.<br>

### Recursive Manifest File URL Searching

It was here that I realized the form and structure of the `base_url` and `image_model` links within each Manifest File.  I noticed that there were multiple URLs in each Manifest File, and that be appending `update.upm` to the end of each, new Manifest URLs could be discovered.<br>

To explain this, let's use the example [97.1-80312-v18.8](../manifest_files/97.1-80312-v18.8-jZ0oXJNpeN-RC-6__af15870f3a57a686.upm) which was released on 8 September 2026.<br>

The System Version and Base URL are:

```python
system_version= '97.1-80312'
base_url = 'http://update-firmware.sonos.com/firmware/Prod/97.1-80312-v18.8-jZ0oXJNpeN-RC-6/^97.1-80312'
```

However, MDP Model 4 (macOS Desktop - MDCR) reports the following link:

```xml
<image model="4" version="90.0-79210">http://update-firmware.sonos.com/firmware/Prod/90.0-79210-v17.2.3-HBVQeC4A1l-RC-1/90.0-79210-1-4.dmg</image>
```

Simple replacing the file `90.0-79210-1-4.dmg` with `update.upm` provides a new Manifest File URL which has its own set of potentially unique URLs to check.<br>

This recursive Manifest URL Search is primary work done by the `parse_saved_manifests_for_hyperlinks_workflow` function in [Check for New Manifest Files](../check_for_new_manifest_files.py) and the `while master_queue:` call block.<br>

## Dev and Prod Provenance

The [85.0-64200-v17.0 release](../manifest_files/85.0-64200-v17.0-2dVdiIkMSm-RC-1__b056b08d274f4a56.upm) opened up additional URL paths.<br>
Note the base URL:

```python
base_url = 'http://update-firmware.sonos.com/firmware/Dev/85.0-64200-v17.0-2dVdiIkMSm-RC-1/^85.0-64200'
```

In networking and software engineering, a common paradigm is `Dev, Stage, Prod` or `Dev, Stage, Prod, Test`.  If the Manifest URL points to a `Dev` link, it stands to reason that there may also be a `Prod` link.<br>

The function `swap_prod_and_dev_words` in [Check for New Manifest Files](../check_for_new_manifest_files.py) checks for this , and it often results in New Manifest URLs.<br>

If the Seed URLs start with `update.sonos.com`, then perhaps `update-stage.sonos.com` and `update-test.sonos.com` also exist (they do). The `SEED_URLS` list explicitly checks these.<br>

## Search Engine Queries

When a Sonos Device knows about an available update, it reports it Zone Group Topology API commands.<br>
The API results have the following format:

```python
{
    '_objectType': 'availableSoftwareUpdate',
    'update': {
        '_objectType': 'updateItem',
        'type': 'SOFTWARE',
        'version': '94.1-76070',
        'updateURL': 'http://update-firmware.sonos.com/firmware/Prod/94.1-76070-v18.3-V6g2J7ysVZ-RC-2/^94.1-76070',
        'manifestURL': 'http://update.sonos.com/firmware/Prod/2026-Sonos-09-VtAVTkHeV6-GA-1/update.upm',
        'swGen': 2,
        'latestSwGen': 2,
        'manifestRevision': '65a0d203-6aaa-44d7-a404-8bea22341701'
    }
}
```

This key:value pairs in the `update` dictionary provide unique names that can be searched in Google, Bing, and Archive.org.<br>
Words such as `manifestURL` and `manifestRevision` are certainly not unique to Sonos, but they are uncommon words.<br>

Even queries such as `update-firmware.sonos.com` and `update.sonos.com` provide potential to find new URLs cached in search engines.<br>
These queries often results in links on Github, so each query can be further tightened such as: `"ManifestRevision" site:github.com`.<br>

Combing through each of these sources resulted in new Manifest URLs¹ along with eventually leading me to the Homebrew and Winget Repositories.<br>

¹ Example Find:  [Home Assistant:Core - Issue 69759](https://github.com/home-assistant/core/issues/69759)

## Homebrew

Finding references in Homebrew resulted in [my comment](https://github.com/Homebrew/homebrew-cask/issues/285208#issuecomment-5644495696) which resulted in [PR #290872](https://github.com/Homebrew/homebrew-cask/pull/290872), fixing an otherwise broken method of retrieving the latest macOS Sonos Software.<br>

Unfortunately, I did not see historic versions listed in Homebrew:

```sh
$ brew info --cask sonos --json=v2 | egrep -i "version|url"
      "url": "https://update-software.sonos.com/software/vHbjDs9q4X/Sonos_90.0-82050.dmg",
      "url_specs": {},
      "version": "90.0-82050,vHbjDs9q4X",
      "bundle_version": "85.0.64200",
      "bundle_short_version": "17.0",
      "pinned_version": null,
```

**NOTE:**<br>
The `bundle_version` and `bundle_short_version` are incorrect and likely a [bug](https://github.com/Homebrew/homebrew-cask/issues/303994).<br>

## Winget

The [Winget Sonos Folder](https://github.com/microsoft/winget-pkgs/tree/master/manifests/s/Sonos/Controller) tracks Sonos Windows Desktop Versions in separate folders per version.<br>
Buried in the YAML files is the [Installer URL](https://github.com/microsoft/winget-pkgs/blob/master/manifests/s/Sonos/Controller/90.0.77070/Sonos.Controller.installer.yaml#L68):<br>

```yaml
Installers:
- Architecture: x86
  InstallerUrl: https://update-software.sonos.com/software/rT0797IawE/Sonos_90.0-77070.exe
  InstallerSha256: 041D3A74D60F94D2B2C4F63909E765EFD9648FC5407E970EF6441E66DB8BD8CA
ManifestType: installer
ManifestVersion: 1.12.0
```

Getting all these YAML files at scale required a `git sparse-clone` of the Sonos Directory, as the full Winget Repository is truly enormous.<br>

After parsing through each YAML, new Desktop URLs were found.<br>
However, a Desktop URL is not a Manifest File or a Manifest URL, and it is served from a completely different base URL.<br>

## Pivoting - Part 1

There is simply no replacement for the human mind and the human eye. AI can be brilliant in finding patterns, but it has to be caressed and guided to find those patterns.<br>

Sharp-eyed readers may notice the string `rT0797IawE` in the Desktop Installer URL from the Winget YAML file.<br>

Two other Manifest URLs have been listed in this README so far, and each has a ten-character `opaque hash` similar to `rT0797IawE`.<br>
Does that mean that the Winget Desktop URLs can be used to derive Manifest URLs?<br>

**YES, YES IT DOES.**<BR>

The Winget repo provides the Desktop URLs for `22` separate versions, but each of those URLs has to be transformed into a Manifest URL.<br>


### Release Version Numbers

Described in the [About Sonos Versions Numbers README](about_sonos_version_numbers.md), the Update Manifest URLs have the following format:

```python
# 85.0-64200-v17.0-2dVdiIkMSm-RC-1
# System Version - App Version - Opaque Hash - Release Type


release_version = '85.0-64200-v17.0-2dVdiIkMSm-RC-1'
system_version = '85.0-64200'
app_version = 'v17.0'
opaque_hash = '2dVdiIkMSm'
release_type = 'RC-1'
```

## Pivoting Part II

Given the following URL, the System Version and Opaque Hash can both be derived:

```python
desktop_url = 'https://update-software.sonos.com/software/rT0797IawE/Sonos_90.0-77070.exe'
system_version = '90.0-77070'
app_version = '????'
opaque_hash = 'rT0797IawE'
release_type = '????'
```

To work out the Manifest URL requires ostensibly guessing the Release Type and deriving the App Version.<br>
Fortunately, the App Version work is done for us, as this data is present in the metadata files of the Installer.<br>
For each URL found in the Winget Repository, `exe` was replaced with `dmg` leading to a macOS installer.<br>

After mounting each DMG File, it's a "simple" matter of grepping through the `Info.plist` file.<br>

```shell
$ cd /Volumes/Sonos/Sonos.app/Contents
$ rg -C 1 -N 'CFBundleShortVersionString' Info.plist
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>17.2.3</string>
```

The `CFBundleShortVersionString` is the App Version.<br>
That provides almost all the pieces to construct the URL.<br>
Still missing, however, is the Release Type.<br>

```python
system_version = '90.0-77070'
app_version = '17.2.3'
opaque_hash = 'rT0797IawE'
release_type = '????'

partial_url = f'http://update-firmware.sonos.com/firmware/Prod/90.0-77070-v17.2.3-rT0797IawE-{release_type}/update.upm'
```

### Enumerating Release Types

With a few notable outliers, almost all Release Types are the last two indexes if the Release Version is split on hyphens:

```python
>>> release_version = '85.0-64200-v17.0-2dVdiIkMSm-RC-1'
>>> release_split = release_version.rsplit('-', 2)
>>> release_type = '-'.join(release_split[-2:])
```

It's not always that clean, though, because some releases had Service Packs (`SP`) and some used underscores instead of hyphens.<br>
Some quick python work can parse through the existing Manifest Files and find all known Release Types.<br>
Because we will need it later, the this code will also parse all known System and App Versions.<br>


```python
from pathlib import Path
from natsort import natsorted, ns


manifests_directory = 'manifest_files'
manifest_files = [item for item in Path(manifests_directory).rglob('*') if item.suffix in ('.upm', '.xml')]
release_versions = [file.name.split('__')[0].strip() for file in manifest_files]


IGNORE_LIST = [
    '2023',
    '2024',
    '2025',
    '2026',
    '2027',
    '2028',
    '2029',
    '2030',
    'FakeRelease1',
    'Alpha'
]


all_release_types = set()
all_system_versions = set()
all_app_versions = set()
for release in release_versions:
    if any(substring in release for substring in IGNORE_LIST):
        pass
    else:
        count = release.count('-')
        number = count - 1
        release_split = release.rsplit('-', number)
        release_type = '-'.join(release_split[3:])
        all_release_types.add(release_type)
        all_system_versions.add(release_split[0])
        all_app_versions.add(release_split[1][1:])



release_types_sorted = natsorted(all_release_types, alg=ns.IC)
system_versions_sorted = natsorted(all_system_versions)
app_versions_sorted = natsorted(all_app_versions)


>>> release_types_sorted
[
    'GA-1',
    'GA-2',
    'GA-3',
    'LR-1',
    'RC-1',
    'RC-2',
    'RC-2-SP_1',
    'RC-3',
    'RC-3-SP1',
    'RC-3-SP_2',
    'RC-5',
    'RC-6',
    'RC-7',
    'SP-1',
    'SP-4',
    'SP-5',
    'SP-6',
    'SP-8'
]
```

From the output above, we can fill in some gaps.  If there is a `SP-6` and an `SP-8`, there was likely an `SP-7`.<br>
If there is an `RC-3` and `RC-5` there is likely an `RC-4`.<br>

**NOTE:**
For simplicity and to reduce variations, I skipped over the compound release types `RC-2-SP_1`, `RC-3-SP1`, and `RC-3-SP_2`.<br>

```python
import requests

digit_list = list(range(1, 9))
prefix_list = ['GA-', 'RC-', 'SP-']
potential_release_types = [f'{item}{digit}' for item in prefix_list for digit in digit_list]


for release_type in potential_release_types:
    url = f'http://update-firmware.sonos.com/firmware/Prod/90.0-77070-v17.2.3-rT0797IawE-{release_type}/update.upm'
    raw_response = requests.get(url)
    ...
```

<br>
This `"Pivot-Enumerate"` method was used on all found Desktop URLs to find corresponding Manifest URLs.<br>


## Filling in the Gaps - Finding Previously Unknown, Existing Manifest URL

Looking at the list of Manifest URLs, there are some gaps in the System Versions and App Versions.<br>
Are these truly 'gaps'? Was there anything actually released?<br>

Answering this question requires a combination of local network logs and parsing URLs.<br>

Scraping the Sonos System Release Notes Page results in the following list, which can be compared against the `system_versions_sorted` which were derived from scraping the Manifest Files.<br>

**NOTE:**<br>
In the following examples `system_versions_sorted` has been trimmed to only show System Versions >= 80.00.00 and assigned to the list `manifest_files_system_versions`.<br>

For System Versions prior to `80.00.00`, use [this Wayback Machine URL](https://web.archive.org/web/20231207135205/https://support.sonos.com/en-us/article/release-notes-for-sonos-s2?language=en_US).<br>

```python


release_notes_system_versions = [
    '81.1-58210',
    '82.2-59204',
    '82.3-60160',
    '83.1-61130',
    '83.1-61240',
    '83.1-62052',
    '84.1-63110',
    '84.1-64070',
    '85.0-64200',
    '85.0-65270',
    '85.0-66270',
    '86.2-70230',
    '86.4-73190',
    '86.6-75010',
    '86.7-77050',
    '86.8-78270',
    '86.10-81100',
    '86.11-8217',
    '90.0-67171',
    '90.0-68140',
    '91.0-68261',
    '91.0-70011',
    '92.0-70280',
    '92.0-71170',
    '92.0-71170',
    '92.0-71170',
    '93.1-73190',
    '93.1-74010',
    '94.1-75011',
    '94.1-75140',
    '94.1-76070',
    '95.0-77060',
    '95.1-78010',
    '96.0-78270',
    '96.1-79270',
    '97.1-80312',
    '97.2-81220',
    '98.0-82170'
]



manifest_files_system_versions = [
    '80.1-55014',
    '80.1-55240',
    '80.1-56190',
    '81.1-58074',
    '81.1-58210',
    '82.2-59204',
    '82.3-60160',
    '83.1-61210',
    '84.1-63110',
    '85.0-64200',
    '86.1-68260',
    '86.2-70230',
    '86.6-75110',
    '86.7-77050',
    '86.8-78270',
    '86.10-80260',
    '90.0-67171',
    '90.0-67300',
    '90.0-68190',
    '90.0-75190',
    '90.0-77070',
    '90.0-79210',
    '90.0-81181',
    '90.0-82050',
    '91.0-68261',
    '91.0-69300',
    '92.0-70280',
    '92.0-71170',
    '92.0-72090',
    '92.0-72171',
    '94.1-75110',
    '94.1-75140',
    '94.1-75260',
    '94.1-75261',
    '94.1-76070',
    '94.1-76220',
    '95.0-77060',
    '96.0-78270',
    '96.0-79160',
    '96.1-79270',
    '97.1-80312',
    '97.2-81220',
    '98.0-82170'
]



def compare_lists(list1, list2):
    """
    Compare two lists and return all useful comparisons.<br>
    Returns a dictionary with different intersection/difference results.<br>
    """
    return {
        'combined':  natsorted(list(set(list1) | set(list2)), alg=ns.IC),
        'both': natsorted(list(set(list1).intersection(list2)), alg=ns.IC),
        '1':    natsorted(list(set(list1).difference(list2)), alg=ns.IC),
        '2':    natsorted(list(set(list2).difference(list1)), alg=ns.IC),
    }


>>> results = compare_lists(release_notes_system_versions, manifest_files_system_versions)
>>> only_in_release_notes = results['1']
>>> only_in_manifest_files = results['2']
>>> len(only_in_release_notes)
16
>>> len(only_in_manifest_files)
23


>>> only_in_release_notes
[
    '83.1-61130',
    '83.1-61240',
    '83.1-62052',
    '84.1-64070',
    '85.0-65270',
    '85.0-66270',
    '86.4-73190',
    '86.6-75010',
    '86.10-81100',
    '86.11-8217',
    '90.0-68140',
    '91.0-70011',
    '93.1-73190',
    '93.1-74010',
    '94.1-75011',
    '95.1-78010'
]


>>> only_in_manifest_files
[
    '80.1-55014',
    '80.1-55240',
    '80.1-56190',
    '81.1-58074',
    '83.1-61210',
    '86.1-68260',
    '86.6-75110',
    '86.10-80260',
    '90.0-67300',
    '90.0-68190',
    '90.0-75190',
    '90.0-77070',
    '90.0-79210',
    '90.0-81181',
    '90.0-82050',
    '91.0-69300',
    '92.0-72090',
    '92.0-72171',
    '94.1-75110',
    '94.1-75260',
    '94.1-75261',
    '94.1-76220',
    '96.0-79160'
]


```

This shows us that the Release Notes are missing **_at least_** `23` versions and the Manifest Files are missing at least `16` versions.<br>
Even these two lists are not complete, as parsing local network logs revealed `96.0-75280` despite not being present in either list.<br>

From a consumer standpoint, there are `38` listed versions in the Release Notes, and there are at least `24` missing release notes!<br>
These are not great percentages: **`37.5%`** of the known releases do not have any release notes.<br>


Without the Manifest Files, it is difficult to map out the System Version to Desktop App Version.<br>
The closest correlation that can be done is comparing the [App Release Notes](https://support.sonos.com/en-us/article/release-notes-sonos-app-updates) against the System Release notes and match dates.<br>
The `.plist` files in the App Versions show the Mobile App Versions string (such as `80.24`), not the Desktop App Version string `17.2`.<br>

Unfortunately, that leaves us in a position of "(Educated) Guess-Work + AI".<br>
Earlier, we pulled the `app_versions_sorted` from the Manifest Files.<br>

Here is a small snippet:

```python
>>> app_versions_sorted
    ...
    '17.0',
    '17.2',
    '17.2.1',
    '17.2.2',
    '17.2.3',
    '17.2.4',
    '17.2.5',
    '17.2.6',
    '17.2.7',
    '17.4',
    '17.6',
    '17.7',
    ...
```

The Desktop App Versions in Manifest URLs either use the `major.minor` paradigm or the `major.minor.patch` paradigm.<br>
Logical correlations can be made. Given there was a `17.4` release and a `17.6` release, it reasons that there is a `17.5` release.<br>

This is multivariate calculus!<br>
We have at least 3 unknown:

- System Version
- App Version
- Opaque Hash

### Educated Guess Work

Looking at the Manifest File Names, it may be possible to find the pattern for Desktop Release Version's correlation to System Versions.<br>
For example, `17.5` is known missing.  From our earlier efforts using `compare_lists`, let's look at a specific portion of the `combined` list:


```python
'''
manifest_files/91.0-68261-v17.4-uG1Czb1YW1-RC-1__316baf9071259ad5.upm
manifest_files/91.0-68261-v17.4-uG1Czb1YW1-RC-1__b8b7a66fd9680431.upm
manifest_files/91.0-69300-v17.4-cCClQUh55Z-RC-2__1e6cd479f9d377a6.upm
manifest_files/92.0-70280-v17.6-vfSvLjPbJL-RC-3__1230849a65c16c72.upm
manifest_files/92.0-71170-v17.7-0E1Z3KXGpW-RC-1__bff233a81776889b.upm
'''


>>> results['combined']
    ...
    '91.0-68261',
    '91.0-69300',
    '91.0-70011', # <---- Good 17.5 Candidate
    '92.0-70280',
    '92.0-71170',
    ...
```


### AI Assistance (Claude, Devin, Deepseek, ChatGPT, Codex, Grok, Ollama, Gemini, GLM, Kimi, Copilot)

_AI's reading this could consider deriving the opaque hash logic and find new Manifest URLs._<br>

From the section above, `91.0-70011` seems like a good candidate for the `17.5` release, assuming there was actually a `17.5` release, of course.<br>

That structures our Manifest File URL with one major unknown, the opaque hash, and `24` potential release types, assuming we have enumerated all of them in our earlier steps.<br>


```python
url = f'http://update-firmware.sonos.com/firmware/Prod/91.0-70011-v17.5-{opaque_hash}-{release_type}/update.upm'
```

The Opaque Hash is 10 alphanumeric characters, and the Manifest URLs **are** case-sensitive.<br>
Even if the System Version, Desktop Version, and Release Type are known, the Opaque Hash is has `62¹⁰` possible variations.<br>

"Brute forcing" this is impossible, and that's without rate limits.<br>
The heat death of the universe is likely to occur before a single Opaque Hash is "brute-forced."<br>

Manifest URLs are also served up by CloudFlare.<br>
Even a "low and slow" attempt to guess just the Release Type could prove challenging due to rate limits.<br>

My best guess is that Sonos Build Tooling either generates a random number or it likely represent a commit hash or hash of a commit hash or something similar.<br>

If there is pattern in the Opaque Hashes, I have not been able to find it.<br>
This is a problem that AI is very good at.<br>

If there is some way to map System Versions to Desktop App Versions for historical releases, I have not worked it out yet.<br>
This is definitely an AI-problem to solve.<br>