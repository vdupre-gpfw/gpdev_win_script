import sys
import os
import platform
import argparse
from shutil import copyfile


# Default arguments: can be modified to fit your working environment
fw_img_name = "DATA.bin"
host_os=platform.system()
if host_os == 'Windows':
    tmp_dir = 'C:/Users/vincent/AppData/Local/Temp/'
    default_fw_bin_path='C:/Users/vincent/Documents/' + fw_img_name
else:
    tmp_dir = '/tmp/'
    default_fw_bin_path='/home/vincent/' + fw_img_name

linux_src_path = "/home/vdupre/GIT/BANZAI_EP"
linux_machine = "vdupre@pluto"
default_host_ip='192.168.0.2'
default_target_ip='192.168.0.202'
default_pre_cmd  = 'ssh '+linux_machine+ ' "cd '+linux_src_path+'; make all GPDEV=1"'
default_pre_cmd += '&& scp '+linux_machine+':'+linux_src_path+'/waf_build/hero/build/eaglepeak/sd_fwupdate/'
default_pre_cmd += fw_img_name +' '+ default_fw_bin_path
default_shared_folder_path = 'C:/Users/vincent/Documents/nginx-1.17.6/html/'


# arguments parser
host_ip_help='IP address of the host with an optionnaly port number (X.X.X.X or X.X.X.X:port_number). Default '+default_host_ip
target_ip_help='IP address of the target (camera) with an optionnaly port number (X.X.X.X or X.X.X.X:port_number). Default '+default_target_ip
shared_folder_help = 'path to shared folder accessible via network (e;G nginx, nfs, etc...). Default '+default_shared_folder_path

parser=argparse.ArgumentParser(
    description='''Script to flash camera via network (usb / wifi). 
                   Be sure your camera is accessible from the host.''',
    epilog='''''')
parser.add_argument('--cmd', nargs='*', help='command to be executed before flashing the camera')
parser.add_argument('--bin', nargs='?', default=default_fw_bin_path
    , help='''path to the fw binary. Must include binary name. Default '''
    +default_fw_bin_path)
parser.add_argument('--host', nargs='?', default=default_host_ip, help=host_ip_help)
parser.add_argument('--target', nargs='?', default=default_target_ip, help=target_ip_help)
parser.add_argument('--shared_folder', nargs='?', default=default_shared_folder_path, help=shared_folder_help)
args=parser.parse_args()

#print args

if args.cmd != None:
    if not args.cmd:
        pre_cmd = default_pre_cmd
    else:
        pre_cmd = args.cmd[0]
    print "Execute pre command " + pre_cmd
    pre_cmd_ret = os.system(pre_cmd)
    if pre_cmd_ret == 0:
        print "pre command succeed!"
    else:
        print "pre command fail... error " + str(pre_cmd_ret)
        quit()



print("firmware flash executed on "+host_os)
print("\t- fw binaries:\t\t"+(args.bin))
print("\t- host ip:\t\t"+(args.host))
print("\t- target ip:\t\t"+(args.target))
print("\t- shared folder:\t"+(args.shared_folder))

# copy the binaries in the shared folder
print("copy binaries from "+args.bin+" to "+args.shared_folder)
copyfile(args.bin, args.shared_folder+fw_img_name)

# Create fw-flash.sh script that will be executed on the target to download fw binaries
print("fw-flash.sh script will be generated here: "+tmp_dir+"\n")
f=open(tmp_dir+"update.sh","wb+")

f.write(b'#!/bin/sh\n')
f.write(b'# Auto-generated script. Do not edit manually\n')
f.write(b'# -------------------------------------------\n')
f.write(b'\n')

f.write(b'export PATH=/usr/local/gopro/bin/:$PATH\n')
f.write(b'\n')
f.write(b'gpdevSendCmd init\n')
f.write(b'gpdevSendCmd TC \"t appc status disable\"\n')
f.write(b'sleep 2\n')
f.write(b'gpdevSendCmd IL\n')
f.write(b'\n')
f.write(b'echo \"[remote] Updating fw with file %s\"\n' % (args.bin))
f.write(b'gpdevFwupdate -a 73800000 -u \"http://%s' % (args.host))
f.write(b'/'+fw_img_name+'\"\n')
f.write(b'sleep 1\n')
f.write(b'echo \"[remote] Rebooting the platform\"\n')
f.write(b'gpdevSendCmd RB &\n')
f.close()

# send fw-flash.sh on the target and force the target to execute the script
print("[host] *** When target's root password is required, just hit enter ***\n")
cmd="scp "+tmp_dir+"update.sh root@"
cmd += args.target
cmd += ":/mnt/"
print(cmd)
ret = os.system(cmd)
if ret != 0:
    print "couldn't execute " + cmd + " (err = " + str(ret) + ")"
    quit()

print("[host] Running update script")
cmd  = 'ssh root@'
cmd += args.target
cmd += ' "chmod +x /mnt/update.sh && /bin/sh /mnt/update.sh"'
print(cmd)
ret = os.system(cmd)
if ret != 0:
    print "couldn't execute " + cmd + " (err = " + str(ret) + ")"
    quit()

print("[host] all done")
