import re
import utils.attendance_parser as attendance_parser


def extract_roll_number(query):

    query = query.upper()

    match = re.search(
        r'238W1A[0-9A-Z]+',
        query
    )

    if match:

        roll_no = match.group().strip()

        print("\nEXTRACTED ROLL NO:", roll_no)

        return roll_no

    return None


def get_attendance(roll_no):

    roll_no = roll_no.strip().upper()

    print("\nSEARCHING FOR:", roll_no)

    print("\nAVAILABLE ATTENDANCE DATA:")
    print(attendance_parser.attendance_data)

    return attendance_parser.attendance_data.get(roll_no)