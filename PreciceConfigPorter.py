import os

def port_v2_to_v3(logger, input_file, output_file="./_generated/config/precice-config-v3.xml"):
    try:
        with open(input_file, 'r') as f:
            lines = f.readlines()
        new_lines = []
        solver_interface_attributes = []
        for line in lines:
            #new_line = port_v2_to_v3_replace('solver-interface', 'participant', line, logger)

            new_line = line
            #remove solver-interface line and save attributes
            if "<solver-interface" in line:
                solver_interface_attributes = get_attributes(line)
                logger.info(f"Found solver-interface with attributes {solver_interface_attributes}")
                new_line = ""
            
            #Participants
            #new_line = port_v2_to_v3_replace('use-mesh provide="true"', 'provide-mesh', line, logger)
            new_line = port_v2_to_v3_replace_attribute('use-mesh', 'provide="true"', 'provide-mesh', line, logger)
            new_line = port_v2_to_v3_replace_attribute('use-mesh', 'provide="false"', 'receive-mesh', line, logger)

            #####
            new_lines.append(new_line)
        if not(os.path.isfile(output_file)):
            with open(output_file,'w') as f:
                f.write("")
            logger.info(f"Creating output file at default path because it does not exist: ./_generated/config/precice-config-v3.xml")
        with open(output_file, 'w') as f:
            f.writelines(new_lines)

        logger.info(f"Converted preCICE config from v2 to v3: {output_file}")

    except FileNotFoundError:
        logger.error(f"Input Precice v2 file {input_file} not found.")
    except Exception as e:
        logger.error(f"Error converting preCICE config: {str(e)}")



def port_v2_to_v3_replace(input_string:str,output_string:str,line,logger):
    if input_string in line:
        logger.info(f"Replaced {input_string} with {output_string}")
        logger.info(f"attributes {get_attributes(line)}")
        return line.replace(input_string, output_string)
    else:
        return line

def port_v2_to_v3_replace_attribute(input_string:str,attribute:str,output_string:str,line,logger):
    if input_string in line:
        logger.info(f"Replaced {input_string} with {output_string}")
        attributes = get_attributes(line)
        logger.info(f"attributes {attributes[attribute]}")
        logger.info(f"attributes {attributes}")
        return line.replace(input_string, output_string)
    else:
        return line


def get_attributes(line):
    attributes = {}
    temp = line.split(' ')
    for attribute in temp:
        if '=' in attribute:
            key, value = attribute.strip().split('=')
            key = key.strip()
            value = value.strip().strip('">')
            attributes[key] = value
    return attributes


