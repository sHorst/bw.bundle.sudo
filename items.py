if node.os == "openbsd":
    root_group = "wheel"
else:
    root_group = "root"

pkg_apt = {
    "sudo": {},
}

directories = {
    "/etc/sudoers.d": {
        'mode': "0755",
        'owner': "root",
        'group': root_group,
    },
    "/etc/pam.d": {
        'mode': "0755",
        'owner': "root",
        'group': root_group,
    },
    '/lib/security': {
        'mode': "0755",
        'owner': "root",
        'group': root_group,
    }
}

files = {
    "/etc/sudoers": {
        'mode': "0440",
        'owner': "root",
        'group': root_group,
        'content_type': "mako",
        'source': "etc/sudoers",
        'verify_with': "visudo -cf {}",
        'context': {'add_lines': node.metadata.get('sudo', {}).get('add_lines', [])}
    },
}

"""Create sudo with ssh key"""
if node.os == 'debian':
    if node.os_version[0] == 8:
        files['/lib/security/pam_ssh_agent_auth.so'] = {
            'mode': '0755',
            'owner': 'root',
            'group': root_group,
            'content_type': "binary",
            'source': "lib/security/pam_ssh_agent_auth.so_deb_8",
            'needed_by': ['file:/etc/pam.d/sudo'],
        }
    elif node.os_version[0] == 9:
        files['/lib/security/pam_ssh_agent_auth.so'] = {
            'mode': '0755',
            'owner': 'root',
            'group': root_group,
            'content_type': "binary",
            'source': "lib/security/pam_ssh_agent_auth.so_deb_9",
            'needed_by': ['file:/etc/pam.d/sudo'],
        }
    files['/etc/pam.d/sudo'] = {
        'mode': '0644',
        'owner': 'root',
        'group': root_group,
        'content_type': "text",
        'source': "etc/pam.d/sudo",
    }

    if node.os_version[0] >= 9:
        pkg_apt['libcrypto++6'] = {'installed': True}
    elif node.os_version[0] == 8:
        pkg_apt['libcrypto++9'] = {'installed': True}


directories["/etc/sudoers.d/.authorized_keys"] = {
    'owner': 'root',
    'group': 'root',
    'mode': "0755",
}

groups = {
    'sudo': {}
}

for username, user_attrs in node.metadata.get('users', {}).items():
    if not user_attrs.get('delete', False):
        files["/etc/sudoers.d/.authorized_keys/{}".format(username)] = {
            'content': "\n".join(user_attrs['ssh_pubkeys']) + "\n",
            'owner': 'root',
            'group': 'root',
            'mode': "0644",
            'needed_by': ['file:/etc/pam.d/sudo'],
        }
