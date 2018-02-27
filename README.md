# Cisco Firepower Migration Toolset
Cisco Firepower Migration Toolset
## Deletion of unused objects via Firepower Management Centre API
The file delete_unused_objects.py will allow you to interactively tidy up the FMC after a successful import (or tidy up FMC after a partial import etc).

Run this, enter the details in the prompts (currently only supports FMC via IP not via DNS) and choose your selection. It will then iterate through each item in the API and try and delete it. If it returns an error 500 it means it is in use or is protected (Cisco provided like any-ipv4 or any-ipv6).

*** NO WARRANTY IS PROVIDED OR IMPLIED, USE THIS AT YOUR OWN RISK AND IS NOT RECOMMENDED FOR PRODUCTION USE ***
