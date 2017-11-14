from netmiko import ConnectHandler
from netmiko import BaseConnection
from netmiko import ssh_dispatcher


class SSHConnector(object):
    def __init__(self):
        self.last_octet = 82
        self.username = ''
        self.password = ''
        self.octets = 205
        self.model_prompt = True

        while True:
            self.username = raw_input("Enter your username:")
            if self.username in '/\*sql':
                print "Please enter a valid username"
            else:
                break

        while True:
            self.password = raw_input("Enter your password:")
            if self.password == '':
                print "Please enter a valid password"
            else:
                break

    def connect(self):
        while True:
            rs_prompt = raw_input("Are you configuring a router or a switch?:")
            if rs_prompt.lower() not in ('router', 'switch'):
                print("Not an appropriate choice.")
            elif rs_prompt.lower() == 'router':
                self.last_octet = 94
                break
            else:
                break

        while True:
            self.model_prompt = raw_input("Yes or No: limit this to Model-Office only?").lower().strip()
            if self.model_prompt not in ('y', 'yes', 'Yes', 'Y', 'n', 'no', 'No', 'N'):
                print "Enter a valid response"
            elif self.model_prompt in ('y', 'yes', 'Yes', 'Y'):
                self.model_prompt = True
                break
            elif self.model_prompt in ('n', 'no', 'No', 'N'):
                self.model_prompt = False
                break

    def choose_connections(self):
        if self.model_prompt:
            self.octets = ['205']
        else:
            self.octets = ['154','128','160','129','224','149','130','175','161','192','131','193','132','225',
          '133','226','162','163','227','164','148','165','228','134','229','230','195','135',
          '196','166','246','167','197','168','231','169','176','199','200','201','170','232',
          '233','171','172','173','234','153','235','202','152','137','138','174','247','204',
          '236','205','146','206','237','140','141','207','177','239','173','179','213','180',
          '210','240','211','241','181','142','242','150','182','244','143','183','144','184',
          '145','185','147']

        '''you will automatically be disconnected after entering your commands...I'm workin' on it'''

    def execute_commands(self):

        for i in self.octets:
            rtr = {
                'device_type': 'cisco_ios',
                'ip': '10.116.' + i + '.' + str(self.last_octet),
                'username': self.username,
                'password': self.password
            }

            rtr_connect = ConnectHandler(**rtr)

            print 'You are now connected to device(s) at' + str(self.octets)

            hostname = str(rtr_connect.find_prompt())
            # raw_command = raw_input("Enter the command:")
            # print "You sent " + raw_command
            output1 = rtr_connect.send_command('sh int counters | inc ( +0 +0 +0)')

            print hostname + ' data is being gathered'
            result = output1.split('\n')

            available = []

            count = 0
            for j in result:
                count += 1
                available.append(j)

            ports_available = (str(count / 2))


            int_file = open(hostname + '_' + ports_available + '_' + 'open_switchports.txt', 'w')
            int_file.write(hostname + ' has ' + ports_available + ' ports available.')
            for k in available:
                int_file.write(str(k) + '\n')
            int_file.close()

            print hostname + ' is complete, disconnecting'

            rtr_connect.disconnect()


connection = SSHConnector()
connection.connect()
connection.choose_connections()
connection.execute_commands()
