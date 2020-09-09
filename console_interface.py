import sbgarchitecture, loader
import os, sys

class MoveUp(Exception):
	pass

sbgarchitecture.Entity.initDatatype()
sbgarchitecture.Relationship.initDatatype()
sbgarchitecture.Trait.initDatatype()

editor = str()

exit_words = ["cancel", "exit"]
binary_mapping = {"y":1, "yes":1, "n":0, "no":0}


def checkBinary(response_check, exit_check):#Checks a Y/N prompt
	if response_check.lower() in binary_mapping:
		return binary_mapping[response_check.lower()]
	elif exit_check and response_check.lower() in exit_words:
		print("Prompt exited")
		raise Exception()
	else:
		if exit_check:
			print("Invalid input. Use 'cancel' to exit this prompt.")
		else:
			print("Invalid input.")
		return 2
def checkSure(exit_check):#Checks to make sure the user wants to carry out an action
	print("Are you sure?")
	continue_loop_binary = True
	while continue_loop_binary:
		binary_response = input("(Y/N): ")
		binary_response_result = checkBinary(binary_response, exit_check)
		if binary_response_result == 1:
			return True
		elif binary_response_result == 0:
			return False
def checkGo(response_go):#Checks to keep going in the creation of a plural aspect
	if response_go.lower() in ["stop", "done"]:
		print("This will end the data entry.")
		if checkSure(False):
			return False
	elif response_go.lower() in exit_words:
		print("This will lose all entered data for this plural aspect.")
		checkSure(True)
	else:
		return True

def listTypes():
	print("These are all registered types:")
	for i in loader.all_datatypes:
		print(i.subglobal_type)
def listInstancesByType(target_type):
	print(f"These are all instances of type {target_type.subglobal_type} found:")
	for i in target_type.target_registry:
		print(target_type.target_registry[i].aspects["readable_name"])
def outlineAspects(target_instance):
	print(f"The aspects of {target_instance.aspects['readable_name']} are as follows:")
	for i in target_instance.aspects:
		if target_instance.aspect_blueprint[i][2]:
			if target_instance.aspect_blueprint[i][3] == None:
				to_print = target_instance.aspects[i]
			else:
				to_print = target_instance.aspect_blueprint[i][3][target_instance.aspects[i][0]].aspects["readable_name"]
			print(f"{target_instance.subglobal_type.capitalize()} {target_instance.aspects['readable_name']}'s {target_instance.aspect_blueprint[4]} is {to_print}")
		else:
			print(f"{target_instance.subglobal_type.capitalize()} {target_instance.aspects['readable_name']} has {len(target_instance.aspects[i][0])} {target_instance.aspect_blueprint[i][4]}")
def detailPluralAspect(target_instance):
	print(f"{target_instance.aspects['readable_name'].capitalize()} has these plural aspects:")
	for i in target_instance.aspects:
		if target_instance.aspect_blueprint[i][2] == False:
			print(f"{target_instance.subglobal_type.capitalize()} {target_instance.aspects['readable_name']} has {len(target_instance.aspects[i][0])} {target_instance.aspect_blueprint[i][4]}")
	print("Please enter which one you would like to view.")
	view_entry = input()
	try:
		target_aspect = target_instance.aspects[view_entry]
		print(f"{target_instance.subglobal_type.capitalize()} {target_instance.aspects['readable_name']} has {target_instance.aspect_blueprint[target_aspect][4].lower()} as follows:")
		for i in target_instance.aspects[target_aspect]:
			if target_instance.aspect_blueprint[target_aspect][3] == None:
				to_print = i
			else:
				to_print = target_instance.aspect_blueprint[target_aspect][3][i].aspects["readable_name"]
			if type(target_instance.aspect_blueprint[target_aspect][0]) == type(list()):
				print(to_print)
			elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(dict()): #Looking for dicts. Could have an issue if I ever have dicts with values of hexdigests
				print(f"{to_print}: {target_instance.aspects[target_aspect][i]}")
	except NameError:
		print("Invalid aspect. Cancelling operation.")

def createPluralAspect(target_instance, target_aspect, readable_name, target_trust,):
	if type(target_instance.aspect_blueprint[target_aspect][0]) == type(list()):
		target_aspect_temp = list()
	elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(dict()):
		target_aspect_temp = dict()
	print(f"Input data for {readable_name}'s {target_instance.aspect_blueprint[target_aspect][4]}.")
	print(f"Press enter after each discrete data point to register it.")
	print(f"Type 'stop' to cease data entry, and 'exit' to cancel entry.")
	continue_loop_go = True
	while continue_loop_go:
		new_entry = input()
		if checkGo(new_entry):
			if type(target_instance.aspect_blueprint[target_aspect][0]) == type(list()):
				target_aspect_temp.append(new_entry)
			elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(dict()): #Only accounts for the only current aspects stored as dicts, which involve trust
				target_aspect_temp[new_entry] = target_trust
		else:
			return target_aspect_temp
			print("Changes registered")
			continue_loop_go = False
def createSingularAspect(target_instance, target_aspect, readable_name):
	print(f"Input new entry for {readable_name}'s {target_aspect}")
	continue_loop_sure = True
	while continue_loop_sure:
		new_entry = input(f"{target_instance.aspect_blueprint[target_aspect][4]}: ")
		print(f"You are about to change {readable_name}'s {target_instance.aspect_blueprint[target_aspect][4]} to {new_entry}")
		if checkSure(True):
			continue_loop_sure = False
	if type(target_instance.aspect_blueprint[target_aspect][0]) == type(str()): #TOCHECK implement switch/case system here?
		return new_entry
	elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(int()):
		return int(new_entry)
	elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(float()):
		return float(new_entry)
def createNewInstance(target_type, own_registrar, **kwargs): #All required information that is not handled in normal initialization and can not be manually inputted must be passed as kwargs
	new_instance_loop = True
	while new_instance_loop:
		return_source_dict = dict()
		for i in target_type.required_aspects: #TODO check efficiency
			if target_type.aspect_blueprint[i][6]:
				if target_type.aspect_blueprint[i][2]:
					return_source_dict[i] = createSingularAspect(target_type, i, f"the new {target_type.subglobal_type.lower()}")
				else:
					return_source_dict[i] = createPluralAspect(target_type, i, f"the new {target_type.subglobal_type.lower()}", kwargs['registrar_trust']) #TODO implement actual trust calculation
			else:
				return_source_dict[i] = kwargs[i]
		print(f"You will create a new {target_type.subglobal_type.lower()} with the above aspects.")
		if checkSure(True):
			new_instance_loop = False
	target_type(return_source_dict, True, own_registrar, False)
def destroyInstance(target_instance): #TODO security
	print(f"You will delete {target_instance.aspects['readable_name']}")
	if checkSure(True):
		print("Make sure that you are REALLY sure about this. This is an irreversible action if saved.")
		if checkSure(True):
			target_instance.deleteInstance()
			raise ZeroDivisionError
		else:
			print("Cancelling.")
	else:
		print("Cancelling.")

def addPluralAspectEntry(target_instance, target_aspect, trust):
	plural_entry_loop = True
	while plural_entry_loop:
		print(f"What would you like to add to {target_instance.aspects['readable_name']}'s {target_instance.aspect_blueprint[target_aspect][4]} aspect?")
		print(f"Enter 'stop' to cease further data entry.")
		new_entry = input()
		if checkGo(new_entry):
			print(f"You will add '{new_entry}' to {target_instance.aspects['readable_name']}'s {target_instance.aspect_blueprint[target_aspect][4]} aspect.")
			if checkSure(False):
				try:
					if type(target_instance.aspect_blueprint[target_aspect][0]) == type(list()):
						target_instance.updateAspect(target_aspect, new_entry, editor, False, len(target_instance.aspects[target_aspect]))
					elif type(target_instance.aspect_blueprint[target_aspect][0]) == type(dict()):
						target_instance.updateAspect(target_aspect, trust, editor, False, new_entry)
				except Exception:
					print("Invalid permissions")
				except KeyError:
					print("Invalid key")
				except IndexError:
					print("Invalid reference")
		else:
			plural_entry_loop = False
			print("Entry completed.")
def removePluralAspectEntry(target_instance, target_aspect, target_entry):
	print(f"You will remove entry '{target_entry}' from {target_instance.aspects["readable_name"]}'s {target_instance.aspect_blueprint[target_aspect][4]} aspect.")
	if checkSure(True):
		print("Deleting...")
		try:
			target_instance.removeAspectEntry(target_aspect, editor, False, target_entry, False)
			print("Successfully removed entry.")
		except Exception():
			print("Permissions error.")
	else:
		print("Deletion cancelled.")
def changePluralAspectEntry(target_instance, target_aspect, target_entry): #TODO let Ibrahim make these two functions one
	try:
		if type(target_instance.aspects[target_aspect]) == type(dict()): #TOCHECK see if dicts will ever have a value that is not trust
			target_entry_readable = target_entry
		elif type(target_instance.aspects[target_aspect]) == type(list()):
			target_entry_readable = target_instance.aspects[target_aspect][target_entry]
		print(f"You will change '{target_entry_readable}' from {target_instance.aspects['readable_name']}'s {target_instance.aspect_blueprint[target_aspect][4]} aspect.")
		print("What would you like to change it to?")
		new_entry = input()
		print(f"You will change '{target_entry_readable}' to '{new_entry}'.")
		if checkSure(True):
			print("Changing...")		
			target_instance.updateAspect(target_aspect, new_entry, editor, False, target_entry)
			print("Successfully changed entry.")
		else:
			print("Operation cancelled.")
	except Exception:
		print("Permissions invalid. Operation cancelled.")
	except KeyError:
		print("No such key. Operation cancelled.")
def changeSingularAspect(target_instance, target_aspect):
	try: #TODO don't repeat yourself?
		print(f"You will change '{target_instance.aspects[target_aspect]}' in {target_instance.aspects['readable_name']}'s {target_instance.aspect_blueprint[target_aspect][4]} aspect.")
		print("What would you like to change it to?")
		new_entry = input()
		print(f"You will change '{target_instance.aspects[target_aspect]}' to '{new_entry}'.")
		if checkSure(True):
			print("Changing...")
			target_instance.updateAspect(target_aspect, new_entry, editor, False, None)
			print("Successfully changed entry.")
		else:
			print("Operation cancelled.")
	except Exception:
		print("Permissions invalid. Operation cancelled.")
	except KeyError:
		print("No such key. Operation cancelled.")

workspaces = dict()
def workspaceList():
	print("Listing available workspaces...")
	for i in workspaces:
		print(i)
def workspaceMove():
	print("Which workspace would you like to move to? Use 'up' to return to the previous workspace. Use 'list' to list all available workspaces.")
	to_move = input().lower()
	try:
		if to_move == "up":
			raise MoveUp
		elif to_move == "list":
			workspaceList()
		eval(f"{workspaces[to_move]}({editor})")
	except NameError:
		print("Invalid workspace.")
def workspaceHelp(target_workspace):
	print("Listing available help...")
	for i in target_workspace.commands:
		print(f"{i}: {target_workspace.commands[i][1]}")
def workspaceSelectInstance(target_type):
	print("Please enter the full hexdigest of your selected instance.")
	target_instance = input()
	try:
		InstanceWorkspace(eval(f"{target_type}.target_registry.{target_instance}"))
def workspaceSelectAspect(target_instance):
	print("Please choose which aspect you will edit.")
	to_edit = input()
	try:
		if target_instance.aspect_blueprint[to_edit][2]:
			changeSingularAspect(target_instance, to_edit)
		else:
			AspectWorkspace()
	except NameError:
		print("Invalid aspect. Operation cancelled.")
def workspaceMainLoop(command_registry):
	main_continue = True
		while main_continue:
			print("Input a command: ")
			to_execute = input().lower()
			try:
				if to_execute in self.commands:
					self.commands[to_execute][0]
				else:
					print("Command not recognized.")
			except ZeroDivisionError:
				main_continue = False

class Workspace(): #TOCHECK quirky or no
	def __init__(self):
		self.commands = dict() #<name of command (str)>:(<function to call>, <help description (str)>)
		self.commands["move"] = (workspaceMove(), "Moves you to another workspace.")
		self.commands["exit"] = (lambda: 1/0, "Exits the prompt.")
		self.commands["help"] = (workspaceHelp(eval('self.commands')), "Provides help for all functions in current workspace.")
class GlobalWorkspace(Workspace):
	workspaces["global"] = "GlobalWorkspace"
	def __init__(self):
		super(GlobalWorkspace, self).__init__()
		self.commands["list"] = (listTypes(), "Lists all subglobal types.")
		workspaceMainLoop(self.commands)
class TypeWorkspace(Workspace):
	editor_trust = float() #TOCHECK jankalicious
	def __init__(self, parent_type):
		super(TypeWorkspace, self).__init__()
		self.parent_type = parent_type
		self.commands["create"] = (createNewInstance(self.parent_type, False, editor_trust), f"Enters the prompt to create a new {cls.parent_type.subglobal_type.lower()} instance.")
		self.commands["list"] = (listInstancesByType(self.parent_type), f"Lists all instances of type {cls.parent_type.subglobal_type.lower()}.")
		self.commands["edit"] = (workspaceSelectInstance(self.parent_type), f"Allows you to enter an instance's workspace.")
class TypeEntityWorkspace(TypeWorkspace):
	workspaces["entity"] = "TypeEntityWorkspace"
	def __init__(self):
		super(TypeEntityWorkspace, self).__init__(sbgarchitecture.Entity)
		workspaceMainLoop(self.commands)
class TypeRelationshipWorkspace(TypeWorkspace):
	workspaces["relationship"] = "TypeRelationshipWorkspace"
	def __init__(self):
		super(TypeRelationshipWorkspace, self).__init__(sbgarchitecture.Relationship)
		workspaceMainLoop(self.commands)
class TypeTraitWorkspace(TypeWorkspace):
	workspaces["trait"] = "TypeTraitWorkspace"
	def __init__(self):
		super(TypeTraitWorkspace, self).__init__(sbgarchitecture.Trait)
		workspaceMainLoop(self.commands)
class InstanceWorkspace(Workspace):
	def __init__(self, target_instance):
		super(InstanceWorkspace, self).__init__()
		self.target_instance = target_instance
		self.commands["delete"] = (destroyInstance(self.target_instance), "Will delete the current instance. Irreversible.")
		self.commands["aspectlist"] = (outlineAspects(self.target_instance), "Outlines the aspects of the current instance.")
		self.commands["aspectdetail"] = (detailPluralAspect(self.target_instance), "Details constituents of specified aspect.")
		self.commands["edit"] = (workspaceSelectAspect(self.target_instance), "Allows editing of aspects.")

def firstTimeSetup(): #TODO make less hardcoded.
	continue_loop = True
	while continue_loop: #TOCHECK Maybe there's a better way to do this flow control
		print("This will set up all information necessary to use Panocular. Doing so will wipe any data that already exists. Continue?")
		response = input("(Y/N): ")
		if checkBinary(response, False) == 0:
			sys.exit("First time set up cancelled.")
		creation_dict = dict()
		creation_dict["existence_trust"] = 1.0
		creation_dict["self_trust"] = 1.0
		try:
			creation_dict["name"] = createSingularAspect(sbgarchitecture.Entity, "name", "the current user")
			sbgarchitecture.Entity(creation_dict, True, True, False)
			continue_loop = False
		except TypeError:
			print("Invalid type")
	loader.writeAllJSONData()
	print("All data created successfully.")
for i in loader.all_datatypes:
	if os.path.exists(f"JSONData/{i.subglobal_type}.json") == False:
		print("Invalid data detected. Moving on to first time set up...")
		firstTimeSetup()
loader.loadAllJSONData()
print("Data loaded. Moving to main prompt...")