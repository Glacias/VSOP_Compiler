# -----------------------------------------------------------------------------
# myLLVMGenerator.py
#
# File responsible for the LLVM IR code generation
# Made by Simon Bernard and Ivan Klapka for the Project 4 : code generation
# University of Liège - Academic year 2019-2020 - INFO0085-1 Compilers course
# -----------------------------------------------------------------------------
import sys
import queue
from myASTExt import *
from mySemanticAnalysisExt import globalSymbolTable
from llvmlite import ir
from collections import OrderedDict

# generateLLVM is the main function of the code generation
#  It return the llvm generator
def generateLLVM(ast, gst, file):
	# Create the llvm code generator
	lgen = llvmGenerator(ast, gst, file)

	# Initialize the classes
	lgen.generateAllClass()

	# Launch it on the tree
	ast.codeGen(lgen)

	# Return the lgen holding the code
	return lgen

# This class is responsible for storing all the useful
# information linked to code generation
class llvmGenerator:
	def __init__(self, ast, gst, file):
		# Get the tree and global symbol table
		self.ast = ast
		self.gst = gst

		# Save the file name
		self.file_name = file

		# Create the types
		self.int64 = ir.IntType(64)
		self.int32 = ir.IntType(32)
		self.int8 = ir.IntType(8)
		self.boolean = ir.IntType(1)
		self.void = ir.VoidType()
		self.double = ir.DoubleType()

		# Create the llvmlite module
		self.module = ir.Module(name=file)

		# Create a dictionnary for initialisation of the vtable and structures
		# This structure allows to acces usefull information such as function declaration
		# so we can define them later on 
		self.initDict = self.initializeStructAndVTables(ast, gst)

		# Dictionnary for externals foreign functions
		self.extDict = self.initializeExtDict()

		# Save the number of string created
		self.nbrStr = 0

	# Return a dictionnary for external foreign function
	#  with already declared foreign function inside
	def initializeExtDict(self):
		extDict = {}
		# Create sub module (this is also done to avoid redefining Object)
		moduleExt = ir.Module(name="moduleExt")
		# Exit
		fnty = ir.FunctionType(self.void, [self.int32])
		fn = ir.Function(moduleExt, fnty, name="exit")
		extDict["exit"] = [fnty, fn]
		# Free
		fnty = ir.FunctionType(self.void, [self.int8.as_pointer()])
		fn = ir.Function(moduleExt, fnty, name="free")
		extDict["free"] = [fnty, fn]
		# isspace
		fnty = ir.FunctionType(self.int32, [self.int32])
		fn = ir.Function(moduleExt, fnty, name="isspace")
		extDict["isspace"] = [fnty, fn]
		# malloc
		fnty = ir.FunctionType(self.int8.as_pointer(), [self.int64])
		fn = ir.Function(moduleExt, fnty, name="malloc")
		extDict["malloc"] = [fnty, fn]
		# realloc
		fnty = ir.FunctionType(self.int8.as_pointer(), [self.int8.as_pointer(), self.int64])
		fn = ir.Function(moduleExt, fnty, name="realloc")
		extDict["realloc"] = [fnty, fn]
		# strlen
		fnty = ir.FunctionType(self.int64, [self.int8.as_pointer()])
		fn = ir.Function(moduleExt, fnty, name="strlen")
		extDict["strlen"] = [fnty, fn]
		# strncmp
		fnty = ir.FunctionType(self.int32, [self.int8.as_pointer(), self.int8.as_pointer(), self.int64])
		fn = ir.Function(moduleExt, fnty, name="strncmp")
		extDict["strncmp"] = [fnty, fn]
		# strtoll
		fnty = ir.FunctionType(self.int64, [self.int8.as_pointer(), self.int8.as_pointer(), self.int32])
		fn = ir.Function(moduleExt, fnty, name="strtoll")
		extDict["strtoll"] = [fnty, fn]
		# Return the dict
		return extDict
	# Return a dictionnary for initialisation of the vtable and structures
	def initializeStructAndVTables(self, ast, gst):
		# Create the dictonnary
		initDict = {}

		# Add the primitives types to the dictionnary
		initDict["int32"] = [self.int32]
		initDict["bool"] = [self.boolean]
		initDict["string"] = [self.int8.as_pointer()]
		initDict["unit"] = [self.void]
		
		### Do a link with object.ll
		# Make Object and his functions accessible
		# Create a unused context so it is not redefined (we can use object.ll)
		ctxObj = ir.Context()
		# Create sub module for object (this is also done to avoid redefining Object)
		moduleObject = ir.Module(name="moduleObject")
		structObj = ctxObj.get_identified_type("struct.Object")
		structObjVTable = ctxObj.get_identified_type("struct.ObjectVTable")

		# Set the body of the structure
		structObj.set_body(structObjVTable.as_pointer())

		# Create the methods type
		object_print_fnty = ir.FunctionType(structObj.as_pointer(), [structObj.as_pointer(), self.int8.as_pointer()])
		object_printBool_fnty = ir.FunctionType(structObj.as_pointer(), (structObj.as_pointer(), self.boolean))
		object_printInt32_fnty = ir.FunctionType(structObj.as_pointer(), (structObj.as_pointer(), self.int32))
		object_inputLine_fnty = ir.FunctionType(self.int8.as_pointer(), [structObj.as_pointer()])
		object_inputBool_fnty = ir.FunctionType(self.boolean, [structObj.as_pointer()])
		object_inputInt32_fnty = ir.FunctionType(self.int32, [structObj.as_pointer()])

		# Create the methods declaration
		object_print = ir.Function(moduleObject, object_print_fnty, name='Object_print')
		object_printBool = ir.Function(moduleObject, object_printBool_fnty, name='Object_printBool')
		object_printInt32 = ir.Function(moduleObject, object_printInt32_fnty, name='Object_printInt32')
		object_inputLine = ir.Function(moduleObject, object_inputLine_fnty, name='Object_inputLine')
		object_inputBool = ir.Function(moduleObject, object_inputBool_fnty, name='Object_inputBool')
		object_inputInt32 = ir.Function(moduleObject, object_inputInt32_fnty, name='Object_inputInt32')

		# Set the body of the VTable
		structObjVTable.set_body(object_print_fnty.as_pointer(), object_printBool_fnty.as_pointer(), object_printInt32_fnty.as_pointer(), object_inputLine_fnty.as_pointer(), object_inputBool_fnty.as_pointer(), object_inputInt32_fnty.as_pointer())

		# Structure Object Dict
		structObjDict = OrderedDict()

		# Vtable Object Dict
		vtableObjDict = OrderedDict()

		# Fill vtable dict
		vtableObjDict["print"] = (0, object_print_fnty, object_print)
		vtableObjDict["printBool"] = (1, object_printBool_fnty, object_printBool)
		vtableObjDict["printInt32"] = (2, object_printInt32_fnty, object_printInt32)
		vtableObjDict["inputLine"] = (3, object_inputLine_fnty, object_inputLine)
		vtableObjDict["inputBool"] = (4, object_inputBool_fnty, object_inputBool)
		vtableObjDict["inputInt32"] = (5, object_inputInt32_fnty, object_inputInt32)

		# Generate init and new
		object_new_fnty = ir.FunctionType(structObj.as_pointer(), ())
		object_new = ir.Function(moduleObject, object_new_fnty, name='Object_new')
		object_init_fnty = ir.FunctionType(structObj.as_pointer(), [structObj.as_pointer()])
		object_init = ir.Function(moduleObject, object_init_fnty, name='Object_init')

		# Add Object vtable and struct to the dictionnary
		# Init Dict Info contains :
		# 0) The identified struct of the object
		# 1) The identified struct of the object's vtable
		# 2) The dictionnary of field's types
		# 3) The dictionnary of methods (vtable)
		# 4) The object_new
		# 5) The object_init
		# 6) The constant vtable (except for Object)
		initDict["Object"] = [structObj.as_pointer(), structObjVTable, structObjDict, vtableObjDict, object_new, object_init]

		# Store the declaration of malloc (but avoid redeclaring it)
		malloc_fnty = ir.FunctionType(self.int8.as_pointer(0), [self.int64])
		malloc = ir.Function(moduleObject, malloc_fnty, name='malloc')
		initDict["_malloc"] = malloc # will not collide with class because class start with a maj

		# Declare the pow function from C library
		power_fnty = ir.FunctionType(self.double, [self.double, self.double])
		power = ir.Function(self.module, power_fnty, name='pow')
		# Also declare the function to cast for int
		power_fnty_int = ir.FunctionType(self.int32, [self.int32, self.int32]).as_pointer()
		initDict["_pow"] = [power, power_fnty_int]

		# Declare the strcmp from C library
		strcmp_fnty = ir.FunctionType(self.int32, [self.int8.as_pointer(), self.int8.as_pointer()])
		strcmp = ir.Function(self.module, strcmp_fnty, name='strcmp')
		initDict["_strcmp"] = strcmp

		return initDict


	# This function is responsible for creating declaration code for all the classes
	#  and fill the init dictionary with the corresponding useful information
	def generateAllClass(self):
		# Declare the externals
		for ext in self.ast.list_ext:
			# Check that it is not already defined
			ExtDictInfo = self.extDict.get(ext.name)
			if ExtDictInfo is not None:
				continue
			# Get the llvmlite type of the return type
			llvmExtFFReturnType = self.initDict[ext.type.type][0]
			# Get the list of llvmlite types of the formals
			ls_formals = []
			for fm in ext.formals.list_formals:
				# Skip the unit
				if fm.type.type == "unit":
					continue
				ls_formals.append(self.initDict[fm.type.type][0])

			# Create the external foreign function type
			llvmExtFFType = ir.FunctionType(llvmExtFFReturnType, ls_formals)
			# Declare the external foreign function
			llvmExtFF = ir.Function(self.module, llvmExtFFType, name=(ext.name))
			# Add the info to the external dict
			self.extDict[ext.name] = [llvmExtFFType, llvmExtFF]
		# Declare all class structure and VTable (before their body) and their method new and init
		for cl in self.ast.list_class:
			# Struct and VTable
			structClass = ir.global_context.get_identified_type("struct." + cl.name)
			structClassVTable = ir.global_context.get_identified_type("struct." + cl.name + "VTable")
			# New
			class_new_fnty = ir.FunctionType(structClass.as_pointer(), ())
			class_new = ir.Function(self.module, class_new_fnty, name=(cl.name + '_new'))
			# Init
			class_init_fnty = ir.FunctionType(structClass.as_pointer(), [structClass.as_pointer()])
			class_init = ir.Function(self.module, class_init_fnty, name=(cl.name + '_init'))
			# Add
			self.initDict[cl.name] = [structClass, structClassVTable, "", "", class_new, class_init, []]

		## Now fill the dict for all the class and generate corresponding code
		for cl in self.ast.list_class:
			self.generateClass(cl)


	## Create the structure types for the class instances and vtable (take inheritance in account)
	# A class will also generate her ancestors if they were not already
	def generateClass(self, cl):
		# Look for the class in the init dict
		clInitDictInfo = self.initDict.get(cl.name)
		# Check that the class is not already declared
		if clInitDictInfo[2] == "":
			# Get info from parent
			parInitDictInfo = self.initDict.get(cl.parent)
			# If the parent is not declared, declare it
			if parInitDictInfo[2] == "":
				parInfo = self.gst.lookupForClass(cl.parent)
				self.generateClass(parInfo[0])

			# Now we know the parent was declared, copy his info
			clInitDictInfo[2] = parInitDictInfo[2].copy()
			clInitDictInfo[3] = parInitDictInfo[3].copy()

			# Keep the number of fields and methods inside the parent
			nbrField = len(clInitDictInfo[2]) + 1
			# For each unit field, remove one
			for n,t in clInitDictInfo[2].items():
				if t[1] == self.void:
					nbrField = nbrField - 1
			nbrMeth = len(clInitDictInfo[3])

			# Add the fields
			for fl in cl.fields:
				# If the type is unit, skip it
				if fl.type.type == "unit":
					nbrField = nbrField - 1
				# Get the llvmlite type
				llvmFieldType = self.initDict[fl.type.type][0]
				clInitDictInfo[2][fl.name] = (nbrField, llvmFieldType)
				nbrField = nbrField + 1

			# Set the body for the structure
			ls_fieldType = [clInitDictInfo[1].as_pointer()]
			for n,t in clInitDictInfo[2].items():
				# If void skip
				if t[1] == self.void :
					continue
				ls_fieldType.append(t[1])
			clInitDictInfo[0].set_body(*ls_fieldType)

			# From now an object is represented by its pointer
			clInitDictInfo[0] = clInitDictInfo[0].as_pointer()

			# Add the methods (and declare them) (and change the return type (why?))
			for mt in cl.methods:
				# Get the llvmlite type of the return type
				llvmMethodReturnType = self.initDict[mt.type.type][0]
				# Get the list of llvmlite types of the formals
				ls_formals = [clInitDictInfo[0]]  # Add the pointer to the class as first argument
				for fm in mt.formals.list_formals:
					# Skip the unit
					if fm.type.type == "unit":
						continue
					ls_formals.append(self.initDict[fm.type.type][0])

				# Create the method type
				llvmMethodType = ir.FunctionType(llvmMethodReturnType, ls_formals)

				# Check for method main exception
				methodLLVMName = cl.name + "_method_" + mt.name
				if methodLLVMName == "Main_method_main":
					methodLLVMName = "main"

				# Declare the method
				llvmMethod = ir.Function(self.module, llvmMethodType, name=(methodLLVMName))

				# Check if the method is overwritten
				infoOverMethod = clInitDictInfo[3].get(mt.name)
				if infoOverMethod is None:
					# If it is not overwritten, add it
					clInitDictInfo[3][mt.name] = (nbrMeth, llvmMethodType, llvmMethod)
					nbrMeth = nbrMeth + 1
				else:
					# If it is overwritten keep the number
					clInitDictInfo[3][mt.name] = (infoOverMethod[0], llvmMethodType, llvmMethod)

			# Set the body for the VTable
			ls_method = []
			ls_methodType = []
			for n,t in clInitDictInfo[3].items():
				ls_method.append(t[2])
				ls_methodType.append(t[1].as_pointer())
			clInitDictInfo[1].set_body(*ls_methodType)

			# Set the constant VTable
			c = ir.Constant(clInitDictInfo[1], ls_method)
			g = ir.GlobalVariable(self.module, c.type, cl.name + "_vtable")
			g.initializer = c
			g.global_constant = True

			# Add the constant to the dict
			clInitDictInfo[6] = g
