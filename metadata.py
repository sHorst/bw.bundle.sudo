defaults = {}

if node.has_bundle("apt"):
    defaults['apt'] = {
        'packages': {
            'sudo': {'installed': True},
        }
    }

    if node.os == 'debian':
        if node.os_version[0] >= 10:
            defaults['apt']['packages']['libpam-ssh-agent-auth'] = {'installed': True}
        if node.os_version[0] == 9:
            defaults['apt']['packages']['libcrypto++6'] = {'installed': True}
        elif node.os_version[0] == 8:
            defaults['apt']['packages']['libcrypto++9'] = {'installed': True}


@metadata_reactor
def add_sudo_group_processor(metadata):
    users = {}
    for username in metadata.get('users').keys():
        if metadata.get('users/{}/sudo'.format(username), False):
            add_groups = metadata.get('users/{}/add_groups'.format(username), [])

            if 'sudo' not in add_groups:
                add_groups.append('sudo')

            users[username] = {
                'add_groups': add_groups,
            }

    return {
        'users': users,
    }
