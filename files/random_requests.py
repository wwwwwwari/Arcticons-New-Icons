#License: Unlicense
#Usage help: python3 random_requests.py --help

import datetime
import sys
import argparse
import random
import os
from enum import Enum
from pathlib import Path

class ErrorLevel(Enum):
	ERROR_LEVEL_CRITICAL = 0
	ERROR_LEVEL_WARNING = 1
	ERROR_LEVEL_INFORMATIONAL = 2

class ErrorName(Enum):
	FILE_NOT_READABLE = 1
	FILE_NOT_WRITABLE = 11
	FILE_NOT_EXISTS = 21
	FILE_OUT_IS_A_DIR = 22
	DIR_OUT_IS_A_FILE = 19
	DIR_IN_NOT_EXISTS = 20
	PARSE_HEADER_NOT_FOUND = 2
	PARSE_WHOLE_FILE_ENTRY_NOT_FOUND = 3
	PARSE_TOTAL_REQUESTS_NOT_DIVISIBLE = 4
	PARSE_ENTRY_WITHOUT_ENTRY_LINE = 5
	PARSE_ENTRY_WITHOUT_COMPONENT_LINE = 6
	PARSE_ENTRY_WITHOUT_GPLAY_LINE = 7
	PARSE_ENTRY_WITHOUT_FDROID_LINE = 8
	PARSE_ENTRY_WITHOUT_REQUEST_COUNTER_LINE = 9
	PARSE_ENTRY_WITHOUT_LAST_REQUESTED_TIME_LINE = 10
	INVALID_ARGUMENTS_NO_NUMBER = 12
	INVALID_ARGUMENTS_NEGATIVE_SKIP_POPULAR = 13
	INVALID_ARGUMENTS_NEGATIVE_THRESHOLD = 14
	INVALID_ARGUMENTS_TOO_BIG_NUMBER = 15
	INVALID_ARGUMENTS_TOO_BIG_SKIP_POPULAR = 16
	INVALID_ARGUMENTS_FILTER_RETURNS_NOTHING = 17
	WARNING_FILTERED_POPULATION_TOO_SMALL = 18

DEFAULT_NUMBER = 10
DEFAULT_SKIP_POPULAR = 0
DEFAULT_REQUEST_THRESHOLD = 1
ENTRY_STARTS_WITH = "<!--"
COMPONENT_STARTS_WITH = "<item"
GPLAY_STARTS_WITH = "https://play.google.com"
FDROID_STARTS_WITH = "https://f-droid.org"
REQUEST_COUNTER_STARTS_WITH = "Requested"
LAST_REQUESTED_TIME_STARTS_WITH = "Last"

DEFAULT_REQUESTS_FILE_NAME = "requests.txt"
DEFAULT_RANDOMIZED_REQ_FILE_NAME = "random_requests.txt"
DEFAULT_NEW_REQ_FILE_NAME = "new_requests.txt"

def prepare_arguments():	
	script_directory = os.path.dirname(os.path.realpath(__file__))
	parser = argparse.ArgumentParser(prog="python3 random_requests.py", description="randomly select Requests from "+DEFAULT_REQUESTS_FILE_NAME+". Copy Arcticons/other/"+DEFAULT_REQUESTS_FILE_NAME+" to the same folder as this script, then run the script. Randomly selected requests will be saved at random_requests.txt and the remaining requests at new_requests.txt in the same folder")
	parser.add_argument("-di", "--input-dir", nargs="?", const=script_directory, default=script_directory, help="directory of "+DEFAULT_REQUESTS_FILE_NAME+" (default=same as this script)")
	parser.add_argument("-do", "--output-dir", nargs="?", const=script_directory, default=script_directory, help="directory of the output files (default=same as this script)")
	parser.add_argument("-n", "--number", nargs="?", const=DEFAULT_NUMBER, default=DEFAULT_NUMBER, type=int, help="number of requests to be randomly selected (default=10)")
	parser.add_argument("-s", "--skip-popular", nargs="?", const=DEFAULT_SKIP_POPULAR, default=DEFAULT_SKIP_POPULAR, type=int, help="skip N most popular requests (default=0/no skip)")
	parser.add_argument("-t", "--request-threshold", nargs="?", const=DEFAULT_REQUEST_THRESHOLD, default=DEFAULT_REQUEST_THRESHOLD, type=int, help="selected requests must have been requested at least N times (default=1)")
	parser.add_argument("-v", "--verbose", action="store_true", help="show verbose output")
	
	del(sys.argv[0])
	args = parser.parse_args(sys.argv)

	if os.path.exists(args.input_dir):
		if not os.path.isfile(os.path.join(args.input_dir, DEFAULT_REQUESTS_FILE_NAME)):
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_NOT_EXISTS, DEFAULT_REQUESTS_FILE_NAME, args.input_dir)
	else:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.DIR_IN_NOT_EXISTS, args.input_dir)
	try:
		Path(args.output_dir).mkdir(parents=True, exist_ok=True)
		out_loc = os.path.join(args.output_dir, DEFAULT_RANDOMIZED_REQ_FILE_NAME)
		if os.path.exists(out_loc) and os.path.isdir(out_loc):
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_OUT_IS_A_DIR, out_loc)
		out_loc = os.path.join(args.output_dir, DEFAULT_NEW_REQ_FILE_NAME)
		if os.path.exists(out_loc) and os.path.isdir(out_loc):
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_OUT_IS_A_DIR, out_loc)
			
	except FileExistsError:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.DIR_OUT_IS_A_FILE, args.output_dir)

	if args.number < 1:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_NO_NUMBER, args.number)
	if args.request_threshold < 0:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_NEGATIVE_THRESHOLD, args.request_threshold)
	if args.skip_popular < 0:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_NEGATIVE_SKIP_POPULAR, args.skip_popular)

	print("Running with the following settings: ")
	print("- Randomly selecting", args.number, "request(s) that have been requested at least", args.request_threshold, "time(s)")
	print("- Skipping", args.skip_popular, "most popular request(s)")
	if args.verbose:
		print("- Verbose output enabled")
	
	return args

def line_counter(lines):
	header_end_idx = -1
	line_count_per_entry = 0
	for x in range(len(lines)):		
		if lines[x].startswith(ENTRY_STARTS_WITH):
			
			if header_end_idx == -1:
				header_end_idx = x
			else:
				line_count_per_entry = x - header_end_idx
				break
			
	return header_end_idx, line_count_per_entry		

def compute_final_population(lines, line_count_per_entry, args):
	combined_lines = []
	included_lines = []
	filter_request_threshold = args.request_threshold > DEFAULT_REQUEST_THRESHOLD
	filter_skip_popular = args.skip_popular > DEFAULT_SKIP_POPULAR
			
	for x in range(0, len(lines), line_count_per_entry):
		current_line = ""
		found_entry_line = False
		found_component_line = False
		found_gplay_line = False
		found_fdroid_line = False
		found_request_counter_line = False
		found_last_requested_time_line = False
		entry_app_name = ""
		entry_requested_times = 0
		entry_number = int((x + line_count_per_entry) / line_count_per_entry)
		skipped = False
		
		for entry_offset in range(0, line_count_per_entry):
			if not found_entry_line and lines[x + entry_offset].startswith(ENTRY_STARTS_WITH):
				found_entry_line = True
				entry_app_name = " ".join(lines[x + entry_offset].split(" ")[1:-1])
			if not found_component_line and lines[x + entry_offset].startswith(COMPONENT_STARTS_WITH):
				found_component_line = True
			if not found_gplay_line and lines[x + entry_offset].startswith(GPLAY_STARTS_WITH):
				found_gplay_line = True			
			if not found_fdroid_line and lines[x + entry_offset].startswith(FDROID_STARTS_WITH):
				found_fdroid_line = True			
			if not found_request_counter_line and lines[x + entry_offset].startswith(REQUEST_COUNTER_STARTS_WITH):
				found_request_counter_line = True			
				entry_requested_times = int(lines[x + entry_offset].split(" ")[1])
			if not found_last_requested_time_line and lines[x + entry_offset].startswith(LAST_REQUESTED_TIME_STARTS_WITH):
				found_last_requested_time_line = True			
			current_line += lines[x + entry_offset]
			
		if not found_entry_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_ENTRY_LINE, x, lines[x])
		if not found_component_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_COMPONENT_LINE, x, lines[x])
		if not found_gplay_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_GPLAY_LINE, x, lines[x])
		if not found_fdroid_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_FDROID_LINE, x, lines[x])
		if not found_request_counter_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_REQUEST_COUNTER_, x, lines[x])
		if not found_last_requested_time_line:
			print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_ENTRY_WITHOUT_LAST_REQUESTED_TIME_LINE, x, lines[x])
			
		if filter_skip_popular and args.skip_popular >= entry_number:
			if args.verbose:
				print("Skipping", entry_app_name, "due to being in", args.skip_popular,"most popular request(s)...")
			skipped = True
		
		if filter_request_threshold and args.request_threshold > entry_requested_times:
			if args.verbose:
				print("Excluded the entry for", entry_app_name, "due to the request threshold")
			skipped = True
		
		if not skipped:
			included_lines.append(current_line)	

		combined_lines.append(current_line)

	return combined_lines, included_lines

def print_error_handling(e_lvl, e_code, *args):	
	DEFAULT_PARSE_ERROR = "A logical error occurred while trying to parse "+DEFAULT_REQUESTS_FILE_NAME+". The format of the file may have been changed, please contact the script author."
	DEFAULT_INVALID_ARGUMENTS_ERROR = "An invalid argument was entered. Please correct the specified error and re-run the script."
	
	print("\n**************************************************************")
	match e_code:
		case ErrorName.FILE_NOT_READABLE:
			print("Error while trying to read", args[0])
			print("Ensure the file exists in the same folder as this script with correct permissions.")
		case ErrorName.FILE_NOT_WRITABLE:
			print("Error while trying to write", args[0])
			print("Ensure the script has necessary permissions to write the file.")
		case ErrorName.FILE_NOT_EXISTS:
			print("The file", args[0], "does not exist in", args[1])
		case ErrorName.FILE_OUT_IS_A_DIR:
			print("Error while validating the specified output file:", args[0])
			print("Ensure that the last component in the above path is not an existing directory (instead of a file) and re-run the script.")
			print("If you're not sure what this error means, just remove", args[0])
		case ErrorName.DIR_OUT_IS_A_FILE:
			print("Error while validating the specified output directory:", args[0])
			print("Ensure that the last component in the above path is not an existing file (instead of a directory) and re-run the script.")
			print("If you're not sure what this error means, just remove", args[0])
		case ErrorName.DIR_IN_NOT_EXISTS:
			print("The specified input directory", args[0], "does not exist")
		case ErrorName.PARSE_HEADER_NOT_FOUND:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find the file header.")
		case ErrorName.PARSE_WHOLE_FILE_ENTRY_NOT_FOUND:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any request entry in the entire file by searching for the word", ENTRY_STARTS_WITH)
		case ErrorName.PARSE_TOTAL_REQUESTS_NOT_DIVISIBLE:
			print(DEFAULT_PARSE_ERROR)
			print("Total number of lines divided by line count per request entry did not result in a whole number")
			print("There are", args[0], "request entries found, each of which was calculated to have", args[1], "lines")
		case ErrorName.PARSE_ENTRY_WITHOUT_ENTRY_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", ENTRY_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.PARSE_ENTRY_WITHOUT_COMPONENT_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", COMPONENT_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.PARSE_ENTRY_WITHOUT_GPLAY_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", GPLAY_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.PARSE_ENTRY_WITHOUT_FDROID_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", FDROID_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.PARSE_ENTRY_WITHOUT_ENTRY_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", REQUEST_COUNTER_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.PARSE_ENTRY_WITHOUT_ENTRY_LINE:
			print(DEFAULT_PARSE_ERROR)
			print("Could not find any line beginning with", LAST_REQUESTED_TIME_STARTS_WITH, " on request entry #", args[0])
			print("The first line of this request entry was:")
			print(args[1])
		case ErrorName.INVALID_ARGUMENTS_NO_NUMBER:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			print("The -n or --number argument needs to be a positive number, but the entered value was", args[0])
		case ErrorName.INVALID_ARGUMENTS_NEGATIVE_SKIP_POPULAR:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			print("The -s or --skip-popular argument needs to be a non-negative number, but the entered value was", args[0])
		case ErrorName.INVALID_ARGUMENTS_NEGATIVE_THRESHOLD:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			print("The -t or --request-threshold argument needs to be a non-negative number, but the entered value was", args[0])
		case ErrorName.INVALID_ARGUMENTS_TOO_BIG_NUMBER:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			print("The -n or --number argument specified is bigger than the total number of requests.")
			print("Total number of available requested icons is", args[0],"but the specified number of icons is", args[1])
		case ErrorName.INVALID_ARGUMENTS_TOO_BIG_SKIP_POPULAR:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			print("The -s or --skip-popular argument specified is bigger than the total number of requests.")
			print("Total number of available requested icons is", args[0], "but the specified number to skip is", args[1])
		case ErrorName.INVALID_ARGUMENTS_FILTER_RETURNS_NOTHING:
			print(DEFAULT_INVALID_ARGUMENTS_ERROR)
			if args[0] > 0:
				print("After", args[0], "most popular requests were skipped, there were no records left that have been requested at least", args[1], "times")
			else:
				print("There are no icons that have been requested at least", args[1], "times")
			print("Please lower your -s/--skip-popular and/or -t/--request-threshold argument(s)")
		case ErrorName.WARNING_FILTERED_POPULATION_TOO_SMALL:
			additional_text = "T"
			if args[2] > 0:
				additional_text = "After skipping the top " + str(args[2]) + " most popular request(s), t"
			print("Warning:", additional_text + "he number of icons that have been requested at least", args[3],"times is", args[0], "but we are trying to randomly select", args[1], "of them.")
			print("As such, the program will select", args[0], "icon requests instead of the specified", args[1])
	
	print("**************************************************************")		
	if(e_lvl == ErrorLevel.ERROR_LEVEL_CRITICAL):	
		print("A critical error was found. The program will exit.")
		print("**************************************************************")
		sys.exit()

def make_new_request_header(remaining_requests):
	DASH_LINE = "-------------------------------------------------------\n"
	
	new_request_header = []
	current_datetime = datetime.datetime.now()
	no_lead_zero_day = str(int(current_datetime.strftime("%d")))
	stats_line = str(int(remaining_requests)) + " Requested Apps Pending (Updated " + no_lead_zero_day + " " + current_datetime.strftime("%B %Y") + ")\n"
	
	new_request_header.append(DASH_LINE)
	new_request_header.append(stats_line)
	new_request_header.append(DASH_LINE)
	return new_request_header
		
def process_file(f, args):
	lines = f.readlines()	
	header_end_idx, line_count_per_entry = line_counter(lines)
	if (header_end_idx == -1):
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_HEADER_NOT_FOUND)
	if (line_count_per_entry == 0):
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_WHOLE_FILE_ENTRY_NOT_FOUND)
	
	del(lines[:header_end_idx])
	total_requests = len(lines) / line_count_per_entry
	
	if total_requests % 1 > 0:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.PARSE_TOTAL_REQUESTS_NOT_DIVISIBLE, len(lines), line_count_per_entry)
	if total_requests < args.number:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_TOO_BIG_NUMBER, int(total_requests), args.number)
	if total_requests < args.skip_popular:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_TOO_BIG_SKIP_POPULAR, int(total_requests), args.skip_popular)
	if args.verbose:
		print("- Total icon requests:", int(total_requests))
	combined_lines, included_lines_filter = compute_final_population(lines, line_count_per_entry, args)
	final_population_size = len(included_lines_filter)
	
	if final_population_size == 0:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.INVALID_ARGUMENTS_FILTER_RETURNS_NOTHING, args.skip_popular, args.request_threshold)
	if final_population_size < args.number:
		print_error_handling(ErrorLevel.ERROR_LEVEL_WARNING, ErrorName.WARNING_FILTERED_POPULATION_TOO_SMALL, final_population_size, args.number, args.skip_popular, args.request_threshold)
		sample_size = final_population_size
	else:
		sample_size = args.number
	
	remaining_requests = total_requests - sample_size
	final_lines = random.sample(included_lines_filter, k=sample_size)

	all_excluded_lines = [x for x in combined_lines if x not in set(final_lines)]

	return final_lines, all_excluded_lines,  make_new_request_header(remaining_requests)

if __name__ == "__main__":
	args = prepare_arguments()
	
	old_requests_loc = os.path.join(args.input_dir, DEFAULT_REQUESTS_FILE_NAME)
	new_requests_loc = os.path.join(args.output_dir, DEFAULT_NEW_REQ_FILE_NAME)
	random_requests_loc = os.path.join(args.output_dir, DEFAULT_RANDOMIZED_REQ_FILE_NAME)
	
	try:
		f = open(old_requests_loc, "r")
	except OSError:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_NOT_READABLE, requests_loc)
	output_list, new_request_text, new_request_header = process_file(f, args)

	f.close()
	output_text = "".join(output_list)
	output_new_request = "".join(str(x) for x in new_request_text)
	output_new_header = "".join(str(x) for x in new_request_header)

	try:
		f = open(random_requests_loc, "w")
	except OSError:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_NOT_WRITABLE, random_requests_loc)
	f.write(output_text)
	f.close()
	
	try:
		f = open(new_requests_loc, "w")
	except OSError:
		print_error_handling(ErrorLevel.ERROR_LEVEL_CRITICAL, ErrorName.FILE_NOT_WRITABLE, new_requests_loc)
	f.write(output_new_header)
	f.write(output_new_request)
	f.close()
	if args.verbose:
		print("Completed successfully.")
	sys.exit()
	
