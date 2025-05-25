import pexpect
import sqlite3
import sys
import os
import re
import time

msf_type  = sys.argv[1]
base_path = sys.argv[2]
dry_run   = sys.argv[3]
database  = os.path.join(base_path, "database.db")

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

sqliteConnection.commit()


def insert_data(table_name, data_array, returning_id):
    try:
        keys = ','.join(data_array.keys())
        question_marks = ','.join(list('?' * len(data_array)))
        values = tuple(data_array.values())
        query = 'INSERT INTO ' + table_name + ' (' + keys + ') VALUES (' + question_marks + ') RETURNING '+returning_id

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
        raise Exception("Database error")


def insert_with_payload_key_key(attack_id, payload_name):
    try:
        query = """
            insert into attacks_attack_payload  
                select distinct ? as attack_d, payload_id 
                from attacks_payload 
                where payload = ?  """
        values = (attack_id, payload_name)

        print(query)
        print(values)

        if (dry_run != "dry_run"):
            cursor.execute(query, values)

            sqliteConnection.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise Exception("Database error")

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


def get_table_counts():
    try:

        values = (payload_default, attack_id)
        query1 = "select count(*) as count from attacks_attack;"
        query2 = "select count(*) as count from attacks_attack_payload;"
        query3 = "select count(*) as count from attacks_payload;"

        if (dry_run != "dry_run"):
            cursor.execute(query1)
            row1 = cursor.fetchone()
            (count,) = row1 if row1 else None
            print (str(count) + "  " + query1)

            cursor.execute(query2)
            row2 = cursor.fetchone()
            (count,) = row2 if row2 else None
            print (str(count) + "  " + query2)

            cursor.execute(query3)
            row3 = cursor.fetchone()
            (count,) = row3 if row3 else None
            print (str(count) + "  " + query3)

            sqliteConnection.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_payload_id(payload):
    try:
        values = (payload,)
        query = "select payload_id from attacks_payload where payload = ? order by payload_id limit 1"

        if (dry_run != "dry_run"):
            cursor.execute(query, values)
            row = cursor.fetchone()
            (paylaod_id,) = row if row else None

            sqliteConnection.commit()

            return paylaod_id

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def find_nth(haystack: str, needle: str, n: int) -> int:
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start

filename = os.path.join(base_path, msf_type + "_search.txt")
json_filename =os.path.join(base_path, msf_type + "_json.txt")
info_filename = os.path.join(base_path, msf_type + "_info.txt")
data_filename = os.path.join(base_path, msf_type + "_data.txt")

child_options = pexpect.spawn('msfconsole')

child_options.expect(['msf6'])  # Wait for prompt
child_options.sendline('show ' + msf_type)
child_options.expect('msf6')  # Wait for prompt
lines = child_options.before.splitlines()
child_options.expect('msf6')  # Wait for prompt
lines = child_options.before.splitlines()
exploits = False
data = []
line_number = 0


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
#child_options = pexpect.spawn('msfconsole')
child_options.setwinsize(400, 1200)
#child_options.expect(['msf6'])  # Wait for prompt


def options_n_stuff(module, attack_id):
    child_options.sendline('options ' + module)

    lines = child_options.after.splitlines()
    while 'options ' + module not in clean_line(lines[0]):
        child_options.expect('msf6')
        lines = child_options.before.splitlines()

    print(lines)

    after_title = False
    section_line_count = 0
    section_count = 0
    section = { "attack_id": "", "title": "" }
    heading_start_pos = []
    lines = lines[2:]
    heading_line = ""
    payload_default = ""

    for line in lines:
        line = clean_line(line)
        section_line_count += 1

        if 'View the full module info with the info, or info -d command.' in line:
            break
        if line != "":
            if section_line_count == 1:
                if "**" in line.strip():
                    section_line_count = 0
                    var_name = line.split(':')[0].replace("**","").strip()
                    var_value = line.split(':')[1].split()[0]
                    var_descr = " ".join(line.split(':')[1].split()[1:])

                    section_count += 1
                    option_heading_id = insert_data('attacks_option_heading',
                                                    { "attack_id": attack_id,
                                                                "title": "Extra Things",
                                                                "order_by": section_count,
                                                                "type": "other"},
                                                    "option_heading_id")
                    insert_data("attacks_option",
                                { "name": var_name,
                                            "current_setting": var_value,
                                            "description": var_descr,
                                            "option_heading_id": option_heading_id},
                                "option_id")

                    continue
                section = {"attack_id": attack_id, 'title': line }
                headings_array = []
                heading_start_pos = []
                after_title = True
                print(section)
                heading_line = line.strip() 
                if heading_line.strip() != "Exploit target:":
                    section_count += 1
                    type = "Other"
                    if "Module" in line: type = "Module"
                    elif "Payload" in line: type = "Payload_from"

                    name = "heading_line"
                    if "(" in heading_line:
                        name = heading_line[heading_line.index('(')+1:len(heading_line)-2]

                    option_heading_id = insert_data('attacks_option_heading',
                                                    { "attack_id": attack_id,
                                                                "title": heading_line,
                                                                "name": name,
                                                                "order_by": section_count,
                                                                "type":type},
                                                    "option_heading_id")
                else: break

                if "Payload options" in line:
                    payload_default = "payload/" + line[line.index('(') + 1:len(line) - 2]


            # headings
            if section_line_count == 3:
                heading_line = line

            # dashes
            if section_line_count == 4:
                for i in range(len(line.split())):
                    pos = find_nth(line, " -", i + 1) + 1
                    heading_start_pos.append(pos)

                i = 0
                for start_pos in heading_start_pos:
                    end_pos = len(heading_line)
                    if i + 1 < len(heading_start_pos):
                        end_pos = heading_start_pos[i + 1]
                    heading = heading_line[start_pos:end_pos].strip()
                    headings_array.append(heading.replace(" ","_"))
                    i += 1


            # options start here
            if section_line_count > 4:
                after_title = False
                i = 0
                section_options = {}
                for start_pos in heading_start_pos:
                    end_pos = len(line)
                    if i + 1 < len(heading_start_pos):
                        end_pos = heading_start_pos[i + 1]
                    if "Description" in headings_array[i]:
                        section_options[headings_array[i]] = line[start_pos:end_pos]
                    else:
                        section_options[headings_array[i]] = line[start_pos:end_pos].strip()
                    i += 1

                if section['title'] != "Exploit Target:":
                    section_options['option_heading_id'] = option_heading_id
                    section_options['order_by'] = section_line_count - 4
                    insert_data("attacks_option", section_options, "option_id")

                #section["options"].append(section_options)
                print(section_options)
                #insert_data("attack_option",section_options)

        if not after_title and line.strip() == "":
            section = { "attack_id": "", "title": "" }
            section_line_count = 0
            option_heading_id = 0
            heading_line = ""
    return payload_default




def payloads_n_stuff(module, attack_id):
    lines = []


    child_options.sendline('use ' + name)
    lines = child_options.after.splitlines()
    while 'msf6' not in clean_line(lines[0]):
        child_options.expect('msf6 *')
        lines = child_options.before.splitlines()

    child_options.sendline('show payloads')
    lines = child_options.after.splitlines()
    while 'show payloads' not in clean_line(lines[0]):
        child_options.expect('msf6 *')
        lines = child_options.before.splitlines()

    for line in lines:
        print (line)

    lines = lines[8:]

    for line in lines:
        line = clean_line(line)
        splits = line.split()
        if len(splits) >= 6 and splits[0][0] != '-':
            payload_id = get_payload_id(str(splits[1]))
            row = {"order_by": int(splits[0]),
                   "payload": splits[1],
                   "disclosure": splits[2],
                   "rank": splits[3],
                   "check_supported": splits[4],
                   "description": " ".join(splits[5:]),
                   "attack_id": attack_id,
                   "payload_id": payload_id
                   }
            insert_data('attacks_attack_payload', row, "attack_payload_id")


#data = [{"name": "exploit/aix/local/ibstat_path"}]
if data:

    with open(info_filename, 'w') as file:

        file.write("\n")


    child = pexpect.spawn('msfconsole')
    child.setwinsize(400, 1200)
    child.expect(['msf6'])
    lines = child.before.splitlines()

    for row in data[]:
        name = row['name']
        #collection_attacks.insert_one(row)
        #row_number = insert_data("attacks_attack", row)


        child.sendline('info ' + name)
        while 'info ' + name not in clean_line(lines[0]):
            child.expect('msf6 *')
            lines = child.before.splitlines()

        write_to_file = False

        rowcount = 0

        targets_found = False
        targets_count = 0

        options_found = False
        options_count = 0

        descr = {}
        headings = [" Name:", " Module:", " Platform: ", " Arch:", " Privileged:",
                    " License:", " Rank:", " Disclosed:"]
        headings_below = ["Provided by:", "Module side effects:", "Module stability:",
                          "Module reliability:", "Check supported:", "Payload information:",
                          "Description:", "References:"]
        head_below = False
        lines_below = []
        heading = ""
        references = True

        with open(info_filename, 'a') as file:

            file.write("==========================================================\n")
            file.write(name + "\n")
            file.write("==========================================================\n\n")

            options_array = [];
            targets_array = [];
            for line in lines:
                line = clean_line(line)

                if any(x in line for x in headings):
                    head = line.split(':')[0].strip().replace(" ", "_")
                    descr[head] = line.split(':')[1].strip()
                    write_to_file = True

                if "View the full module info with the" in line:
                    write_to_file = False

                options_count += 1
                if "Basic options:" in line:
                    options_found = True
                    options_count = 0

                if options_found:
                    if options_count == 0:
                        headings_array = []
                        heading_line = ""
                        heading_start_pos = []

                    # headings
                    if options_count == 1:
                        heading_line = line
                    # dashes
                    if options_count == 2:
                        dashes = line
                        index = 0
                        for i in range(len(line.split())):
                            pos = find_nth(line, " -", i + 1) + 1
                            heading_start_pos.append(pos)

                        i = 0
                        for start_pos in heading_start_pos:
                            end_pos = len(heading_line)
                            if i + 1 < len(heading_start_pos):
                                end_pos = heading_start_pos[i + 1]
                            heading = heading_line[start_pos:end_pos].strip()
                            headings_array.append(heading)
                            i += 1

                    # options start here
                    if options_count > 2 and line != "":
                        i = 0
                        section_options = {}
                        for start_pos in heading_start_pos:
                            end_pos = len(line)
                            if i + 1 < len(heading_start_pos):
                                end_pos = heading_start_pos[i + 1]
                            head = headings_array[i].replace(" ", "_")
                            if "Description" in head:
                                section_options[head] = line[start_pos:end_pos]
                            else:
                                section_options[head] = line[start_pos:end_pos].strip()
                            i += 1

                        section_options['order_by'] = options_count - 2
                        options_array.append(section_options)
                        # insert_data("attacks_options", section_options)
                        # print(section_options)

                    elif line == "":
                        options_found = False


                targets_count += 1
                if "Available targets:" in line:
                    targets_found = True
                    targets_count = 0
                if targets_found:
                    if targets_count > 2 and line != "":
                        target_dict = {
                            "order_by": targets_count - 2,
                            "default_setting": "",
                            "id": "",
                            "name": "",
                        }
                        target_dict["default_setting"] = line[0:4].strip()
                        target_dict["id"] = line[4:10].strip()
                        target_dict["name"] = line[10:]
                        # print(target_dict)
                        # collection_targets.insert_one(target_dict)
                        #insert_data("attacks_target", target_dict, "target_id")
                        targets_array.append(target_dict)

                    elif line == "":
                        targets_found = False

                if head_below == True and line != "":
                    lines_below.append(line.strip())

                if not head_below and any(x in line for x in headings_below):
                    heading = line[:-1].strip().replace(" ", "_")

                    head_below = True

                if line == "":
                    if head_below:
                        # descr.append( { heading : lines_below })
                        descr[heading] = "\n".join(lines_below)
                        head_below = False
                        lines_below = []

                if heading == "References" and line == "" and references:
                    descr['type'] = msf_type
                    references = False
                    print("\n\n\n")
                    print(descr)
                    # collection_details.insert_one(descr)
                    descr["Refs"] = descr["References"]
                    del descr["References"]
                    attack_id = insert_data("attacks_attack", descr, "attack_id")
                    # for opt in options_array:
                    #     opt['attack_id'] = attack_id
                    #     insert_data("attacks_option", opt, "target_id")
                    for tar in targets_array:
                        tar['attack_id'] = attack_id
                        insert_data("attacks_target", tar, "target_id")
                        
                    payloads_n_stuff(descr['Module'], attack_id)
                    print("____________________________________________________")
                    
                    payload_default = options_n_stuff(descr['Module'], attack_id)
                    if payload_default != "": update_descr(attack_id, payload_default)

                    get_table_counts()

                if write_to_file:
                    file.write(line)
                    file.write("\n")
                    # print(line)



