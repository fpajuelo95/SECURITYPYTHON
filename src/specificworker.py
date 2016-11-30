#
# Copyright (C) 2016 by YOUR NAME HERE
#
#    This file is part of RoboComp
#
#    RoboComp is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    RoboComp is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with RoboComp.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, Ice, traceback, time
import networkx as nx
import matplotlib.pyplot as plt

from PySide import *
from genericworker import *

ROBOCOMP = ''
try:
	ROBOCOMP = os.environ['ROBOCOMP']
except:
	print '$ROBOCOMP environment variable not set, using the default value /opt/robocomp'
	ROBOCOMP = '/opt/robocomp'
if len(ROBOCOMP)<1:
	print 'genericworker.py: ROBOCOMP environment variable not set! Exiting.'
	sys.exit()


preStr = "-I"+ROBOCOMP+"/interfaces/ --all "+ROBOCOMP+"/interfaces/"
Ice.loadSlice(preStr+"GotoPoint.ice")
from RoboCompGotoPoint import *
Ice.loadSlice(preStr+"AprilTags.ice")
from RoboCompAprilTags import *
Ice.loadSlice(preStr+"DifferentialRobot.ice")
from RoboCompDifferentialRobot import *



class SpecificWorker(GenericWorker):
	def __init__(self, proxy_map):
		super(SpecificWorker, self).__init__(proxy_map)
		self.timer.timeout.connect(self.compute)
		self.Period = 2000
		self.timer.start(self.Period)
		self.fichero()

	def setParams(self, params):
		#try:
		#	par = params["InnerModelPath"]
		#	innermodel_path=par.value
		#	innermodel = InnerModel(innermodel_path)
		#except:
		#	traceback.print_exc()
		#	print "Error reading config params"
		return True
	
	def fichero(self):
		posiciones = {}
		fich = open('puntos.txt', 'r')
		with fich as f:
		  g=nx.Graph()
		  for line in f:
		    l=line.split()
		    if l[0] == "N":
		      g.add_node(l[1], x=l[2], z=l[3], tipo=l[4])
		      posiciones[l[1]] = (float(l[2]), float (l[3]))
		    elif line[0] == "E":  
		      g.add_edge(l[1], l[2])
		fich.close()
		print posiciones
		img  = plt.imread("plano.png")
		plt.imshow(img, extent = ([-12284, 25600, -3840, 9023]))
		#nx.draw_networkx_nodes(g, posiciones)
		#nx.draw_networkx_edges(g, posiciones)
		#nx.draw_networkx_labels(g, posiciones)

		#print g.nodes()
		#print g.number_of_nodes()
		#print nx.shortest_path(g, source="3", target="12")
		nx.draw_networkx(g, posiciones)
		plt.show()
		
		    
		      
		    

	@QtCore.Slot()
	def compute(self):
		print 'SpecificWorker.compute...'
		
		switch = { 
		  'i':EDOi, 
		   0 :EDO0, 
		   1 :EDO1, 
		   2 :EDO2, 
		} 
		#try:
		#	self.differentialrobot_proxy.setSpeedBase(100, 0)
		#except Ice.Exception, e:
		#	traceback.print_exc()
		#	print e
		return True





