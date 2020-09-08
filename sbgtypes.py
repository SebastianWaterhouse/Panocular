entity_registry = dict()
relationship_registry = dict()
trait_registry = dict()
master_registry = dict()

entity_blueprint = {
	"target_registry": entity_registry, #What registry subglobals of this type should be sorted into
	"subglobal_type": "Entity", #What kind of subglobal datatype the entity is
	"readable_name_calculation": ["aspect_dict['name']", "' ('", "aspect_dict['hexdigest']", "')'"], #This is the human readable name of the datatype. Types with no readable name will use their hexdigest.
	"digest_calculation":["'entity'", "aspect_dict['name']"], #This is the formula for creating a unique hex digest. Put all variable names to use in the desired order.
	"aspect_blueprint":{ #All variables associated with this subglobal datatype. Syntax: "<variable name>":(<type (class>, "<description>", <singular (bool)>, <source registry (registry (None if no interpretation needed))>, "<readable name>", <required for instantiation (bool)>, ["<complementary aspect(s) in given registry (None instead of a list if no registry)>"], <data is entered manually (bool)>)
		"name":(str(), "the name of the entity", True, None, "Name", None, True), #All data needed to understand structure should be within these tuples
		"existence_trust":(float(), "the trust in the entity's existence", True, None, "Existence Trust", None, False),
		"self_trust":(float(), "trust in the entity", True, None, "Self Trust", None, False),
		"registrar":(str(), "registrar of the entity as hexdigest", True, entity_registry, "Registrar", ["registrees"], False),
		"registrees":(list(), "registrees of the entity as hexdigests", False, master_registry, "Registrees", ["registrar"], False),
		"editors":(list(), "editors of the entity as hexdigests", False, entity_registry, "Editors", ["edited"], False),
		"edited":(list(), "edited subglobals by entity as hexdigests", False, master_registry, "Edited items", ["editors"], False),
		"traits":(dict(), "traits of the entity {<trait hexdigest>:<trust>}", False, trait_registry, "Traits (trait: trust)", ["entities"], True),
		"relationships":(list(), "relationships of the entity as hexdigests", False, relationship_registry, "Relationships", ["origin", "targets"], False),
		"readable_name":(str(), "readable name of the entity", True, None, "Readable Name", None, False),
		"hexdigest":(str(), "unique identifier of the entity", True, None, "Hexdigest", None, False) #A hexdigest is MANDATORY for all types of subglobals!
	},
	"immutables":{ #Items about a subglobal that should not change after initialization. If boolean is true, it IS allowed to be modified through the actions of other pieces of code, but not manually
		"registrar":False,
		"hexdigest":False,
		"existence_trust":True,
		"self_trust":True,
		"registrees":True,
		"editors":True,
		"edited":True,
		"relationships":True,
	},
	"register_conditions":[ #The checks in other subglobals that must be made for an instance of this subglobal to be created.
		"registrar", #Aspect
		"registrees",
		"editors",
		"edited",
		"traits",
		"relationships"
	],
	"required_aspects":[ #The aspects of the subglobal necessary for instantiation
		"name",
		"existence_trust",
		"self_trust",
		"registrar",
		"hexdigest"
	]
}
relationship_blueprint = {
	"target_registry": relationship_registry,
	"subglobal_type": "Relationship",
	"readable_name_calculation": ["aspect_dict['hexdigest']"],
	"digest_calculation": ["aspect_dict['origin']", "aspect_dict['relative_status']", "aspect_dict['reverse_status']"],
	"aspect_blueprint":{
		"registrar":(str(), "registrar of the relationship as a hexdigest", True, entity_registry, "Registrar", ["registrees"], False),
		"origin":(str(), "origin of the relationship as a hexdigest", True, entity_registry, "Origin", ["relationships"], True),
		"relative_status":(str(), "status of the target(s) relative to the origin", True, None, "Target Status", None, True),
		"reverse_status":(str(), "status of the origin relative to the target(s)", True, None, "Origin Status", None, True),
		"trust":(float(), "trust in the existence of the relationship", True, None, "Trust", None, False),
		"targets":(list(), "target(s) of the relationship as hexdigests", False, entity_registry, "Target(s)", ["relationships"], True),
		"categories":(list(), "categories of the relationship", False, None, "Categories", None, True),
		"editors":(list(), "editors of the relationship as hexdigests", False, entity_registry, "Editors", ["edited"], False),
		"origin_traits":(list(), "relevant traits of the origin", False, trait_registry, "Origin Traits", ["relationships"], True), #TODO implement a way of checking that referenced entities have these traits
		"target_traits":(list(), "relevant traits of the target(s)", False, trait_registry, "Target Traits", ["relationships"], True),
		"readable_name":(str(), "identifier of the relationship", True, None, "Readable Name", None, False),
		"hexdigest":(str(), "unique identifier of the relationship", True, None, "Hexdigest", None, False)
	},
	"immutables":{
		"registrar":False,
		"hexdigest":False,
		"origin":True,
		"trust":True,
		"targets":True,
		"editors":True,
	},
	"register_conditions":[
		"registrar",
		"origin",
		"targets",
		"editors",
		"origin_traits",
		"target_traits"
	],
	"required_aspects":[
		"registrar",
		"origin",
		"relative_status",
		"reverse_status",
		"trust",
		"targets",
		"hexdigest"
	]
}
trait_blueprint = {
	"target_registry": trait_registry,
	"subglobal_type": "Trait",
	"readable_name_calculation": ["aspect_dict['name']", "' ('", "aspect_dict['hexdigest']", "')'"],
	"digest_calculation": ["'trait'", "aspect_dict['name']"],
	"aspect_blueprint":{
		"name":(str(), "name of the trait", True, None, "Name", None, True),
		"trust":(float(), "trust in the existence of the trait", True, None, "Trust", None, False),
		"registrar":(str(), "registrar of the trait", True, entity_registry, "Registrar", ["registrees"], False),
		"editors":(list(), "editors of the trait", False, entity_registry, "Editors", ["edited"], False),
		"relationships":(list(), "relationships associated with this trait", False, relationship_registry, "Relationships", ["origin_traits", "target_traits"], False),
		"entities":(list(), "entities with this trait", False, entity_registry, "Entities", ["traits"], False),
		"categories":(list(), "categories of the trait", False, None, "Categories", None, True),
		"readable_name":(str(), "readable name of the trait", True, None, "Readable Name", None, False),
		"hexdigest":(str(), "unique identifier of the trait", True, None, "Hexdigest", None, False)
	},
	"immutables":{
		"name":False,
		"registrar":False,
		"hexdigest":False,
		"trust":True,
		"editors":True,
		"relationships":True,
		"entities":True,
	},
	"register_conditions":[
		"relationships",
		"entities",
	],
	"required_aspects":[
		"name",
		"trust",
		"registrar",
		"hexdigest",
	]
}