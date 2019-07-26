# Gandi_DDNS
Short script to autoupdate Gandi's domain DNS record if dynamic IP is used

# How to use
1. Get Gandi's LiveDNS token from here:
https://account.gandi.net/en/users/YOURUSERNAME/security
2. create/edit configuration file "gandi_ddns.cfg". Put your token there, domain and subdomain
  example:
```
[local]
apikey = your_token
domain = domain.com
record = subdomain
api_url = https://dns.api.gandi.net/api/v5/
checker_url = https://api.ipify.org/
stored_external_ip = 0.0.0.0
```
3. use scheduler to run the script:
```
sudo crontab -e
*/5 * * * * python /path/to/gandi-ddns.py
```

## For ASUS routers with Merlin FW
```
admin@router:/tmp/home/root# cat /jffs/scripts/init-start
#!/bin/sh
# Script to update Gandi DNS
cru a gandi_ddns "*/15 * * * * cd /mnt/sda6/entware/var/opt/gandi_ddns && python gandi_ddns.py >> gandi_dns.log"
```
 # Links
 * initial idea https://github.com/matt1/gandi-ddns
 * Gandi API page https://doc.livedns.gandi.net/

#BONUS
## Gandi script to search for a short domain names - gandi_check_domain.py
https://github.com/ageev/others/blob/master/5_symbols_domains.log - example of the output
don't forget to put your token to gandi_check_domain.cfg (see .cfg file at the repo as an example. You need only token here)
