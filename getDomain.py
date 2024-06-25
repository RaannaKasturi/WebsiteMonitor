import tldextract
 
# Get URL from user
url = input("Enter URL: ")
 
# Extract information from URL
extracted_info = tldextract.extract(url)
 
# Print all extracted information
print("The result after extraction is:", extracted_info)
 
# Print only the domain name
print("Domain name is:", extracted_info.subdomain+"."+extracted_info.domain+"."+extracted_info.suffix)