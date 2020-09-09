import hashlib, sbgtypes

def makeHash(digest_calculation, aspect_dict):
	digest_calculated = []
	for g in digest_calculation:
		digest_calculated.append(eval(g))
	return str(hashlib.blake2b(bytes(str().join(digest_calculated), 'utf-8'), digest_size=32).hexdigest())
def makeReadableName(readable_name_calculation, aspect_dict):
	readable_name_calculated = []
	for g in readable_name_calculation:
		readable_name_calculated.append(eval(g))
	return str().join(readable_name_calculated)
def iterateCreation(target_class, source_dict, from_scratch, own_registrar, loaded): #Iterates through the aspects of a subglobal and assigns values properly. Must pass ALL aspects as kwargs except hexdigest and readable_name, which are made automatically
	if from_scratch:
		source_dict["hexdigest"] = makeHash(target_class.digest_calculation, source_dict)
		source_dict["readable_name"] = makeReadableName(target_class.readable_name_calculation, source_dict)
	if own_registrar:
		source_dict["registrar"] = source_dict["hexdigest"]
		source_dict["registrees"] = [source_dict["hexdigest"]]
	try:
		for g in target_class.required_aspects: #Ensures that all required items exist
			if g in source_dict:
				pass
			else:
				raise Exception(f"RequiredAspects")
		for g in target_class.register_conditions: #Ensures all items are referencing existing items
			if g in source_dict:
				if g != "registrar" and own_registrar == False or g != "registrees" and own_registrar == False or loaded == False:
					if target_class.aspect_blueprint[g][2]:
						if source_dict[g] in target_class.aspect_blueprint[g][3]:
							pass
						else:
							raise Exception("RegisterConditions")
					else:
						for gg in source_dict[g]:
							if source_dict[g][gg] in target_class.aspect_blueprint[g][3]:
								pass
							else:
								raise Exception("RegisterConditions")
		for g in source_dict:
			if type(target_class.aspect_blueprint[g][0]) == type(source_dict[g]):
				target_class.aspects[g] = source_dict[g]
			else:
				raise TypeError()
	except ValueError: #Possibly not necessary-
		raise ValueError("InvalidDict")
	except TypeError:
		raise TypeError("InvalidType")

#Rudimentary way to check permissions
def checkPermissions(required_approval, var_to_check, to_check_against): #List of all variables that must be true, variable whose existence to check, dict/list to check existence in.
	if var_to_check in to_check_against:
		for g in required_approval:
			if g == False:
				raise Exception()

def auditSubglobalRegistryLinks(target_type): #Ensures that all links between subglobal instances are valid, and, if not, removes them
	for g in target_type.target_registry:
		for gg in target_type.register_conditions:
			if target_type.aspect_blueprint[2]:
				if target_type.target_registry[g].aspects[gg] in target_type.target_registry[g].aspect_blueprint[gg][3]:
					target_type.target_registry[g].aspects[gg] = target_type.aspect_blueprint[gg][0]
			else:
				for ind, ggg in enumerate(target_type.target_registry[g].aspects[gg]):
					if ggg in target_type.aspect_blueprint[gg][3]:
						pass
					else:
						if type(target_type.aspect_blueprint[gg][0]) == type(list()):
							del target_type.target_registry[g].aspects[gg][ind]
						elif type(target_type.aspect_blueprint[gg][0]) == type(dict()):
							del target_type.target_registry[g].aspects[gg][ggg]

class SubglobalData(): #Each of the subglobal datatypes is a subclass
	def __init__(self, creation_dict, from_scratch, own_registrar, loaded): #creation_dict is a dictionary of the aspects, from_scratch is a boolean that tells it to generate a hexdigest and readable name
		self.aspects = dict()
		iterateCreation(self, creation_dict, from_scratch, own_registrar, loaded)
		sbgtypes.master_registry[self.aspects["hexdigest"]] = self
		self.target_registry[self.aspects["hexdigest"]] = self
	@classmethod
	def initDatatype(cls):
		cls.aspect_blueprint = cls.used_blueprint["aspect_blueprint"]
		cls.subglobal_type = cls.used_blueprint["subglobal_type"]
		cls.digest_calculation = cls.used_blueprint["digest_calculation"]
		cls.immutables = cls.used_blueprint["immutables"]
		cls.readable_name_calculation = cls.used_blueprint["readable_name_calculation"]
		cls.target_registry = cls.used_blueprint["target_registry"]
		cls.register_conditions = cls.used_blueprint["register_conditions"]
		cls.required_aspects = cls.used_blueprint["required_aspects"]

	def deleteInstance(self):
		del master_registry[self.aspects["hexdigest"]]
		del self.target_registry[self.aspects["hexdigest"]]
		auditSubglobalRegistryLinks(eval(self.subglobal_type))
	def updateAspect(self, target_aspect, new_value, editor, approved_process, plural_index): #Can be used with plural aspects by passing the index/key through plural_index. If not plural, pass None. Can be called for creation and editing
		try:
			checkPermissions([approved_process, self.immutables[target_aspect]], target_aspect, self.immutables)
			if self.aspect_blueprint[target_aspect][2]:
				self.aspects[target_aspect] = new_value
			else:
				if plural_index in self.aspects[target_aspect]:
					self.aspects[target_aspect][plural_index] = new_value
				else:
			 		raise IndexError
		except Exception:
			raise Exception("PermsError")
		except KeyError:
			raise KeyError()
		except IndexError:
			if target_aspect in self.register_conditions:
				if new_value not in self.aspect_blueprint[target_aspect][3]:
					raise IndexError()
			if type(self.aspect_blueprint[target_aspect][0]) == type(list()):
				self.aspects[target_aspect].append(new_value)
			elif type(self.aspect_blueprint[target_aspect][0]) == type(dict()):
				self.aspects[target_aspect][plural_index] = new_value
	def removeAspectEntry(self, target_aspect, editor, approved_process, plural_index, full_deletion): #Deletes an entry from an instance's plural aspect. full_deletion should only be called as part of the deletion of a separate instancess 
		try:
			checkPermissions([approved_process, self.immutables[target_aspect]], target_aspect, self.immutables)
			if self.aspect_blueprint[target_aspect][3] == None:
				del self.aspects[target_aspect][plural_index]
			else:
				for h in self.aspect_blueprint[target_aspect][5]:
					if self.aspects["hexdigest"] in self.aspect_blueprint[target_aspect][3][h]:
						checkPermissions([approved_process, self.aspect_blueprint[target_aspect][3][self.aspects["hexdigest"]].immutables[h]], h, self.aspect_blueprint[target_aspect][3][self.aspects["hexdigest"]].immutables)
						checkPermissions([full_deletion], h, self.aspect_blueprint[target_aspect][3][self.aspects["hexdigest"]].required_aspects)
					del self.aspect_blueprint[target_aspect][3][self.aspects["hexdigest"]].aspects[h][plural_index]
		except Exception:
			raise Exception("PermsError")


class Entity(SubglobalData):
	used_blueprint = sbgtypes.entity_blueprint
class Relationship(SubglobalData):
	used_blueprint = sbgtypes.relationship_blueprint
class Trait(SubglobalData):
	used_blueprint = sbgtypes.trait_blueprint