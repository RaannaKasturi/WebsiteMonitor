import requests

def getStatus(URL):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        webResponse = requests.get(URL, headers=headers)
        webCode = str(webResponse.status_code)
        code, status, webStatus, moreDetails = statusCodes(webCode)
        return code, status, webStatus, moreDetails
    except requests.ConnectionError:
        error = f"Failed to connect to {URL}"
        return error, error, error, error
    except requests.Timeout:
        error = f"Request to {URL} timed out"
        return error, error, error, error
    except requests.RequestException as e:
        error = f"An error occurred: {e}"
        return error, error, error, error
    
def statusCodes(code):
        try:
            if code.startswith("2"):
                status = f"Website is Online and Accessible"
                webStatus = f"The website is currently functioning optimally and delivering content successfully"
                moreDetails = f"https://httpstatuses.io/{code}"
                return code, status, webStatus, moreDetails
            elif code.startswith("3"):
                status = "Website Online, but Redirecting"
                webStatus = f"The website is employing a redirection mechanism to direct users to a different URL (Redirection code: {code})."
                moreDetails = f"https://httpstatuses.io/{code}"
                return code, status, webStatus, moreDetails
            elif code.startswith("4"):
                status = "Website Online, but Inaccessible. Client-side Error or Unauthorization Error or Authentication Error"
                webStatus = f"Website is inaccessible due to a client-side error (Client Error code: {code}). This could be caused by an invalid request or the website is protected by captcha or against bots. "
                moreDetails = f"https://httpstatuses.io/{code}"
                return code, status, webStatus, moreDetails
            elif code.startswith("5"):
                status = "Website Offline. Server-side Error"
                webStatus = f"Website is offline due to a server-side error (Server Error code: {code}). This could be caused by the issues with the website itself or its infrastructure."
                moreDetails = f"https://httpstatuses.io/{code}"
                return code, status, webStatus, moreDetails
            else:
                return "Unable to fetch website status. Please contact us for assistance", "Unable to fetch website status. Please contact us for assistance", "Unable to fetch website status. Please contact us for assistance", "Unable to fetch website status. Please contact us for assistance"
        except KeyError:
            return "Unable to fetch website status", "Unable to fetch website status", "Unable to fetch website status", "Unable to fetch website status"
