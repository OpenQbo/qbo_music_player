#!/usr/bin/env python
#
# Software License Agreement (GPLv2 License)
#
# Copyright (c) 2011 OpenQbo, Inc.
#
# This program is free software; you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as 
# published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA 02110-1301, USA.
#
# Authors: Arturo Bajuelos <arturo@openqbo.com>

import roslib; roslib.load_manifest("qbo_music_player")
import rospy 
from syscall import runCmd
from std_msgs.msg import String
from qbo_talk.srv import Text2Speach
import time
import re

client_speak = None

playing_music = False

music_volume = 80

def main():
    
    global client_speak
    
    rospy.init_node("music_master")
    print "Starting Master Listener Node"
    
    rospy.Subscriber("/hand_gesture_node/hand_gesture", String, hand_gesture_callback)  
    client_speak = rospy.ServiceProxy("/qbo_talk/festival_say_no_wait", Text2Speach)
    
    runCmd("xmms2-launcher")

    speak_this("I am ready to play music")
    
    rospy.spin()
    runCmd("nyxmms2 stop")


def hand_gesture_callback(data):
    
    command = str(data.data)
    
    rospy.loginfo(rospy.get_name()+": I heard %s",command)
    
    global playing_music
    global music_volume
    
     
    if command == "play":
        
        runCmd("nyxmms2 toggle")
        
        if playing_music :
            speak_this("Music pause")
            playing_music = False
        else:
            runCmd("nyxmms2 play")
            song_info = get_song_info_2()
            if song_info[1].strip()=="Come What May":
		speak_this("Playing "+song_info[1])
		speak_this("by "+song_info[0])
	    else:
            	speak_this("Playing "+song_info[1]+" by "+song_info[0])
            playing_music = True
        
    
    elif command == "stop":
        runCmd("nyxmms2 "+command)  
        speak_this("Music stopped")
        playing_music = False
    
    elif command == "next" or command == "prev":
        runCmd("nyxmms2 "+command)        
        if playing_music:
            time.sleep(1)
            song_info = get_song_info_2()
	    if song_info[1].strip()=="Spring":
		speak_this("Playing " + song_info[1])
		speak_this("by "+song_info[0])
	    else:
            	speak_this("Playing "+song_info[1]+" by "+song_info[0])
        else:
            time.sleep(1)
            song_info = get_song_info_2()
            
            speak_this("Song selected ")
	    if song_info[1].strip()=="Come What May":
	        speak_this(song_info[1])
		speak_this("by "+song_info[0])	
            else:
		speak_this(song_info[1]+" by "+song_info[0])
         
    elif command=="volume_up":
        if music_volume<=80:
            music_volume+=20
        runCmd("nyxmms2 server volume "+str(music_volume))
        speak_this("Volume up")
    
    elif command=="volume_down":
        if music_volume>20:
            music_volume-=20
        runCmd("nyxmms2 server volume "+str(music_volume)) 
        speak_this("Volume down")

def get_song_info():
    (ph_out, ph_err, ph_ret) = runCmd("nyxmms2 status")
    out_str = str(ph_out)
    splitted = out_str.split(":")
    song_info = splitted[1].strip()
    
    song_info = song_info.split(" - ")
    
    return song_info
    
#    speak_this("Playing "+song_info[0])
#    speak_this(song_info[1])

def get_song_info_2():
    (ph_out, ph_err, ph_ret) = runCmd("nyxmms2 list")
    out_str = str(ph_out)
    
    song_info = out_str.split("->")
    song_info = song_info[1]
    song_info = song_info.split("]")
    song_info = song_info[1]
    song_info = song_info.split("(")
    song_info = song_info[0]
    
    song_info = song_info.strip()
    
    song_info = song_info.split(" - ")
    
    print "Artist: "+song_info[0]+ ", Song: "+song_info[1]
    
    return song_info

def speak_this(text):
    global client_speak
    client_speak(text)
    

if __name__ == '__main__':

    try:
        main()
    except rospy.ROSInterruptException: pass

