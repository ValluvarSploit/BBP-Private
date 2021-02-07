# BBP-Private

# Web Screenshot:
   Workflow Name: web_screenshot.yml</br>
   Workflow Description: Take screenshot of given subdomains</br>
   Workflow Dependency: subdomain_enumeration.yml</br>
   
   # Example:
      1. TARGET_DOMAIN 
           example.com
      2. TARGET_SUBDOMAINS_LIST
           https://example.com
           https://info.example.com
                    
# XSS Hunt:
   Workflow Name: xss_hunter.yml</br>
   Workflow Description: Check for Cross-Site-Scripting(XSS) vulnerability for given urls.</br>
   Workflow Dependency: 
     subdomain_enumeration.yml</br>
     url_miner.yml</br>
   
   # Example:
      1. TARGET_DOMAIN 
           example.com
      2. TARGET_XSS_URLS_LIST
           https://example.com/image.php?q=FUZZ
           https://example.com/image.php?a=FUZZ
           
           

 
