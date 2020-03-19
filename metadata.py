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


@metadata_processor
def add_apt_packages(metadata):
    # TODO: add support for other package managers as well
    if node.has_bundle("apt"):
        metadata.setdefault('apt', {})
        metadata['apt'].setdefault('packages', {})

        metadata['apt']['packages']['sudo'] = {'installed': True}

        if node.os == 'debian':
            if node.os_version[0] >= 10:
                metadata['apt']['packages']['libpam-ssh-agent-auth'] = {'installed': True}
            if node.os_version[0] == 9:
                metadata['apt']['packages']['libcrypto++6'] = {'installed': True}
            elif node.os_version[0] == 8:
                metadata['apt']['packages']['libcrypto++9'] = {'installed': True}

    return metadata, DONE
