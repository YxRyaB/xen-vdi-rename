__author__ = 'yxryab'
# -*- coding: utf-8 -*-
import XenAPI
import optparse
import getpass
import logging

def renamevdi(session, VDIlist):
    def rename(vdi):
        if (vdi['Name'] + '_' + vdi['position']) == vdi['VDI']:
            logging.debug('VDI name matches a pattern renaming: %s_%s = %s' % (vdi['Name'], vdi['position'], vdi['VDI']))
        else:
            logging.debug('Renaming :VM_name: ' + vdi['Name'] + ' : ' + 'VDI_name: ' + vdi['VDI'] + ' : VDI_id: ' + vdi['VDIid'] + ' : position_in_VBD: ' + vdi['position'])
            #session.xenapi.VDI.set_name_label(vdi['VDIid'], '%s_%s' % (vdi['Name'], vdi['position']))

    for vdi in VDIlist:
        if 'False' == byname:
            rename(vdi)
        else:
            if byname == vdi['Name']:
                rename(vdi)

def getvdi(session):
    allvdis = session.xenapi.VDI.get_all()
    vdis = []
    for vdiss in allvdis:
        if not session.xenapi.VDI.get_is_a_snapshot(vdiss) \
        and session.xenapi.VDI.get_VBDs(vdiss):
            vdis.append(vdiss)
    vdiArray = []
    for vdi in vdis:
        VDIname = []
        VMname = []
        vdivbds = session.xenapi.VDI.get_VBDs(vdi)
        for vbd in vdivbds:
            vdivm = session.xenapi.VBD.get_VM(vbd)
            position = session.xenapi.VBD.get_userdevice(vbd)
            VMname = session.xenapi.VM.get_name_label(vdivm)
            if not 'CD' in session.xenapi.VBD.get_type(vbd) \
                and not 'Transfer' in VMname:
                VDIname = session.xenapi.VDI.get_name_label(vdi)
                data = {
                    "VDI": VDIname,
                    "Name": VMname,
                    "VDIid": vdi,
                    "position": position,
                }
                vdiArray.append(data)
    logging.info('Number of VDI %s' % len(vdiArray))
    for _vdi in vdiArray:
        vdi_list = sorted(vdiArray, key=lambda _vdi: _vdi['Name'])
    return vdi_list

def main():
    if 'DEBUG' == levelpars:
        logging.basicConfig(filename='xen_rename_VDI.log',
                            level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s  %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    elif 'INFO' == levelpars:
        logging.basicConfig(filename='xen_rename_VDI.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s  %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Started create session')
    try:
        url = 'https://' + str(server) + ':' + str(port)
        logging.debug('url: %s' % url)
        session = XenAPI.Session(url)
        session.xenapi.login_with_password(username, password, "1.0")
        logging.debug('Username: %s' % username)
    except XenAPI.Failure, e:
        if e.details[0] == 'HOST_IS_SLAVE':
            logging.info('Host is slave')
            session = XenAPI.Session('https://' + e.details[1])
            logging.debug('Url is: https://%s' % e.details[1])
            session.login_with_password(username, password)
        else:
            raise
    try:
        logging.info("Started create VDI list")
        VDIlist = getvdi(session)
        logging.info("Finished create VDI list")
        logging.info("Started rename VDIs")
        renamevdi(session, VDIlist)
        logging.info("Finished rename VDIs")
    except:
        session.logout()
        logging.info("Session closed")
    session.logout()
    logging.info("Session closed")

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [option] arg1 ...")
    parser.add_option("-s", "--server",
                      dest="server",
                      default="10.216.0.10",
                      type="string",
                      help="IP address of the server you want to connect")
    parser.add_option("-p", "--port",
                      dest="port",
                      default="443",
                      type="string",
                      help="Server port to connect to")
    parser.add_option("-w", "--password",
                      dest="password",
                      default=getpass.getpass('password: '),
                      type="string",
                      help="Password on the server")
    parser.add_option("-u", "--user",
                      dest="username",
                      default="root",
                      type="string",
                      help="Username on the server")
    parser.add_option("-n", "--by_name",
                      dest="nameVM",
                      default="False",
                      help='Change only in a particular VM VDI, example: -n "CentOS 6 test"')
    parser.add_option("-l", "--setlevel",
                      default="INFO",
                      dest="level",
                      choices = ("DEBUG", "INFO"),
                      help="Set the level of logging default is INFO. Possible options is DEBUG, INFO")
    (options, args) = parser.parse_args()
    server = options.server
    port = options.port
    username = options.username
    password = options.password
    byname = options.nameVM
    levelpars = options.level
    main()