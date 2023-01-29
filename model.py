import ijson


def _parse_json_file(file_path):
    with open(file_path, 'r') as f:
        parser = ijson.parse(f)
        for prefix, event, value in parser:
            yield prefix, event, value


def _get_target_tags(file_path, vm_id):
    vm_found = False
    tags_found = False
    tags = []

    for prefix, event, value in _parse_json_file(file_path):
        if prefix == 'vms.item' and event == 'start_map' and vm_found:
            break
        if prefix == 'vms.item.vm_id' and value == vm_id and not vm_found:
            vm_found = True
        elif vm_found and prefix == 'vms.item.tags':
            tags_found = True
        elif vm_found and tags_found and prefix == 'vms.item.tags.item':
            tags.append(value)

    return tags


def _get_source_tags(file_path, vm_id):
    vm_tags = _get_target_tags(file_path, vm_id)
    print(f'{vm_tags=}')
    source_tags = []
    source_tag = ''

    for prefix, event, value in _parse_json_file(file_path):
        if prefix == 'fw_rules.item.source_tag':
            source_tag = value
        elif prefix == 'fw_rules.item.dest_tag':
            if value in vm_tags:
                source_tags.append(source_tag)
            source_tag = ''

    return source_tags


def get_source_vms(file_path, vm_id):
    source_tags = _get_source_tags(file_path, vm_id)
    vms = []

    for prefix, event, value in _parse_json_file(file_path):
        if prefix == 'vms' and event == 'end_array':
            break
        elif prefix == 'vms.item.vm_id':
            current_vm_name = value
            current_vm_added = False
        elif prefix == 'vms.item.tags.item' and value in source_tags:
            if not current_vm_added:
                vms.append(current_vm_name)
                current_vm_added = True
    return vms


def count_vms(file_path):
    vms = 0

    for prefix, event, value in _parse_json_file(file_path):
        if prefix == 'vms' and event == 'end_array':
            break
        elif prefix == 'vms.item.vm_id':
            vms += 1

    return vms

