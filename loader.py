import json, sbgarchitecture

all_datatypes = [sbgarchitecture.Entity, sbgarchitecture.Relationship, sbgarchitecture.Trait] #All types of data from sbgarchitecture

def readJSONData(target_datatype): #Registers data from chosen datatype's json file to registries via SubglobalData()'s init
	json_in = json.load(open(f"JSONData/{target_datatype.subglobal_type}.json", "r"))
	for i in json_in:
		target_datatype(json_in[i], False, False, True)
def writeJSONData(target_datatype): #Writes data from registry of target datatype to datatype's json file
	compiled_json_data = dict()
	for i in target_datatype.target_registry:
		compiled_json_data[i] = target_datatype.target_registry[i].aspects
	json.dump(compiled_json_data, open(f"JSONData/{target_datatype.subglobal_type}.json", "w"))

def loadAllJSONData():
	for i in all_datatypes:
		readJSONData(i)
def writeAllJSONData():
	for i in all_datatypes:
		writeJSONData(i)


#TODO get the auditors in after loading