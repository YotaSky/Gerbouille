#!/usr/bin/python
#Bot Gerbouille Discord/ARK
#France-Evolved https://discord.gg/gVsveNY
#2017 By YotaSky https://github.com/YotaSky

import os
import shlex
import subprocess
import psutil
import signal
import binascii

class CmdServer(object):
    def __init__(self, config, safe=False):
        self.config = config
        self.safe = safe
        self.folder = os.path.join(os.path.sep,config['arkserverroot'],'ShooterGame','Binaries','Linux','ShooterGameServer')
        self.pid_file = os.path.join(os.path.sep,'etc','gerbouille','{}.pid'.format(binascii.crc32(bytes(self.folder,encoding="UTF-8"))))

    def start(self):
        result = {}
        if os.path.isfile(self.pid_file):
            with open(self.pid_file, 'r') as pidfile:
                 pid = int(pidfile.read())
            try:
                psutil.Process(pid)
                result['error'] = True
                result['message'] = "D'Oh! Le serveur est déjà en ligne !"

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
                map_mod_id = '?MapModID={}'.format(self.config['serverMapModId'])
        except KeyError:
            map_mod_id = ''

        #Generation de la commande
        if result['error'] is False:
            start_cmd = "{my_binary} " \
                        "{map}" \
                        "{mapid}" \
                        "?RCONEnabled=True" \
                        "?RCONPort={rcon_port}" \
                        "?SessionName={session_name}" \
                        "?Port={listen_port}" \
                        "?QueryPort={query_port}" \
                        "?ServerPassword{serverpass}" \
                        "?ServerAdminPassword={adminpass}" \
                        "?MaxPlayers={players}" \
                        "?GameModIds={mods}" \
                        "?ClusterDirOverride={clustdirover}" \
                        "?clusterid={clusterid}" \
                        "?NoTransferFromFiltering={NoTransferFromFiltering}" \
                        "?PreventDownloadSurvivors={PreventDownloadSurvivors}" \
                        "?PreventDownloadDinos={PreventDownloadDinos}" \
                        "?PreventUploadSurvivors={PreventUploadSurvivors}" \
                        "?PreventUploadDinos={PreventUploadDinos}" \
                        "?RCONServerGameLogBuffer={rconbuffer}" \
                        "?listen " \
                        "-servergamelog " \
                .format(my_binary=self.folder,
                        map=str(self.config['serverMap']),
                        mapid=map_mod_id,
                        rcon_port=self.config['RCONPort'],
                        session_name=str(self.config['SessionName']),
                        listen_port=self.config['Port'],
                        query_port=self.config['QueryPort'],
                        serverpass=server_password,
                        adminpass=self.config['ServerAdminPassword'],
                        players=self.config['MaxPlayers'],
                        mods=mods,
                        clustdirover=self.config['ClusterDirOverride'],
                        clusterid=self.config['clusterid'],
                        NoTransferFromFiltering=self.config['NoTransferFromFiltering'],
                        PreventDownloadSurvivors=self.config['PreventDownloadSurvivors'],
                        PreventDownloadDinos=self.config['PreventDownloadDinos'],
                        PreventUploadSurvivors=self.config['PreventUploadSurvivors'],
                        PreventUploadDinos=self.config['PreventUploadDinos'],
                        rconbuffer='600'
                        )

            print (start_cmd)

            server_process = subprocess.Popen(shlex.split(start_cmd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session = True)
            pid = server_process.pid
            with open(self.pid_file, 'w') as my_pid_file:
                my_pid_file.write('{}'.format(pid))
            result['message'] = "L'instance %s est en cours de chargement ... Petit Strip-Poker en attendant ?"%(self.config['serverMap'])
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
