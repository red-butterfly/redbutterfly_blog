#!/usr/bin/python
import os
import re


class SysInfo(object):

    def __init__(self):
        pass

    @property
    def cpumeminfo(self):
        """"
        get the cpu used and mem used info
        return (cpuuesd,memused,memtotal,memused%)
        """
        redinfo = os.popen('top -bi -n 2 -d 0.02').read()
        getcpu = re.findall(r'%Cpu.+',redinfo)
        getmem = re.findall(r'KiB Mem.+',redinfo)

        cpuinfo = re.search(r'%Cpu\(s\):\s*(.+)\s*us.+', getcpu[1])
        if cpuinfo:
            cpu = float(cpuinfo.group(1))

        meminfo = re.search(r'KiB Mem:\s*(\d*)\s*total,\s*(\d*)\s*used',getmem[1])
        if meminfo:
            mem = int( int(meminfo.group(2))*100 / int(meminfo.group(1)) )
        return (cpu,meminfo.group(2),meminfo.group(1),mem)

    @property
    def networkinfo(self):
        """"
        get all the network receive and transmit
        return ['eth0':['in':xxx,'out':xxx],.....]
        """
        f = open('/proc/net/dev','rb')
        devinfo = f.readlines()
        f.close()

        ret = {}
        item = {'in':0,'out':0}

        for line in devinfo:
            if line.find(':') > 0:
                line = line.replace(':',' ')
                items = line.split()
                item['in'] = long(items[1])
                item['out'] = long(items[len(items)/2 + 1])
                ret[items[0]] = item.copy()

        return ret

    @property
    def diskinfo(self):
        """
        get the disk info:available, capacity,used%
        return (free,total,used%)
        """
        disk = os.statvfs("/")
        free = disk.f_bsize * disk.f_bfree
        total = disk.f_bsize * disk.f_blocks
        uesd = 100 - free*100/total

        return (free,total,uesd)

def get_sysinfo():
    sysinfo = {}
    info = SysInfo()
    sysinfo['cpuused'], sysinfo['memused'], sysinfo['diskused'] = \
        str(info.cpumeminfo[0]), str(info.cpumeminfo[3]), str(info.diskinfo[2])
    return sysinfo

def test():
    sysinfo = SysInfo()
    print (sysinfo.cpumeminfo,sysinfo.diskinfo,sysinfo.networkinfo)

if __name__=='__main__':
    test()
