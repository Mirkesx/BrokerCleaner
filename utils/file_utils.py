def get_container_names_from_compose_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    # return only the lines that contains "container_name", clean the result of any space or \n
    return [x.split("container_name:")[-1].strip() for x in data if "container_name" in x]