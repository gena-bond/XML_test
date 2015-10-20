# coding: utf8

import shapefile 
import xml.etree.ElementTree as ET
from sys import argv
from os.path import exists
#import unicodedata
script, first = argv
###########################
## Сравнивает два массива - массив Полилинии+Номера точек и массив номеров полилиний полигона
## На выходе - Номера точек (UIDP)каждого из полигонов 
###########################	
def massPoints (ternals,flag):
	if type(ternals[0])==int:
		mass=[]	
		for point in ternals:
			for i in polylines: #Береться с переменной polilynes XPath
				if i[0]==point:
					mass.append(i[1:len(i)])
					break
		if flag==True:
			mass=[y for i in mass for y in i] # вытаскиваем все номера точек с двухмерного массива в одномерный
		else:
			pass
		return mass
	else:
		mass=[]
		for num_point in ternals:
			mass1=[]
			for y in range(len(num_point)):
				for z in polylines:
					if z[0]==num_point[y]:
						mass1.append(z[1:len(z)])
						break
			mass2=[y for i in mass1 for y in i] # вытаскиваем все номера точек с двухмерного массива в одномерный
			mass.append(mass2)
		return mass
	
def PolygonFun (ternal_mass): ##Создает массив точек координат вида [[X1,Y1],[X2,Y2],...] по номерам точек из массива External_mass
	if type(ternal_mass[0])==int:
		k=[]
		External_polygon=[]		
		for point in ternal_mass:
			if point not in k:
				k.append(point)
				for i in coordinates:
					array=[]
					if i[0]==point:
						array.append(i[1])
						array.append(i[2])
						External_polygon.append(array)
						break
		return External_polygon
	else:
		k=[]
		Internal_polygon=[]		
		for z in range(len(ternal_mass)):
			inner_polygon=[]
			for point in ternal_mass[z]:
				if point not in k:
					k.append(point)
					for i in coordinates:
						array=[]
						if i[0]==point:
							array.append(i[1])
							array.append(i[2])
							inner_polygon.append(array)
							break
					
			Internal_polygon.append(inner_polygon)
		return Internal_polygon


w = shapefile.Writer(shapefile.POLYGON)
zone=shapefile.Writer(shapefile.POLYGON)

tree = ET.parse(first)
root = tree.getroot()
point = root.findall(".//Point") #Координаты точек
polyline=root.findall(".//Polyline") #Полилинии для определения внутренних и внешних полигонов
external=root.findall(".//ParcelInfo//ParcelMetricInfo//Externals") #Внешний полигон
internal=root.findall(".//ParcelInfo//ParcelMetricInfo//Internals") #Внутренний полигон
restrictions=root.findall('.//RestrictionInfo')

#target = open(r"d:/xml_/coor.in4", 'w')
#print "Opening the file..."
#target.truncate()
#print "Truncating the file.  Goodbye!"


###Земельный участок

##Адрес

#Parsel_region = root.findall('.//ParcelLocationInfo/Region')[0].text #Область
#print "Rarsel"+Parsel_region
#Parsel_Setlement = root.findall('.//ParcelLocationInfo/Settlement') #город
#Parsel_StreetType = root.findall('.//ParcelAddress/StreetType')[0].text #Тип удицы
#Parsel_StreetName = root.findall('.//ParcelAddress/StreetName')[0].text #Название проезда
#Partsel_Buildings = root.findall('.//ParcelAddress/Building')[0].text #Строение

#####Категория/цель предоставления
Category = root.findall('.//CategoryPurposeInfo/Category') #Категория (код)
#Purpose = root.findall('.//CategoryPurposeInfo/Purpose') # Цель предоставления
#print Purpose[0].text
Use = root.findall('.//CategoryPurposeInfo/Use') # 
#str="Проезд - %s" % (StreetName)
#print str

if len(root.findall('.//Authentication/NaturalPerson/FullName'))<>0:
	###Собственник
	LastName = root.findall('.//Authentication/NaturalPerson/FullName/LastName') #фамилия
	FirstName = root.findall('.//Authentication/NaturalPerson/FullName/FirstName') #имя
	MiddleName = root.findall('.//Authentication/NaturalPerson/FullName/MiddleName') #отчество
	TaxNumber = root.findall('.//Authentication/NaturalPerson/TaxNumber') #ИНН
	##Данные паспорта
	DocumentType = root.findall('.//Authentication/NaturalPerson/Passport/DocumentType') #Тип
	PassportNumber = root.findall('.//Authentication/NaturalPerson/Passport/PassportNumber') #номер
	PassportIssuedDate = root.findall('.//Authentication/NaturalPerson/Passport/PassportIssuedDate') #когда выдан
	IssuanceAuthority = root.findall('.//Authentication/NaturalPerson/Passport/IssuanceAuthority') #кем выдан
	PassportSeries = root.findall('.//Authentication/NaturalPerson/Passport/PassportSeries') #серия
	##Прописка
	Citizenship = root.findall('.//Authentication/NaturalPerson/Citizenship') #Гражданство (код)
	Country = root.findall('.//Authentication/NaturalPerson/Address/Country') #Прописка(страна)(код)
	ZIP = root.findall('.//Authentication/NaturalPerson/Address/ZIP') #Прописка(почтовый индекс)
	Region = root.findall('.//Authentication/NaturalPerson/Address/Region') ##Прописка(область)
	#District = root.findall('.//Authentication/NaturalPerson/Address/District') ##Прописка()
	Settlement = root.findall('.//Authentication/NaturalPerson/Address/Settlement') ##Прописка(город)
	Street = root.findall('.//Authentication/NaturalPerson/Address/Street') ##Прописка(улица)
	Building = root.findall('.//Authentication/NaturalPerson/Address/Building') ##Прописка(дом)
	BuildingUnit = root.findall('.//Authentication/NaturalPerson/Address/BuildingUnit') ##Прописка(квартира)

S = root.findall('.//ParcelMetricInfo/Area/Size') #Площа

##1Создание массива точек вида [[UIDP1,X1,Y1],[...]]
coordinates = []
for points in point:
	array = []
	pn = int(points[0].text) #Из XML - номер точки
	array.append(pn)
	array.append(float(points[4].text)) #в массив добавляем координату Х
	array.append(float(points[3].text)) #в массив добавляем координату Y
	coordinates.append(array)
	
##2Создание массива полилиний вида [[ULID1,Poinst1,Poinst2,..],[...]]
polylines=[]
for poly in polyline[0]:
	array = []
	ULID = int(poly[0].text) #Из XML - уникальній номер полилинии
	array.append(ULID)
	for i in poly[1]:
		array.append(int(i.text)) 
	polylines.append(array)	
	

Externals=[] ##3Определение номеров полилиний внешнего полигона
for ex in external[0][0][0]: 
	array = []
	ULID = int(ex[0].text) #Номера линий внешнего полигона
	Externals.append(ULID)

##Обработка номеров полилиний полигона
if len(internal)==0:
	External_polygon=PolygonFun(massPoints(Externals,True))
	PointsPolygon=[External_polygon]
else:
	
	Internals=[]
	for ex in internal[0]: 
		array = []
		for i in range(len(ex[0])):
			#print ex[0][i][0].text
			ULID = int(ex[0][i][0].text) #Номера линий внутреннего полигона
			array.append(ULID)
		#print array
		Internals.append(array)
	
	Internal_mass=massPoints(Internals,True) ##Вызов функции
	#print len(Internal_mass)
	
	k=[]
	Internal_polygon=[]		
	for z in range(len(Internal_mass)):
		inner_polygon=[]
		for point in Internal_mass[z]:
			if point not in k:
				k.append(point)
				for i in coordinates:
					array=[]
					if i[0]==point:
						array.append(i[1])
						array.append(i[2])
						inner_polygon.append(array)
						break
				#print inner_polygon
		Internal_polygon.append(inner_polygon)
	External_polygon=PolygonFun(massPoints(Externals,True))
	
	##Проверка внутреннего полигона - порядок обхода точек по часовой / против
	#print "Start-",Internal_polygon[0]
	#print "internal",len(Internal_polygon)
	for i in Internal_polygon:
		print len(i)
		#print "Index",i.index(i)
		if shapefile.signed_area(i)>=0:
			print 111
			i.reverse()
		else:
			i.reverse()
			
	PointsPolygon=[External_polygon]
	for i in Internal_polygon:
		PointsPolygon.append(i)



##Охранные зоны Restrictions_code [код зоны], Restrictions_name название охранной зоны
if len(restrictions)<>0:
	##Create polygon&records
	#Restrictions_code=[]
	#Restrictions_name=[]
	Restrictions_poly=[]
	Records=[]
	for i in restrictions:
		Record=[]
		Record.append(i[0].text)
		Record.append(i[1].text)
		s=i[1].text.encode('utf-8')
		#print s.decode('cp1251')
		Restrictions_poly.append(int(i[2][0][0][0][0].text))
		Records.append(Record)
	#print "re",Records[0][0]
	#print Restrictions_poly
	Restrictions_polygon=PolygonFun(massPoints(Restrictions_poly,False))
	#print Restrictions_polygon
else:
	pass
	
#for i in range(len(PointsPolygon)): 
#	print PointsPolygon[i]
#	print

int_poly=[[5238760.3196,5364138.3808],[5238759.2538,5364133.3751],[5238725.3569,5364149.6068],[5238718.1628,5364151.1455],[5238718.5318,5364152.8816],[5238711.6371,5364156.1872],[5238715.9995,5364176.532],[5238758.4857,5364169.3077],[5238766.4535,5364167.1906],[5238760.3196,5364138.3808]]
ex_poly=[[5238697.9,5364184.6],[5238777.6,5364184.2],[5238781.6,5364120.7],[5238702.3,5364122.7],[5238697.9,5364184.6]]
points=[[[5238697.9,5364184.6],[5238777.6,5364184.2],[5238781.6,5364120.7],[5238702.3,5364122.7],[5238697.9,5364184.6]],[[5238760.3196,5364138.3808],[5238759.2538,5364133.3751],[5238725.3569,5364149.6068],[5238718.1628,5364151.1455],[5238718.5318,5364152.8816],[5238711.6371,5364156.1872],[5238715.9995,5364176.532],[5238758.4857,5364169.3077],[5238766.4535,5364167.1906],[5238760.3196,5364138.3808]]]
text1=[[[0,50],[50,50],[50,0],[0,0],[0,50]],[[10,40],[10,10],[30,10],[30,40],[10,40]],[[70,20],[100,20],[100,0],[70,0],[70,20]]]
#points=test2.append(test[0])

#print "points"
#print[coordinates]
#print "polylines"
#print polylines
#print "Externals polilynes"
#print Externals
#print "External"
#print [External_polygon]
#print "Internal"
#print Internal_polygon

##Запись
zone.poly(parts=Restrictions_polygon)
w.poly(parts =PointsPolygon) 
#w.poly(parts =points) 
#w.poly(parts=text1)
#Объявление структуры полей dbf	
w.field('NAME')
w.record('1')
w.record('2')
zone.field('code','c',40)
zone.field('name','c',100)
for z in range(len(Records)):
	print Records[z][0]
	print Records[z][1].encode("cp1251")
	zone.record(code=Records[z][0],name=Records[z][1].encode("cp1251"))

	
w.save('shapefiles/test/'+first[first.rfind("\\")+1:-4]) 
zone.save('shapefiles/test/'+first[first.rfind("\\")+1:-4]+'zone') 



