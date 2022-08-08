# -*- coding: mbcs -*-
# Created by makepy.py version 0.5.01
# By python version 3.9.13 (tags/v3.9.13:6de2ca5, May 17 2022, 16:36:42) [MSC v.1929 64 bit (AMD64)]
# From type library 'NFActiveX.ocx'
# On Thu Jul 21 16:00:55 2022
'NFActiveX ActiveX Control module'
makepy_version = '0.5.01'
python_version = 0x3090df0
'original file name: 8E2C42D5-A3C9-4D8D-996C-DD2D669F59DAx0x1x0.py'

import win32com.client.CLSIDToClass, pythoncom, pywintypes
import win32com.client.util
from pywintypes import IID
from win32com.client import Dispatch
import numpy as np

# The following 3 lines may need tweaking for the particular server
# Candidates are pythoncom.Missing, .Empty and .ArgNotFound
defaultNamedOptArg=pythoncom.Empty
defaultNamedNotOptArg=pythoncom.Empty
defaultUnnamedArg=pythoncom.Empty

CLSID = IID('{8E2C42D5-A3C9-4D8D-996C-DD2D669F59DA}')
MajorVersion = 1
MinorVersion = 0
LibraryFlags = 10
LCID = 0x0

from win32com.client import DispatchBaseClass
class _DNFActiveX(DispatchBaseClass):
	'Dispatch interface for NFActiveX Control'
	CLSID = IID('{54E2FADC-4D63-4883-88F8-2A3D9DC5B7F2}')
	coclass_clsid = IID('{084B94EF-4DA1-4964-A142-6AD6C4B3E1C9}')

	def AboutBox(self):
		return self._oleobj_.InvokeTypes(-552, LCID, 1, (24, 0), (),)

	def Acq(self, Mode=defaultNamedNotOptArg, IntegrationTime=defaultNamedNotOptArg, AccumulationNum=defaultNamedNotOptArg, From=defaultNamedNotOptArg
			, To=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(5, LCID, 1, (3, 0), ((3, 0), (5, 0), (3, 0), (5, 0), (5, 0)),Mode
			, IntegrationTime, AccumulationNum, From, To)

	def AddID(self, ID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(49, LCID, 1, (3, 0), ((3, 0),),ID
			)

	def AutoFocus(self, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(38, LCID, 1, (3, 0), ((3, 0),),Mode
			)

	def ConvertUnit(self, Value=defaultNamedNotOptArg, Direction=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(25, LCID, 1, (5, 0), ((5, 0), (3, 0)),Value
			, Direction)

	def CreateDataObject(self, Type=defaultNamedNotOptArg, Size=defaultNamedNotOptArg, Size2=defaultNamedNotOptArg, Color=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(22, LCID, 1, (3, 0), ((8, 0), (3, 0), (3, 0), (3, 0)),Type
			, Size, Size2, Color)

	def Dialog(self, Mode=defaultNamedNotOptArg, ItemType=defaultNamedNotOptArg, ItemName=defaultNamedNotOptArg, ItemValue=defaultNamedNotOptArg
			, Options=defaultNamedNotOptArg):
		return self._ApplyTypes_(54, 1, (12, 0), ((3, 0), (30, 0), (30, 0), (30, 0), (30, 0)), 'Dialog', None,Mode
			, ItemType, ItemName, ItemValue, Options)

	def Exec(self, ID=defaultNamedNotOptArg, Command=defaultNamedNotOptArg, pParam=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(3, LCID, 1, (3, 0), ((3, 0), (3, 0), (16396, 0)),ID
			, Command, pParam)

	def GUI(self, Mode=defaultNamedNotOptArg, Name=defaultNamedNotOptArg, Param=defaultNamedNotOptArg, ID=defaultNamedNotOptArg
			, Value=defaultNamedNotOptArg, State=defaultNamedNotOptArg, Format=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(45, LCID, 1, (3, 0), ((3, 0), (8, 0), (8, 0), (3, 0), (16396, 0), (3, 0), (3, 0)),Mode
			, Name, Param, ID, Value, State
			, Format)

	def GetAcqID(self):
		return self._oleobj_.InvokeTypes(6, LCID, 1, (3, 0), (),)

	def GetActiveData(self, DataType=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(23, LCID, 1, (3, 0), ((8, 0),),DataType
			)

	def GetConfigParam(self, pNames=defaultNamedNotOptArg, pUnits=defaultNamedNotOptArg, pTypes=defaultNamedNotOptArg, pValues=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(14, LCID, 1, (3, 0), ((16396, 0), (16396, 0), (16396, 0), (16396, 0)),pNames
			, pUnits, pTypes, pValues)

	def GetDetectorZone(self, FromX=defaultNamedNotOptArg, ToX=defaultNamedNotOptArg, BinningX=defaultNamedNotOptArg, FromY=defaultNamedNotOptArg
			, ToY=defaultNamedNotOptArg, BinningY=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(28, LCID, 1, (3, 0), ((16396, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0)),FromX
			, ToX, BinningX, FromY, ToY, BinningY
			)

	def GetLastErrorInfo(self):
		return self._ApplyTypes_(9, 1, (12, 0), (), 'GetLastErrorInfo', None,)

	def GetMappingParams(self, Axis=defaultNamedNotOptArg, From=defaultNamedNotOptArg, To=defaultNamedNotOptArg, Step=defaultNamedNotOptArg
			, Mode=defaultNamedNotOptArg, Use=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(56, LCID, 1, (3, 0), ((8, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0)),Axis
			, From, To, Step, Mode, Use
			)

	def GetMotorAction(self, Action=defaultNamedNotOptArg, Position=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(16, LCID, 1, (3, 0), ((16396, 0), (16396, 0)),Action
			, Position)

	def GetMotorPosition(self, MotorName=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._ApplyTypes_(8, 1, (12, 0), ((8, 0), (3, 0)), 'GetMotorPosition', None,MotorName
			, Mode)

	def GetMotorStatus(self, MotorName=defaultNamedNotOptArg, MotorID=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(27, LCID, 1, (3, 0), ((8, 0), (3, 0)),MotorName
			, MotorID)

	def GetTriggerMode(self, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(41, LCID, 1, (3, 0), ((8, 0),),Mode
			)

	def GetValue(self, ID=defaultNamedNotOptArg, pName=defaultNamedNotOptArg, pValue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(1, LCID, 1, (3, 0), ((3, 0), (8, 0), (16396, 0)),ID
			, pName, pValue)

	def GetValueSimple(self, ID=defaultNamedNotOptArg, pName=defaultNamedNotOptArg, Value=defaultNamedNotOptArg, VarType=defaultNamedNotOptArg):
		return self._ApplyTypes_(24, 1, (12, 0), ((3, 0), (8, 0), (5, 0), (3, 0)), 'GetValueSimple', None,ID
			, pName, Value, VarType)

	def InitNA(self, pNARoot=defaultNamedNotOptArg, pStatus=defaultNamedNotOptArg):
		'method InitNA'
		return self._oleobj_.InvokeTypes(100, LCID, 1, (3, 0), ((3, 0), (3, 0)),pNARoot
			, pStatus)

	def Load(self, pFileName=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(4, LCID, 1, (3, 0), ((8, 0),),pFileName
			)

	def LoadAll(self, pFileName=defaultNamedNotOptArg):
		return self._ApplyTypes_(50, 1, (12, 0), ((8, 0),), 'LoadAll', None,pFileName
			)

	def LoadConfig(self, IniName=defaultNamedNotOptArg, ShowDialog=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(19, LCID, 1, (3, 0), ((8, 0), (3, 0)),IniName
			, ShowDialog)

	def ManageTemperature(self, Mode=defaultNamedNotOptArg, HeatingSpeed=defaultNamedNotOptArg, HeatingTime=defaultNamedNotOptArg, CoolingSpeed=defaultNamedNotOptArg
			, CoolingTime=defaultNamedNotOptArg, HoldingTime=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(53, LCID, 1, (3, 0), ((3, 0), (5, 0), (5, 0), (5, 0), (5, 0), (5, 0)),Mode
			, HeatingSpeed, HeatingTime, CoolingSpeed, CoolingTime, HoldingTime
			)

	def Map(self, Mode=defaultNamedNotOptArg, DataID=defaultNamedNotOptArg, MapID=defaultNamedNotOptArg, SpectrumID=defaultNamedNotOptArg
			, Values=defaultNamedNotOptArg, Labels=defaultNamedNotOptArg, Units=defaultNamedNotOptArg, Display=defaultNamedNotOptArg, From=defaultNamedNotOptArg
			, To=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(31, LCID, 1, (3, 0), ((3, 0), (16396, 0), (16396, 0), (3, 0), (12, 0), (12, 0), (12, 0), (12, 0), (4, 0), (4, 0)),Mode
			, DataID, MapID, SpectrumID, Values, Labels
			, Units, Display, From, To)

	def MapEx(self, Mode=defaultNamedNotOptArg, MapID=defaultNamedNotOptArg, SpectrumID=defaultNamedNotOptArg, SpectrumIndex=defaultNamedNotOptArg
			, AxisX=defaultNamedNotOptArg, AxisY=defaultNamedNotOptArg, Labels=defaultNamedNotOptArg, Units=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(52, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0), (3, 0), (12, 0), (12, 0), (12, 0), (12, 0)),Mode
			, MapID, SpectrumID, SpectrumIndex, AxisX, AxisY
			, Labels, Units)

	def Message(self, Message=defaultNamedNotOptArg, Type=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(12, LCID, 1, (3, 0), ((8, 0), (3, 0)),Message
			, Type)

	def MessageEx(self, Message=defaultNamedNotOptArg, Type=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(11, LCID, 1, (8, 0), ((8, 0), (3, 0)),Message
			, Type)

	def MoveMotor(self, MotorName=defaultNamedNotOptArg, PositionValue=defaultNamedNotOptArg, PositionName=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(7, LCID, 1, (3, 0), ((8, 0), (5, 0), (8, 0), (3, 0)),MotorName
			, PositionValue, PositionName, Mode)

	def OpenCL(self, Mode=defaultNamedNotOptArg, DataID=defaultNamedNotOptArg, PlatformNum=defaultNamedNotOptArg, DeviceNum=defaultNamedNotOptArg
			, KernelSource=defaultNamedNotOptArg, GlobalWorkSize=defaultNamedNotOptArg, LocalWorkSize=defaultNamedNotOptArg, ResultSize=defaultNamedNotOptArg):
		return self._ApplyTypes_(55, 1, (12, 0), ((3, 0), (3, 0), (3, 0), (3, 0), (31, 0), (3, 0), (3, 0), (3, 0)), 'OpenCL', None,Mode
			, DataID, PlatformNum, DeviceNum, KernelSource, GlobalWorkSize
			, LocalWorkSize, ResultSize)

	def OperVar(self, Mode=defaultNamedNotOptArg, Index=defaultNamedNotOptArg, Value=defaultNamedNotOptArg, Param=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(46, LCID, 1, (3, 0), ((3, 0), (8, 0), (16396, 0), (3, 0)),Mode
			, Index, Value, Param)

	def Paint(self, Mode=defaultNamedNotOptArg, SpectrumID=defaultNamedNotOptArg, Value=defaultNamedNotOptArg, PosX=defaultNamedNotOptArg
			, PosY=defaultNamedNotOptArg, SizeX=defaultNamedNotOptArg, SizeY=defaultNamedNotOptArg, Text=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(42, LCID, 1, (3, 0), ((3, 0), (3, 0), (4, 0), (5, 0), (5, 0), (5, 0), (5, 0), (8, 0)),Mode
			, SpectrumID, Value, PosX, PosY, SizeX
			, SizeY, Text)

	def Pause(self, Time=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(10, LCID, 1, (3, 0), ((5, 0),),Time
			)

	def Print(self, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(44, LCID, 1, (3, 0), ((3, 0),),Mode
			)

	def Profile(self, Mode=defaultNamedNotOptArg, ProfileID=defaultNamedNotOptArg, SpectrumID=defaultNamedNotOptArg, Value=defaultNamedNotOptArg
			, Unit=defaultNamedNotOptArg, Label=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(37, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0), (5, 0), (8, 0), (8, 0)),Mode
			, ProfileID, SpectrumID, Value, Unit, Label
			)

	def PutArrGUI(self, Index=defaultNamedNotOptArg, pValue=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(48, LCID, 1, (3, 0), ((12, 0), (16396, 0), (3, 0)),Index
			, pValue, Mode)

	def PutDataInfo(self, ID=defaultNamedNotOptArg, TableName=defaultNamedNotOptArg, TableEntry=defaultNamedNotOptArg, TableValue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(32, LCID, 1, (3, 0), ((3, 0), (8, 0), (8, 0), (8, 0)),ID
			, TableName, TableEntry, TableValue)

	def PutGUI(self, Index=defaultNamedNotOptArg, Value=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(47, LCID, 1, (3, 0), ((12, 0), (12, 0), (3, 0)),Index
			, Value, Mode)

	def PutValue(self, ID=defaultNamedNotOptArg, pName=defaultNamedNotOptArg, pValue=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(2, LCID, 1, (3, 0), ((3, 0), (8, 0), (16396, 0)),ID
			, pName, pValue)

	def Save(self, ID=defaultNamedNotOptArg, pFileName=defaultNamedNotOptArg, pFormat=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(26, LCID, 1, (3, 0), ((3, 0), (8, 0), (8, 0)),ID
			, pFileName, pFormat)

	def SaveConfig(self, IniName=defaultNamedNotOptArg, ShowDialog=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(18, LCID, 1, (3, 0), ((8, 0), (3, 0)),IniName
			, ShowDialog)

	def Send(self, To=defaultNamedNotOptArg, Command=defaultNamedNotOptArg, Param=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg
			, Status=defaultNamedNotOptArg):
		return self._ApplyTypes_(33, 1, (12, 0), ((8, 0), (8, 0), (12, 0), (3, 0), (16396, 0)), 'Send', None,To
			, Command, Param, Mode, Status)

	def SetAutoExposure(self, TestTime=defaultNamedNotOptArg, MinTime=defaultNamedNotOptArg, MaxTime=defaultNamedNotOptArg, DesiredIntensity=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(39, LCID, 1, (3, 0), ((5, 0), (5, 0), (5, 0), (5, 0)),TestTime
			, MinTime, MaxTime, DesiredIntensity)

	def SetConfigParam(self, Description=defaultNamedNotOptArg, pNames=defaultNamedNotOptArg, pUnits=defaultNamedNotOptArg, pTypes=defaultNamedNotOptArg
			, pValues=defaultNamedNotOptArg, ShowMode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(15, LCID, 1, (3, 0), ((8, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0), (3, 0)),Description
			, pNames, pUnits, pTypes, pValues, ShowMode
			)

	def SetDetectorZone(self, FromX=defaultNamedNotOptArg, ToX=defaultNamedNotOptArg, BinningX=defaultNamedNotOptArg, FromY=defaultNamedNotOptArg
			, ToY=defaultNamedNotOptArg, BinningY=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(29, LCID, 1, (3, 0), ((3, 0), (3, 0), (3, 0), (3, 0), (3, 0), (3, 0)),FromX
			, ToX, BinningX, FromY, ToY, BinningY
			)

	def SetMappingParams(self, Axis=defaultNamedNotOptArg, From=defaultNamedNotOptArg, To=defaultNamedNotOptArg, Step=defaultNamedNotOptArg
			, Mode=defaultNamedNotOptArg, Use=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(36, LCID, 1, (3, 0), ((31, 0), (5, 0), (5, 0), (5, 0), (3, 0), (3, 0)),Axis
			, From, To, Step, Mode, Use
			)

	def SetMotorInfo(self, Position=defaultNamedNotOptArg, State=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(17, LCID, 1, (3, 0), ((5, 0), (3, 0)),Position
			, State)

	def SetScale(self, FromX=defaultNamedNotOptArg, ToX=defaultNamedNotOptArg, FromY=defaultNamedNotOptArg, ToY=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(30, LCID, 1, (3, 0), ((5, 0), (5, 0), (5, 0), (5, 0)),FromX
			, ToX, FromY, ToY)

	def SetScaleEx(self, ID=defaultNamedNotOptArg, FromX=defaultNamedNotOptArg, ToX=defaultNamedNotOptArg, FromY=defaultNamedNotOptArg
			, ToY=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(57, LCID, 1, (3, 0), ((3, 0), (5, 0), (5, 0), (5, 0), (5, 0)),ID
			, FromX, ToX, FromY, ToY)

	def SetScriptParamOptions(self, Description=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(35, LCID, 1, (3, 0), ((8, 0), (3, 0)),Description
			, Mode)

	def SetScriptPath(self, pScriptPath=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(13, LCID, 1, (3, 0), ((8, 0),),pScriptPath
			)

	def SetSingleScriptParam(self, Name=defaultNamedNotOptArg, Unit=defaultNamedNotOptArg, Value=defaultNamedNotOptArg, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(34, LCID, 1, (3, 0), ((31, 0), (31, 0), (12, 0), (3, 0)),Name
			, Unit, Value, Mode)

	def Template(self, Mode=defaultNamedNotOptArg, Param=defaultNamedNotOptArg, Value=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(43, LCID, 1, (3, 0), ((3, 0), (8, 0), (16396, 0)),Mode
			, Param, Value)

	def TickCount(self):
		return self._oleobj_.InvokeTypes(51, LCID, 1, (3, 0), (),)

	def Translate(self, Text=defaultNamedNotOptArg):
		# Result is a Unicode object
		return self._oleobj_.InvokeTypes(40, LCID, 1, (8, 0), ((8, 0),),Text
			)

	def Treat(self, ID=defaultNamedNotOptArg, FunctionName=defaultNamedNotOptArg, FunctionMode=defaultNamedNotOptArg, Param1=defaultNamedNotOptArg
			, Param2=defaultNamedNotOptArg, Param3=defaultNamedNotOptArg, Param4=defaultNamedNotOptArg, Param5=defaultNamedNotOptArg, Param6=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(20, LCID, 1, (3, 0), ((3, 0), (8, 0), (3, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0), (16396, 0)),ID
			, FunctionName, FunctionMode, Param1, Param2, Param3
			, Param4, Param5, Param6)

	def Video(self, Mode=defaultNamedNotOptArg):
		return self._oleobj_.InvokeTypes(21, LCID, 1, (3, 0), ((3, 0),),Mode
			)

	_prop_map_get_ = {
	}
	_prop_map_put_ = {
	}
	def __iter__(self):
		"Return a Python iterator for this object"
		try:
			ob = self._oleobj_.InvokeTypes(-4,LCID,3,(13, 10),())
		except pythoncom.error:
			raise TypeError("This object does not support enumeration")
		return win32com.client.util.Iterator(ob, None)

class _DNFActiveXEvents:
	'Event interface for NFActiveX Control'
	CLSID = CLSID_Sink = IID('{AD50553A-2189-4A82-8142-C343C7E0882B}')
	coclass_clsid = IID('{084B94EF-4DA1-4964-A142-6AD6C4B3E1C9}')
	_public_methods_ = [] # For COM Server support
	_dispid_to_func_ = {
		}

	def __init__(self, oobj = None):
		if oobj is None:
			self._olecp = None
		else:
			import win32com.server.util
			from win32com.server.policy import EventHandlerPolicy
			cpc=oobj._oleobj_.QueryInterface(pythoncom.IID_IConnectionPointContainer)
			cp=cpc.FindConnectionPoint(self.CLSID_Sink)
			cookie=cp.Advise(win32com.server.util.wrap(self, usePolicy=EventHandlerPolicy))
			self._olecp,self._olecp_cookie = cp,cookie
	def __del__(self):
		try:
			self.close()
		except pythoncom.com_error:
			pass
	def close(self):
		if self._olecp is not None:
			cp,cookie,self._olecp,self._olecp_cookie = self._olecp,self._olecp_cookie,None,None
			cp.Unadvise(cookie)
	def _query_interface_(self, iid):
		import win32com.server.util
		if iid==self.CLSID_Sink: return win32com.server.util.wrap(self)

	# Event Handlers
	# If you create handlers, they should have the following prototypes:


from win32com.client import CoClassBaseClass
# This CoClass is known by the name 'NFACTIVEX.NFActiveXCtrl.1'
class NFActiveX(CoClassBaseClass): # A CoClass
	# NFActiveX Control
	CLSID = IID('{084B94EF-4DA1-4964-A142-6AD6C4B3E1C9}')
	coclass_sources = [
		_DNFActiveXEvents,
	]
	default_source = _DNFActiveXEvents
	coclass_interfaces = [
		_DNFActiveX,
	]
	default_interface = _DNFActiveX

RecordMap = {
}

CLSIDToClassMap = {
	'{54E2FADC-4D63-4883-88F8-2A3D9DC5B7F2}': _DNFActiveX,
	'{AD50553A-2189-4A82-8142-C343C7E0882B}': _DNFActiveXEvents,
	'{084B94EF-4DA1-4964-A142-6AD6C4B3E1C9}': NFActiveX,
}
CLSIDToPackageMap = {}
win32com.client.CLSIDToClass.RegisterCLSIDsFromDict(CLSIDToClassMap)
VTablesToPackageMap = {}
VTablesToClassMap = {
}


NamesToIIDMap = {
	'_DNFActiveX' : '{54E2FADC-4D63-4883-88F8-2A3D9DC5B7F2}',
	'_DNFActiveXEvents' : '{AD50553A-2189-4A82-8142-C343C7E0882B}',
}

# encapsulate a class delicated for horiba
class Horiba:

	def __init__(self):
		self.horiba = NFActiveX()

	def get_temperature(self):
		temperature = self.horiba.Acq(Mode=4, IntegrationTime=0, AccumulationNum=0, From=0, To=0)
		return float(temperature)

	def get_wl(self):
		wl = self.horiba.GetMotorPosition(MotorName='Spectro', Mode=0)
		return float(wl)

	def get_slit(self):
		slit_pos = self.horiba.GetMotorPosition(MotorName='Slit', Mode=0)
		return float(slit_pos)

	def get_hole(self):
		hole_pos = self.horiba.GetMotorPosition(MotorName='Hole', Mode=0)
		return float(hole_pos)

	def get_rayleigh_line(self):
		ray = self.horiba.GetMotorPosition(MotorName='Laser', Mode=0)
		return float(ray)

	def set_wl(self, wl):
		self.horiba.MoveMotor(MotorName='Spectro', PositionValue=wl, PositionName='', Mode=0)

	def acquire_spectrum(self, exposure_time, exposure_num):
		"""acquire single spectrum, the wavelength range is detector width"""
		self.horiba.Acq(Mode=300, IntegrationTime=exposure_time, AccumulationNum=exposure_num, From=0, To=0)
		acq_flg = True
		while acq_flg:
			acq_ID = self.horiba.GetAcqID()
			if acq_ID > 0:
				acq_flg = False
				print('loop end')
		print('start to get value')
		# data = np.empty(shape=[0, 2])
		data = list()
		spectrum = self.horiba.GetValue(ID=acq_ID, pName='XYData', pValue=data)
		print(spectrum)
		wavenumber = np.array(spectrum[1][0])
		intensity = np.array(spectrum[1][1])
		laser_line = self.get_rayleigh_line()
		wavelength = laser_line/(1 - wavenumber * laser_line * 1e-7)
		return wavelength, intensity

	def acquire_spectrum_stitch(self, start, stop, exposure_time, exposure_num):
		"""acquire single spectrum, the wavelength range is detector width"""
		self.horiba.Acq(Mode=300, IntegrationTime=exposure_time, AccumulationNum=exposure_num, From=start, To=stop)
		acq_flg = True
		while acq_flg:
			acq_ID = self.horiba.GetAcqID()
			if acq_ID > 0:
				acq_flg = False
				print('loop end')
		print('start to get value')
		# data = np.empty(shape=[0, 2])
		data = list()
		spectrum = self.horiba.GetValue(ID=acq_ID, pName='XYData', pValue=data)
		print(spectrum)
		wavenumber = np.array(spectrum[1][0])
		intensity = np.array(spectrum[1][1])
		laser_line = self.get_rayleigh_line()
		wavelength = laser_line/(1 - wavenumber * laser_line * 1e-7)
		return wavelength, intensity

	# not stable, do not use it
	def acquire_RTA(self, exposure_time):
		self.horiba.Acq(Mode=5, IntegrationTime=exposure_time, AccumulationNum=0, From=0, To=0)
		acq_flg = True
		while acq_flg:
			acq_ID = self.horiba.GetAcqID()
			if acq_ID > 0:
				acq_flg = False
				print('loop end')
		print('start to get value')
		# data = np.empty(shape=[0, 2])
		data = list()
		spectrum = self.horiba.GetValue(ID=acq_ID, pName='XYData', pValue=data)
		print(spectrum)
		wavenumber = np.array(spectrum[1][0])
		intensity = np.array(spectrum[1][1])
		laser_line = self.get_rayleigh_line()
		wavelength = laser_line/(1 - wavenumber * laser_line * 1e-7)
		return wavelength, intensity

	def acquire_cancel(self):
		self.horiba.Acq(Mode=8, IntegrationTime=0, AccumulationNum=0, From=0, To=0)