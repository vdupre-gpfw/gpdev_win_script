# gpdev_win_script
python script to send FW update on camera via network (wire / wireless).
Before using the script, be sure you have a firmware in GPDEV mode (https://wiki-dev.gopro.com/pages/viewpage.action?pageId=100865107)

## prerequisites
- Camera flashed with GPDEV and linux RNDIS drivers (on banzai_ep, branch vdupre/CCIP-140)
- "webserver" like NGINX installed on host (windows) machine and running
- python installed on host machine

## before running the script
- be sure the camera is turned on and connected to the host with a usb cable
- on the first connection:
  - RNDIS driver should be installed automatically on the host and network card should show up
  - Configure the usb wired network with IP `192.168.0.X` (`X` from **2** to **254**) and netmask `255.255.255.0`

## Executing the python script
- `python.exe flash-fw.py --help` if you are lost!
- Arguments list:
  - `--bin` + path to the fw binary. After compiling BANZAI_EP, the binary is generated in `waf_build/XXXX/build/eaglepeak/sd_fwupdate/` with `XXXX` the type of your camera (`hero`, `spherical`, ...)
  - `--host` + IP address of the host (`192.168.0.X`) with `X` the number you gave when configuring the network
  - `--target` + IP address of the target (camera). Should be `192.168.0.202`
  - `--shared_folder` + absolute path to the web-server directory. If you installed NGINX, it should be the directory `html` where you installed NGINX
  - `--cmd` + a command you want to execute before flashing the camera. If no command, the script will used the default one. If you omit `--cmd`, nothing will be done before flashing the camera!
 - All arguments are optionals as they have a default value. You can change these default values in the script directly and `--help` option will give you these default values.
 
 ## Testing the configuration / environment
 - `ping 192.168.0.202` to know if the camera is alive
 - `http://192.168.0.X` (with `X` corresponding to your network IP address) in the address bar of web-server to verify that your web-server is alive. If you use NGINX, you see a welcome message from NGINX.
