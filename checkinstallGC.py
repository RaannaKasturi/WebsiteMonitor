import chrome_version
import subprocess

def checkGC(OS):
  while True:
    if OS == "linux":
      try:
        if chrome_version.get_chrome_version() == "":
          print("Chrome not found in system.\nInstalling Google Chrome . . .")
          installGC("linux")
          return True
        else:
          print("Chrome is installed.")
          return False
      except OSError:
        print("Unable to install chrome. Exiting...")
        return True
    elif OS == "windows":
      try:
        if chrome_version.get_chrome_version() == "":
            print("Chrome not found in system.\nInstalling Google Chrome . . .")
            installGC("windows")
            return True
        else:
            print("Chrome is installed.")
            return False
      except:
        print("Unable to install chrome. Exiting...")
        return True
    else:
      print("Unsupported OS. We are currently supported on Windows and Linux only.")
      exit()

def installGC(OS):
  if OS == "linux":
    cmd = subprocess.run(['sudo', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if cmd.returncode == 0:
      subprocess.run(['sudo', 'apt-get', 'update'])
      subprocess.run(['sudo', 'apt-get', 'install', '-y', 'wget', 'unzip'])
      subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
      subprocess.run(['sudo', 'apt-get', 'install', '-y', './google-chrome-stable_current_amd64.deb'])
      subprocess.run(['sudo', 'rm', 'google-chrome-stable_current_amd64.deb'])
      subprocess.run(['sudo', 'apt-get', 'clean'])
    else:
      subprocess.run(['apt-get', 'update'])
      subprocess.run(['apt-get', 'install', '-y', 'wget', 'unzip'])
      subprocess.run(['wget', 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb'])
      subprocess.run(['apt-get', 'install', '-y', './google-chrome-stable_current_amd64.deb'])
      subprocess.run(['rm', 'google-chrome-stable_current_amd64.deb'])
      subprocess.run(['apt-get', 'clean'])
  else:
    subprocess.run(['powershell', '-command', 'winget', 'install', 'Google.Chrome', '--force'])
