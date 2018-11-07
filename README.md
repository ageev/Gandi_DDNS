# Gandi_DDNS
Short script to autoupdate Gandi's domain DNS record if dynamic IP is used

#How to use
1. Get Gandi's LiveDNS token from here:
*https://account.gandi.net/en/users/YOURUSERNAME/security
2. create/edit configuration file "gandi_ddns.cfg". Put your token there, domain and subdomain
  example:
  [local]
apikey = your_token
domain = domain.com
record = subdomain
api_url = https://dns.api.gandi.net/api/v5/
checker_url = https://api.ipify.org/
stored_external_ip = 0.0.0.0
  
3. use scheduler to run the script:
  sudo crontab -e
  */5 * * * * python /path/to/gandi-ddns.py
  
 #Links
 initial idea https://github.com/matt1/gandi-ddns
 Gandi API page https://doc.livedns.gandi.net/
