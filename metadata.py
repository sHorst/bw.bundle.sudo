@metadata_processor
def add_sudo_group_processor(metadata):
    if 'users' in metadata:
        for username in metadata['users'].keys():
            if metadata['users'][username].get('sudo', False):
                add_groups = metadata['users'][username].get('add_groups', [])

                if 'sudo' not in add_groups:
                    add_groups.append('sudo')

                metadata['users'][username]['add_groups'] = add_groups

        return metadata, DONE

    return metadata, RUN_ME_AGAIN
