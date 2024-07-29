#!/usr/bin/python3
import argparse
import os
import re
import shutil
import sys

# REPLACER
# Enforce stroke-color as #fff, stroke-width as 1, linejoin/linecap as round, fill-opacity to 0 in all SVGs in a given directory
# See usage: python3 replacer.py --help
# Dependencies: none
#
# WARNING! This script is made to fit Wari's icon-making workflows
# It will force the following even if the Arcticons project may accept them as exceptions
# - All fills are removed (fill opacity will become 0) -- even if it is a small white dot
# - All stroke widths are forced to 1 (a warning may be given if the <style> is not detected

REGEX_STROKE_COLOR_1 = r"stroke=\s*[\"\'](?:rgba?\(\d{1,3},\d{1,3},\d{1,3}(?:,\d{1,3})?\)|#[a-fA-F\d]{3,6})[\"\']" # ex. stroke="#123456"
REGEX_STROKE_COLOR_2 = r"stroke:\s*(?:rgba?\(\d{1,3},\d{1,3},\d{1,3}(?:,\d{1,3})?\)|#[a-fA-F\d]{3,6})" # ex. stroke:#123456
REGEX_STROKE_WIDTH_1 = r"stroke-width=\s*[\"\'](?:\d+(?:\.\d+)?|\.\d+)[\"\']" # ex. stroke-width="0.99987"
REGEX_STROKE_WIDTH_2 = r"stroke-width:\s*(?:\d+(?:\.\d+)?|\.\d+)" # ex. stroke-width:0.99987
REGEX_STROKE_LINEJOIN_1 = r"stroke-linejoin=\s*[\"\'](?:arcs|bevel|miter|miter-clip)[\"\']" # ex. stroke-linejoin="miter"
REGEX_STROKE_LINEJOIN_2 = r"stroke-linejoin:\s*(?:arcs|bevel|miter|miter-clip)" # ex. stroke-linejoin:miter
REGEX_STROKE_LINECAP_1 = r"stroke-linecap=\s*[\"\'](?:butt|square)[\"\']" # ex. stroke-linejoin="butt"
REGEX_STROKE_LINECAP_2 = r"stroke-linecap:\s*(?:butt|square)" # ex. stroke-linejoin:butt
REGEX_FILL_OPACITY_1 = "fill-opacity=\s*[\"\'](?:\d+(?:\.\d+)?|\.\d+)%?[\"\']" # ex. fill-opacity="50%"
REGEX_FILL_OPACITY_2 = "fill-opacity:\s*(?:\d+(?:\.\d+)?|\.\d+)%?" # ex. fill-opacity:50%

REPL_STROKE_COLOR_1 = "stroke=\"#fff\""
REPL_STROKE_COLOR_2 = "stroke:#fff"
REPL_STROKE_WIDTH_1 = "stroke-width=\"1\""
REPL_STROKE_WIDTH_2 = "stroke-width:1"
REPL_STROKE_LINEJOIN_1 = "stroke-linejoin=\"round\""
REPL_STROKE_LINEJOIN_2 = "stroke-linejoin:round"
REPL_STROKE_LINECAP_1 = "stroke-linecap=\"round\""
REPL_STROKE_LINECAP_2 = "stroke-linecap:round"
REPL_FILL_OPACITY_2 = "fill-opacity=\"0\""
REPL_FILL_OPACITY_1 = "fill-opacity:0"

STYLE_TAG_TOKEN = "</style>"

RC_OK = 0
RC_WARN = 4
RC_ERR = 16

def init_args():
	parser = argparse.ArgumentParser(description="Enforce stroke-color as #fff, stroke-width as 1, linejoin/linecap as round, fill-opacity to 0 in all SVGs in a given directory")
	parser.add_argument("indir", help="Input directory")
	parser.add_argument("outdir", help="Output directory")
	parser.add_argument("--verbose", help="Print detailed information", action="store_true")
	parser.add_argument("--no-delete", help="Do not delete the output directory if exists (abort instead)", action="store_true")
	args = parser.parse_args()
	return args	

def dir_validate(args):
	if not os.path.isdir(args.indir):
		print(f"Directory {args.indir} does not exist or is not a directory. Aborting.")
		sys.exit(RC_ERR)
	if os.path.exists(args.outdir):
		if os.path.isdir(args.outdir):
			if args.no_delete:
				print(f"Directory {args.outdir} exists and --no-delete flag was passed. Aborting.")
				sys.exit(RC_ERR)
			if args.verbose:
				print(f"Removing the existing directory {args.outdir}.")
			try:
				shutil.rmtree(args.outdir)
			except OSError as e:
				print(f"Error removing the directory {args.outdir}: {e}.")
				sys.exit(RC_ERR)
		else:
			print(f"{args.outdir} is not a directory. Aborting.")
			sys.exit(RC_ERR)
	try:
		os.makedirs(args.outdir)
		if (args.verbose):
			print(f"Created the directory {args.outdir}.")
	except Exception as e:
		print(f"Error creating the directory {outdir}: {e}.")
		sys.exit(RC_ERR)
	if args.verbose:
		print()
		print(f"Input directory: {args.indir}.")
		print(f"Output directory: {args.outdir}.")
		print()
	
	return

def replacer(verbose, indir, outdir, svgfilename):
	return_code = RC_OK
	svgfilepath_in = os.path.join(indir, svgfilename)
	svgfilepath_out = os.path.join(outdir, svgfilename)
	svgcontent = None
	if verbose:
		print(f"Processing {svgfilename}.")
	
	try:
		svgfile_in = open(svgfilepath_in, "r")
	except Exception as e:
		print(f"Error opening {svgfilepath_in}: {e}.")
		sys.exit(RC_ERR)
	
	try:
		svgcontent = svgfile_in.read()
	except Exception as e:
		print(f"Error reading {svgfilepath_in}: {e}.")
		sys.exit(RC_ERR)
	finally:
		svgfile_in.close()
	
	if STYLE_TAG_TOKEN not in svgcontent:
		print(f"\tWARNING: <style> tag is not present in {svgfilename}. Forcing stroke-width to 1 may result in the stroke-widths being completely wrong.")
		return_code = RC_WARN
	
	svgcontent = re.sub(REGEX_STROKE_COLOR_1, REPL_STROKE_COLOR_1, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_COLOR_2, REPL_STROKE_COLOR_2, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_WIDTH_1, REPL_STROKE_WIDTH_1, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_WIDTH_2, REPL_STROKE_WIDTH_2, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_LINEJOIN_1, REPL_STROKE_LINEJOIN_1, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_LINEJOIN_2, REPL_STROKE_LINEJOIN_2, svgcontent)	
	svgcontent = re.sub(REGEX_STROKE_LINECAP_1, REPL_STROKE_LINECAP_1, svgcontent)
	svgcontent = re.sub(REGEX_STROKE_LINECAP_2, REPL_STROKE_LINECAP_2, svgcontent)
	
	try:
		svgfile_out = open(svgfilepath_out, "w")
		svgfile_out.write(svgcontent)
	except PermissionError as e:
		print(f"No permission to write {svgfilepath_out: {e}}")
		sys.exit(RC_ERR)
	except Exception as e:
		print(f"Error writing {svgfilepath_out}: {e}.")
		sys.exit(RC_ERR)
	finally:
		svgfile_out.close()
	
	if verbose:
		print(f"Successfully processed {svgfilename}\n")
	
	return return_code

def main():
	return_code = RC_OK
	args = init_args()
	dir_validate(args)

	for f in os.listdir(args.indir):
		if f.endswith(".svg"):
			rc = replacer(args.verbose, args.indir, args.outdir, f)
			return_code = max(rc, return_code)
	sys.exit(return_code)
if __name__ == "__main__":
	main()
