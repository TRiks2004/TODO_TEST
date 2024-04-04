async def get_path_file(name, name_ext) -> str:
    name_ext_split = name_ext.split(".", 1)

    if len(name_ext_split) == 2:
        return name + "." + name_ext_split[1]
    else:
        return name
