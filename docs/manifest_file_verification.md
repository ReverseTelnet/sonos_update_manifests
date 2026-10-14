# Manifest File Verification

This document explains the Signature in a Manifest File, how it is computed, and how it can be verified.<br>
This document also explains why you trust these XML files from a random repository on Github.<br>


## About the Manifest File Signature

Manifest Files are served over an `http` connection (no TLS).<br>
The Signature Line ensures the contents of the file are valid, accurate, and have not been tampered with in transit.<br>

The `<!-- SIGNATURE:` line in a Manifest File is an RSA Signature of the SHA256 hash.<br>


### Computing the Signature

1. SHA256 hash the manifest body, everything up to and including the newline before `<!-- SIGNATURE:`<br>
2. Sonos's Private Key is used to sign that SHA256 digest using RSA-2048 with PKCS1v15 padding.<br>
3. This results in a 256-byte (512 hex character) value in the `<!-- SIGNATURE:` line.<br>


## Automated Manifest File Verification

A simple Python Script can be used to hash the body of a Manifest File, then verify the RSA Signature against the hash using Public Keys.<br>

**See The Following:**<br>

- [Verify Manifest Files - Script](../verify_manifest_files.py)
- [Extract Manifest Validator Public Keys - Script](../extract_manifest_validator_public_keys.py)


## Manual Manifest FIle Verification

How can you trust these XML Files from a random repository on Github?<br>

   1. The desktop installer download URLs in the Manifest Files actually work, and they point to a direct link sonos.com.<br>
   2. Take any of the manifest filenames, and go to the links directly in your browser.<br>
      Simply follow this formula to get the Manifest File's URL.<br>

      ```python
      type_flag = Prod
      release_version = '85.0-64200-v17.0-2dVdiIkMSm-RC-1'
      f'http://update-firmware.sonos.com/firmware/{type_flag}/{manifest_file}/update.upm'
      ```

       **Notes:**
       1. To get the actual release version:<br>

           For each manifest filename, remove everything from the double underscore to the end of the filename.<br>
               `filename: 85.0-64200-v17.0-2dVdiIkMSm-RC-1__b056b08d274f4a56.upm`
               `version: 85.0-64200-v17.0-2dVdiIkMSm-RC-1`

       2. To get the type flag:<br>

            For each manifest file, look at the `sys_flag` at the top of the file.<br>
            The sys_flag indicates the type_flag that is needed.<br>
           - sys_flag 0x1 = Prod
           - sys_flag 0x3 = Dev

        ```xml
         <?xml version="1.0"?>
         <update_manifest version="1.1"
                          revision="cfc6ebad-a898-4573-abf8-a0cfaed9e8f8"
                          system_version="85.0-64200"
                          default_version="85.0-64200"
                          base_url="http://update-firmware.sonos.com/firmware/Dev/85.0-64200-v17.0-2dVdiIkMSm-RC-1/^85.0-64200"
                          sys_flags="0x3" <---- Type Flag = Dev
                          swgen="2">
           <supported_models>
        ```

       3. This same general method can be used for any of the links within a Manifest File.<br>

         ```xml
         <image model="22"
         fromver_max="54.2-71229"
         version="57.5-87010"
         flags="0x4" milestone_index="2">
         http://update-firmware.sonos.com/firmware/Prod/57.5-87010-v11.2.6-aocdfj-GA-1/^57.5-87010
         </image>                              Replace `^57.5-87010` with `update.upm`  ---^
         ```

       <br>
