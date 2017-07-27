#!/usr/bin/python
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import os
import shlex
import subprocess
import psutil
import signal

class CmdServer(object):
    def __init__(self, config, safe=False):
        self.config = config
        self.safe = safe
        self.pid_file = os.path.join('ark.pid')
        
        #Rendre multi-instance
        self.folder = '/home/arkserver/ARK-Event2/ShooterGame/Binaries/Linux/ShooterGameServer'

    def start(self):
        result = {}
        if os.path.isfile(self.pid_file):
            with open(self.pid_file, 'r') as pidfile:
                 pid = int(pidfile.read())
            try:
                psutil.Process(pid)
                result['error'] = True
                result['message'] = 'Wooot le serveur est déjà en ligne !'

                return result
            except:
                result['error'] = False
                os.remove(self.pid_file)
                pid = ''
        else:
            result['error'] = False
        
        #Mise en forme du MDP pour launcher
        if self.config['ServerPassword'] is not '':
            server_password = "={}".format(self.config['ServerPassword'])
        else:
            server_password = ''

        #Verification Battleye
        #NOTA : Voir pour l'ajout en fichier de conf
        '''if self.config['BattleEye']:
            battleye_enable = "-UseBattlEye "
        else:
            battleye_enable = ""
        '''
        #Liste des mods à charger
        try:
            if self.config['GameModIds']:
                mods = str(self.config['GameModIds']).replace(" ", "")
        except KeyError:
                mods = ''

        #Chargement Mod Map
        try:
            if self.config['serverMapModId']:
                map_mod_id = '-mapmodid={}'.format(self.config['GameModIds'])
        except KeyError:
            map_mod_id = ''

        #Generation de la commande
        if result['error'] is False:
            start_cmd = "{my_binary} " \
                        "{map}" \
                        "?GameModIds={mods}" \
                        "?MaxPlayers={players}" \
                        "?Port={listen_port}" \
                        "?QueryPort={query_port}" \
                        "?RCONEnabled=True" \
                        "?RCONPort={rcon_port}" \
                        "?ServerAdminPassword={adminpass}" \
                        "?ServerPassword{serverpass}" \
                        "?listen " \
                        "-server " \
                        "-log " \
                        "{mapid}" \
                .format(my_binary=self.folder,
                        map=self.config['serverMap'],
                        mods=mods,
                        players=self.config['MaxPlayers'],
                        listen_port=self.config['Port'],
                        query_port=self.config['QueryPort'],
                        rcon_port=self.config['RCONPort'],
                        adminpass=self.config['ServerAdminPassword'],
                        serverpass=server_password,
                        mapid=map_mod_id,
                        )

            server_process = subprocess.Popen(shlex.split(start_cmd), shell=False)
            pid = server_process.pid
            with open(self.pid_file, 'w') as my_pid_file:
                my_pid_file.write('{}'.format(pid))
            map_temp="event2"
            result['message'] = "L'instance %s est en cours de chargement ... Petit Strip-Poker en attendant ?"%(map_temp)
            return result

        else:
            return result

    def stop(self):
        result = {}
        if not os.path.isfile(self.pid_file):
            result['error'] = True
            result['message'] = 'Impossible de stopper le serveur, serveur déjà hors ligne (PID non existant)'
            return result
        else:
            if self.safe:
                command = ServerRcon('127.0.0.1', int(self.config['RCONPort']), self.config['ServerAdminPassword'], 'saveworld')
                result['save_world'] = commad.run_command()

            with open(self.pid_file, 'r') as pidfile:
                pid = int(pidfile.read())
            p = psutil.Process(pid)
            p.send_signal(signal.SIGTERM)
            os.remove(self.pid_file)
            pid = ''
            result['error'] = False
            result['message'] = "Et voila, Gerbouille a tout pété l'instance !"

            return result

                


