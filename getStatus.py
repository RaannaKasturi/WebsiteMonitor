import json

def run(code):
    code, webstatus, status, morestatus = getStatus(code)
    return code, webstatus, status, morestatus

def getStatus(code):
    with open('/home/user/app/status.json', 'r') as file:
        data = json.load(file)
        try:
            if code.startswith("2"):
                status = data['WebStatus']['Online']['SuccessfulConnection'][code]
                code = code
                webstatus = "Online"
                status = status
                morestatus = f"The website is currently functioning optimally and delivering content successfully."
                return code, webstatus, status, morestatus
            elif code.startswith("3"):
                status = data['WebStatus']['Online']['Redirection'][code]
                code = code
                webstatus = "Online"
                status = status
                morestatus = f"The website is employing a redirection mechanism to direct users to a different URL (Redirection code: {code})."
                return code, webstatus, status, morestatus
            elif code.startswith("4"):
                status = data['WebStatus']['Offline']['ClientError'][code]
                code = code
                webstatus = "Offline. Client-side Error or Unauthorization Error or Authentication Error."
                status = status
                morestatus = f"Website is offline due to a client-side error (Client Error code: {code}). This could be caused by an invalid request or issue with your browser."
                return code, webstatus, status, morestatus
            elif code.startswith("5"):
                status = data['WebStatus']['Offline']['ServerError'][code]
                code = code
                webstatus = "Offline"
                status = status
                morestatus = f"Website is offline due to a server-side error (Server Error code: {code}). This indicates an issue with the website itself or its infrastructure."
                return code, webstatus, status, morestatus
            else:
                return "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance.", "Invalid status code. Please contact us for assistance."
        except KeyError:
            return "abc.", "def.", "ghi.", "jkl."

if __name__ == "__main__":
    run()