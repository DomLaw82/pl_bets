import datetime, re
from app.cli import cl_output

def validate(check_type: str, value: str, prompt: str, **kwargs) -> str:
    var_list = kwargs.get("var_list") or []
    length = kwargs.get("length")

    while True:
        if check_type == "yes_no":
            condition = value.upper() not in ("Y", "N")
            error_message = "ERROR: VALUE MUST BE 'Y' OR 'N'"
        elif check_type == "text":
            condition = value.isnumeric()
            error_message = "ERROR: VALUE MUST BE A TEXT"
        elif check_type == "int":
            condition = not value.isnumeric() or "." in value
            error_message = "ERROR: VALUE MUST BE AN INTEGER"
        elif check_type == "id":
            condition = not bool(re.match('((\w{1}|\w{2})-\d+)', value))
            error_message = "ERROR: MUST FOLLOW ID FORMAT IN TABLE"
        elif check_type == "float":
            condition = "." not in value or not value.split(".")[0].isnumeric() or not value.split(".")[1].isnumeric()
            error_message = f"ERROR: ENTRY MUST BE A FLOAT"
        elif check_type == "in_list":
            condition = value.upper() not in [val.upper() for val in var_list]
            error_message = "ERROR: ENTER EXISTING VALUE"
        elif check_type == "not_in_list":
            condition = value.upper() in [val.upper() for val in var_list]
            error_message = "ERROR: ENTER UNIQUE VALUE"
        elif check_type == "length":
            condition = len(value) != length
            error_message = f"ERROR: ENTRY MUST BE {length} CHARACTERS LONG"
        elif check_type == "season":
            condition = not bool(re.search("\d{2}\/\d{2}", value))
            error_message = f"ERROR: SEASON MUST BE IN FORM 'YY/YY'"
        else:
            condition = False
            error_message = "ERROR: UNKNOWN VALIDATION TYPE"

        if not condition:
            return value

        cl_output.delete_last_lines()
        out = input(error_message + '; PRESS ENTER TO CONTINUE...')
        cl_output.delete_last_lines()
        value = input(prompt)

def is_valid_date(date_string):
	try:
		datetime.datetime.strptime(date_string, '%Y-%m-%d')
		return True
	except ValueError:
		return False

def get_valid_date_input(value: str, prompt: str):
	while True:
		if is_valid_date(value):
			return value
		else:
			cl_output.delete_last_lines()
			out = input("ERROR: INVALID DATE FORMAT; ENTER TO CONTINUE...")
			cl_output.delete_last_lines()
			value = input(prompt)

