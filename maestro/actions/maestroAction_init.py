#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2012, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

from maestro import debug
from maestro import tools
from maestro import env
from maestro import multiprocess
import os

def help():
	return "plop"

def execute(arguments):
	debug.info("execute:")
	for elem in arguments:
		debug.info("    '" + str(elem.get_arg()) + "'")
	if len(arguments) == 0:
		debug.error("Missing argument to execute the current action ...")
	
	# the configuration availlable:
	branch = "master"
	manifest_name = "default.xml"
	address_manifest = ""
	for elem in arguments:
		if elem.get_option_name() == "branch":
			debug.info("find branch name: '" + elem.get_arg() + "'")
			branch = elem.get_arg()
		elif elem.get_option_name() == "manifest":
			debug.info("find mmanifest name: '" + elem.get_arg() + "'")
			manifest_name = elem.get_arg()
		elif elem.get_option_name() == "":
			if address_manifest != "":
				debug.error("Manifest adress already set : '" + address_manifest + "' !!! '" + elem.get_arg() + "'")
			address_manifest = elem.get_arg()
		else:
			debug.error("Wrong argument: '" + elem.get_option_name() + "' '" + elem.get_arg() + "'")
	
	if address_manifest == "":
		debug.error("Init: Missing manifest name")
	
	debug.info("Init with: '" + address_manifest + "' branch='" + branch + "' name of manifest='" + manifest_name + "'")
	
	
	# check if .XXX exist (create it if needed)
	if     os.path.exists(env.get_maestro_path()) == True \
	   and os.path.exists(env.get_maestro_path_config()) == True \
	   and os.path.exists(env.get_maestro_path_manifest()) == True:
		debug.error("System already init: path already exist: '" + str(env.get_maestro_path()) + "'")
	tools.create_directory(env.get_maestro_path())
	# check if the git of the manifest if availlable
	
	# create the file configuration:
	data = "repo=" + address_manifest + "\nbranch=" + branch + "\nfile=" + manifest_name
	tools.file_write_data(env.get_maestro_path_config(), data)
	
	#clone the manifest repository
	cmd = "git clone " + address_manifest + " --branch " + branch + " " + env.get_maestro_path_manifest()
	
	debug.info("clone the manifest")
	ret = multiprocess.run_command_direct(cmd)
	
	if ret == "":
		return True
	
	if ret == False:
		# all is good, ready to get the system work corectly
		return True
	debug.info("'" + ret + "'")
	debug.error("Init does not work")
	return False

