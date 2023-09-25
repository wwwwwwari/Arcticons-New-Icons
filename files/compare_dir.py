import os
import sys
import argparse

#usage example:
# python compare_dir.py 2023-09-18/svg/opti ../../Arcticons/icons/white/ -p0
def prepare_arguments():	
	parser = argparse.ArgumentParser(prog="python3 compare_dir.py", description="compare file names from two directories")
	parser.add_argument("dir1", help="the first directory to be compared")
	parser.add_argument("dir2", help="the second directory to be compared")
	parser.add_argument("-p0", "--print-same", action="store_true", help="print common files in both directories to console (default no)")
	parser.add_argument("-p1", "--print-only1", action="store_true", help="print exlusive files in the first directory to console (default no)")
	parser.add_argument("-p2", "--print-only2", action="store_true", help="print exlusive files in the second directory to console (default no)")
	parser.add_argument("-w", "--write", action="store_true", help="write file if specified -w. default = no write")
	parser.add_argument("-dw", "--write-dir", nargs='?', default=os.path.dirname(os.path.realpath(__file__)), help="output directory, only used if output lists are to be written to files. default the same as this script")
	del(sys.argv[0])
	args = parser.parse_args(sys.argv)
	
	if not os.path.exists(args.dir1) or os.path.isfile(args.dir1):
		print("Error: the first directory is not a valid directory")
		sys.exit()
	if not os.path.exists(args.dir2) or os.path.isfile(args.dir2):
		print("Error: the second directory is not a valid directory")
		sys.exit()	
	if args.write and (not os.path.exists(args.write_dir) or os.path.isfile(args.write_dir)):
		print("Error: the output directory (-dw, --write-dir) is not a valid directory")
		sys.exit()
		
	return args

def compare_directories(dir1, dir2):
	dir1_files = set(os.listdir(dir1))
	dir2_files = set(os.listdir(dir2))
		
	return list(dir1_files.intersection(dir2_files)), list(dir1_files.difference(dir2_files)), list(dir2_files.difference(dir1_files))
	
def write_file(file_list, file_name):
	with open(os.path.join(args.write_dir,file_name), 'w') as f:
		for file_listed in sorted(file_list):
			f.write(file_listed + "\n")
	
if __name__ == "__main__":
	args = prepare_arguments()
	samefiles, dir1only, dir2only = compare_directories(args.dir1, args.dir2)
	print("Duplicate files in both directories: " + str(len(samefiles)))
	if args.print_same:
		for listed_file in samefiles:
			print("\t" + listed_file)
	print("Files only in the first directory: " + str(len(dir1only)))
	if args.print_only1:
		for listed_file in dir1only:
			print("\t" + listed_file)
	print("Files only in the second directory: " + str(len(dir2only)))
	if args.print_only2:
		for listed_file in dir2only:
			print("\t" + listed_file)
	
	if(args.write):
		write_file(samefiles, "samefile.txt")
		write_file(dir1only, "dir1only.txt")
		write_file(dir2only, "dir2only.txt")
