import pexpect
import sqlite3
import sys
import os
import re
import time

msf_type = sys.argv[1]
base_path = sys.argv[2]
dry_run = sys.argv[3]
database = os.path.join(base_path, "database.db")

if "exploits" != msf_type and "auxiliary" != msf_type and "post" != msf_type:
    print("You need to specify exploits, auxiliary, or post")
    sys.exit(1)

if not os.path.exists(os.path.join(base_path, "database.db")):
    print("Database does not exist in " + base_path)
    sys.exit(1)


def clean_line(line):
    line = line.decode('utf-8')
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()


def insert_data(table_name, data_array, returning_id):
    try:
        keys = ','.join(data_array.keys())
        question_marks = ','.join(list('?' * len(data_array)))
        values = tuple(data_array.values())
        query = 'INSERT INTO ' + table_name + ' (' + keys + ') VALUES (' + question_marks + ') RETURNING ' + returning_id

        print(query)
        print(values)

        if (dry_run != "dry_run"):
            cursor.execute(query, values)

            row = cursor.fetchone()
            (inserted_id,) = row if row else None

            sqliteConnection.commit()
            return inserted_id

        return 2

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def update_descr(attack_id, payload_default):
    try:

        values = (payload_default, attack_id)
        query = "update attacks_attack set payload_default = ? where attack_id = ?"

        print(query)
        print(values)

        if (dry_run != "dry_run"):
            cursor.execute(query, values)
            sqliteConnection.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


filename = os.path.join(base_path, msf_type + "_search.txt")
json_filename = os.path.join(base_path, msf_type + "_json.txt")
info_filename = os.path.join(base_path, msf_type + "_info.txt")
data_filename = os.path.join(base_path, msf_type + "_data.txt")

child_options = pexpect.spawn('msfconsole')

child_options.expect(['msf6'])  # Wait for prompt
child_options.sendline('show ' + msf_type)
child_options.expect('msf6')  # Wait for prompt
lines = child_options.before.splitlines()
try:
    child_options.expect('msf6')  # Wait for prompt
    lines = child_options.before.splitlines()
except:
    pass
exploits = False
data = []
line_number = 0

child_options.sendline('show payloads')

# with open(filename, 'w') as file:
for line in lines:
    line = clean_line(line)
    if "show " + msf_type in line:
        exploits = True
    if exploits:
        line_number += 1
        if line_number >= 10:
            splits = line.split()
            if len(splits) > 6:
                row = {"rowid": int(splits[0]),
                       "name": splits[1],
                       "date": splits[2],
                       "rank": splits[3],
                       "check_supported": splits[4],
                       "desc": " ".join(splits[5:]),
                       "type": msf_type
                       }
                data.append(row)
            # file.write(line.decode('utf-8'))
            # file.write("\n")

# child_options.sendline('exit')
#
# child_options = pexpect.spawn('msfconsole')
child_options.setwinsize(400, 1200)


# child_options.expect(['msf6'])  # Wait for prompt

def payload_payload():
    child_options.expect('msf6.*')
    lines = child_options.before.splitlines()
    try:
        child_options.expect('msf6 *')
        lines = child_options.before.splitlines()
    except:
        pass

    print(lines)

    lines1 = lines[9:]
    payloads = []

    for line1 in lines1:
        line1 = clean_line(line1)
        splits = line1.split()
        if len(splits) >= 6:
            row = {"order_by": int(splits[0]),
                   "payload": splits[1],
                   "disclosure": splits[2],
                   "rank": splits[3],
                   "check_supported": splits[4],
                   "description": " ".join(splits[5:])
                   }
            payloads.append(row)
            # insert into datumbase
            payload_id = insert_data("attacks_payload", row, "payload_id")

            # okie dokie artichokie

            child_options.sendline('options ' + row['payload'])
            child_options.expect('msf6 *')
            options = child_options.before.splitlines()
            child_options.expect('msf6 *')
            options = child_options.before.splitlines()

            after_title = False
            section_line_count = 0
            section_count = 0
            section = {"attack_id": "", "title": ""}
            heading_start_pos = []
            options = options[2:]
            heading_line = ""
            payload_default = ""

            for option_line in options:
                option_line = clean_line(option_line)
                section_line_count += 1

                if 'View the full module info with the info, or info -d command.' in option_line:
                    break
                if option_line != "":
                    if section_line_count == 1:
                        if "**" in option_line.strip():
                            section_line_count = 0
                            var_name = option_line.split(':')[0].replace("**", "").strip()
                            var_value = option_line.split(':')[1].split()[0]
                            var_descr = " ".join(option_line.split(':')[1].split()[1:])

                            section_count += 1
                            option_heading_id = insert_data('attacks_option_heading',
                                                            {"attack_id": payload_id,
                                                             "title": "Extra Things",
                                                             "order_by": section_count,
                                                             "type": "payload"},
                                                            "option_heading_id")
                            insert_data("attacks_option",
                                        {"name": var_name,
                                         "current_setting": var_value,
                                         "description": var_descr},
                                        "option_id")

                            continue
                        section = {"attack_id": payload_id,
                                   'title': option_line}
                        headings_array = []
                        heading_line = ""
                        heading_start_pos = []
                        after_title = True
                        print(section)
                        heading_line = option_line.strip()
                        if heading_line.strip() != "Exploit target:":
                            section_count += 1
                            name = ""
                            if "(" in heading_line:
                                name = heading_line[heading_line.index('(') + 1:len(heading_line) - 2]
                            option_heading_id = insert_data('attacks_option_heading',
                                                            {"attack_id": payload_id,
                                                             "title": heading_line,
                                                             "name": name,
                                                             "order_by": section_count,
                                                             "type": "Payload"},
                                                            "option_heading_id")
                        else:
                            break

                    # headings
                    if section_line_count == 3:
                        heading_line = option_line

                    # dashes
                    if section_line_count == 4:
                        dashes = option_line
                        index = 0
                        for i in range(len(option_line.split())):
                            pos = find_nth(option_line, " -", i + 1) + 1
                            heading_start_pos.append(pos)

                        i = 0
                        for start_pos in heading_start_pos:
                            end_pos = len(heading_line)
                            if i + 1 < len(heading_start_pos):
                                end_pos = heading_start_pos[i + 1]
                            heading = heading_line[start_pos:end_pos].strip()
                            headings_array.append(heading.replace(" ", "_"))
                            i += 1

                    # options start here
                    if section_line_count > 4:
                        after_title = False
                        i = 0
                        section_options = {}
                        for start_pos in heading_start_pos:
                            end_pos = len(option_line)
                            if i + 1 < len(heading_start_pos):
                                end_pos = heading_start_pos[i + 1]
                            if "Description" in headings_array[i]:
                                section_options[headings_array[i]] = option_line[start_pos:end_pos]
                            else:
                                section_options[headings_array[i]] = option_line[start_pos:end_pos].strip()
                            i += 1

                        if section['title'] != "Exploit Target:":
                            section_options['option_heading_id'] = option_heading_id
                            section_options['order_by'] = section_line_count - 4
                            insert_data("attacks_option", section_options, "option_id")

                        # section["options"].append(section_options)
                        print(section_options)
                        # insert_data("attack_option",section_options)

                if not after_title and option_line.strip() == "":
                    section = {"attack_id": "", "title": ""}
                    section_line_count = 0
                    option_heading_id = 0
                    heading_line = ""


payload_payload()
