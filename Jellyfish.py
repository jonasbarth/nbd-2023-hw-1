#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 11:20:14 2023

@author: giacomo
"""

""" Module to create the Jellyfish topology"""

""" IMPORTANT: 
    
                - Check if the number of servers is S(n-r) or n^3/4
                - Check if construction procedure part 2 is necessary and if it's correct"""

import random

class Jellyfish:
    
    def __init__(self, n, tau, capacity):
        
        self.n = n       #number of ports of a swith
        self.r = n // 2  #number of neighbor
        self.S = n ** 2  #number of switches
        self.tau = tau   #trip time between two nodes in the server in micro-seconds
        self.capacity = capacity #the capacity of links in the fat-tree in Gbit/s.
        self.switches = {i: [] for i in range(self.S)} #initialize as a dictionary: key is the index, the values are the neighbor
        self.servers = (n ** 3) // 4 #number of servers
        
    def build_structure(self): 
        
        """
        |CONSTRUCTION PROCEDURE PART 1|
        
        1. Create a list of switches with free ports
        
        2. Until there are free ports: 
            
                a. choice 2 random switch from the list; 
                b. if they are not connected and they are not the same switch: 
                    
                        -connect them adding them to the list of neighbor;
                        
                c. if one of them reach the maximum number of neighbor r: 
                    
                        -remove from the list of switches with free ports
        """
        switches_with_free_ports = list(range(self.S)) #indexes of switches with free port
        
        while switches_with_free_ports != []:
            
            switch1 = random.choice(switches_with_free_ports) #random choices
            switch2 = random.choice(switches_with_free_ports)
            
            if switch1 != switch2 and switch1 not in self.switches[switch2]:#check if they are the same or already connected
                
                self.switches[switch1].append(switch2) #connect them
                self.switches[switch2].append(switch1)
                
                if len(self.switches[switch1]) == self.r: #check maximum number of neighbor
                    
                    switches_with_free_ports.remove(switch1) #no more free ports
                    
                if len(self.switches[switch2]) == self.r:
                    
                    switches_with_free_ports.remove(switch2)
                    
        """
        |CONSTRUCTION PROCEDURE PART 2|
        
        1. Check if a switch has >= 2 free ports left, say (p1,p2)
        
        2. Choose a random link (x,y)
        
        3. Remove the link
        
        4. Replace the link with (p1,x) and (p2,x)
        
        """    

        for i in range(self.S): #iterate over the switches
            
            if len(self.switches[i]) <= self.r - 2: #check for >= 2 free ports 
                
                #choose random link
                x = random.choice(list(self.switches.keys()))  #choose one random switch
                y = random.choice(self.switches[x]) #choose one random link
                
                #remove link
                self.switches[x].remove(y) #remove y from the neighbor of x
                self.switches[y].remove(x) #remove x from the neighbor of y
                
                p1,p2 = i #set p1,p2 as two port of the switch
                
                #add the new link
                self.switches[p1].append(x)
                self.switches[x].append(p1)
                self.switches[p2].append(y)
                self.switches[y].append(p2)
                
        