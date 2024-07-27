#!/usr/bin/python3
import argparse
import os
import requests
import sys
import time

from http import HTTPStatus

# DUPECHECKER
# Check all SVGs whether their names already exist in the Arcticons project
# See usage: python3 dupechecker.py --help
# Dependencies: python3-github (apt install python3-github or pip3 install pygithub requests)

COMBINED_XML = "combined_appfilter.xml"

GH_COMBINED_XML_URL = f"https://api.github.com/repos/Arcticons-Team/Arcticons/contents/docs/assets/{COMBINED_XML}"
GH_HEADER_ACCEPT_RAW = "application/vnd.github.raw+json"

COMPONENT_START_TAG = "\t<item component="

# how long does the cache file have to age until it is pulled again to avoid hitting GH's rate-limit
CACHE_EXPIRE_AGE = 1800

RC_OK = 0
RC_WARN = 4
RC_ERR = 16

def init_args():
	parser = argparse.ArgumentParser(description="Check all SVGs whether their names already exist in the Arcticons project on GitHub")
	parser.add_argument("indir", help="Input directory with all the SVGs you want to check")
	parser.add_argument("--verbose", help="Print detailed information", action="store_true")
	parser.add_argument("--force-reload", help="Force pulling the combined appfilter from GitHub, even if the file already exists and not enough time has passed since its last modified time (30 minutes)", action="store_true")

	args = parser.parse_args()
	return args	

def remove_old_combined_xml(verbose, xml_path):
	if verbose:
		print(f"Removing existing cache file.")
	try:
		os.remove(xml_path)
	except Exception as e:
		print(f"Error removing {xml_path}: {e}.")
		sys.exit(RC_ERR)
	return

def download_combined_xml(verbose, xml_path):
	if verbose:
		print(f"Downloading a new cache file from {GH_COMBINED_XML_URL}.")
	get_response = requests.get(GH_COMBINED_XML_URL, headers={"Accept":GH_HEADER_ACCEPT_RAW})
	if get_response.status_code == HTTPStatus.OK.value:
		if verbose:
			print(f"New cache file downloaded.")
		get_content = get_response.text
		try:
			new_cache_file = open(xml_path, "w")
		except Exception as e:
			print(f"Error opening {xml_path}: {e}.")
			sys.exit(RC_ERR)
		try:
			new_cache_file.write(get_content)
		except Exception as e:
			print(f"Error writing to {xml_path}: {e}.")
			sys.exit(RC_ERR)
		finally:
			new_cache_file.close()
		if verbose:
			print(f"New cache file saved.")	
	else:
		print(f"Error downloading a new cache file: {get_response.status_code} {get_response.reason}")
		sys.exit(RC_ERR)
	return
def process_combined_xml(verbose, xml_path, indir):
	#text.split("\"")[-2]
	if verbose:
		print(f"Processing the cache file.")
	try:
		cache_file = open(xml_path, "r")
	except Exception as e:
		print(f"Error opening {xml_path}: {e}.")
	try:
		content = cache_file.readlines()
	except Exception as e:
		print(f"Error reading {xml_path}: {e}.")
	finally:
		cache_file.close()
	cache_icon_arr = []
	for item in content:
		if item.startswith(COMPONENT_START_TAG):
			cache_icon_name = item.split("\"")[-2]
			cache_icon_arr.append(cache_icon_name)
	in_icon_arr = []
	if verbose:
		print(f"Processing the input directory {indir}.")
	for f in os.listdir(indir):
		if f.endswith(".svg"):
			in_icon_name = f.rsplit(".",1)[0]
			in_icon_arr.append(in_icon_name)
	matches = set(cache_icon_arr).intersection(set(in_icon_arr))
	return matches
def main():
	return_code = RC_OK
	script_path = os.path.dirname(os.path.realpath(__file__))
	xml_path = os.path.join(script_path, COMBINED_XML)

	args = init_args()
	
	if not os.path.isdir(args.indir):
		print(f"Directory {args.indir} does not exist or is not a directory. Aborting.")
		sys.exit(RC_ERR)
	if os.path.exists(xml_path):
		if not os.path.isfile(xml_path):
			print(f"{xml_path} is not a file. Aborting")
			sys.exit(RC_ERR)
		else:
			cache_modified = os.path.getmtime(xml_path)
			cache_modified_readable = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cache_modified))
			cache_age = time.time() - cache_modified
			if args.verbose:
				print(f"Found cache file {COMBINED_XML}.")
				print(f"Cache file last modified: {cache_modified_readable}.")
			if cache_age < CACHE_EXPIRE_AGE:
				if args.force_reload:
					if args.verbose:
						print(f"Cache not expired but --force-reload is passed. Will get a new cache file.")
					remove_old_combined_xml(args.verbose, xml_path)
					download_combined_xml(args.verbose, xml_path)
				else:
					if args.verbose:
						print(f"Cache not expired. Using the old cache file.")
			else:
				if args.verbose:
					print(f"Cache expired. Will get a new cache file.")
				remove_old_combined_xml(args.verbose, xml_path)
				download_combined_xml(args.verbose, xml_path)
	else:
		if args.verbose:
			print(f"Cache not exist. Will get a new cache file.")
		download_combined_xml(args.verbose, xml_path)
	matches = process_combined_xml(args.verbose, xml_path, args.indir)
	if len(matches) > 0:
		print(f"WARNING! {len(matches)} file name(s) duplicated with already existing icon name(s) in Arcticons:")
		return_code = max(RC_WARN, return_code)
	for item in matches:
		print(f"\t{os.path.join(args.indir,item)}.svg")
	return return_code
if __name__ == "__main__":
	main()

