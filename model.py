from typing import List, Generator, Any

import ijson


def _parse_json_file(file_path: str) -> Generator[Any, Any, Any]:
    with open(file_path, 'r') as f:
        parser = ijson.parse(f)
        for prefix, event, value in parser:
            yield prefix, event, value


def validate_json_file_logic(file_path: str) -> bool:
    if count_fw_rules(file_path) and not count_vms(file_path):
        return False
    # some other validations might be added here

    return True


def validate_json_file_structure(file_path: str) -> bool:
    prefix_string_dict = {
        'vms': ('vm_id', 'name', 'tags'),
        'fw_rules': ('fw_id', 'source_tag', 'dest_tag')
    }

    stack = []
    key = ''
    values = []

    for prefix, event, value in _parse_json_file(file_path):
        if (prefix, event, value) == ('', 'start_map', None) and stack:
            return False

        elif (prefix, event) == ('', 'map_key'):
            if (stack[-1] != ('', 'start_map', None) and stack[-1] != ('', 'map_key', 'vms')) or value not in prefix_string_dict.keys():
                return False
            else:
                key = value
                values = prefix_string_dict[key]
                if stack[-1] == ('', 'map_key', 'vms'):
                    stack.pop()
                stack.append((prefix, event, value))
                continue

        elif (prefix, event, value) == ('', 'end_map', None):
            if stack[-1] in (('', 'map_key', 'fw_rules'), ('', 'map_key', 'vms')):
                stack.pop()
            if stack[-1] != ('', 'start_map', None):
                return False
            else:
                stack.pop()
                continue

        elif (prefix, event) == (key, 'start_array') and stack[-1] != ('', 'map_key', prefix):
            return False
        elif (prefix, event, value) == (key, 'end_array', None):
            if stack[-1] != (key, 'start_array', None):
                return False
            else:
                stack.pop()
                continue
        elif (prefix, event, value) == (f'{key}.item', 'end_map', None):
            if stack[-1] != (f'{key}.item', 'start_map', None):
                return False
            else:
                stack.pop()
                continue

        elif (prefix, event) == (f'{key}.item', 'start_map') and stack[-1] != (f'{key}', 'start_array', None):
            return False
        elif (prefix, event) == (f'{key}.item', 'map_key') and stack[-1] != (f'{key}.item', 'start_map', None):
            return False
        elif any([(prefix, event) == (f'{key}.item.{prefix_value}', 'string') and stack[-1] == (f'{key}.item', 'map_key', f'{prefix_value}') for prefix_value in values]):
            stack.pop()
            continue
        elif (prefix, event, value) == ('vms.item.tags', 'start_array', None) and stack[-1] != ('vms.item', 'map_key', 'tags'):
            return False
        elif (prefix, event) in [('vms.item.tags.item', 'string'), ('vms.item.tags', 'end_array')]:
            if (stack[-1][0], stack[-1][1]) not in [('vms.item.tags.item', 'string'), ('vms.item.tags', 'start_array')]:
                return False
            if event == 'end_array':
                while stack.pop() != ('vms.item', 'map_key', 'tags'):
                    continue
            continue

        stack.append((prefix, event, value))

    return False if stack else True


def _get_target_tags(file_path: str, vm_id: str) -> List[str]:
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


def _get_source_tags(file_path: str, vm_id: str) -> List[str]:
    vm_tags = _get_target_tags(file_path, vm_id)
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


def get_source_vms(file_path: str, vm_id: str) -> List[str]:
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


def count_vms(file_path: str) -> int:
    return _count_objects_in_array(file_path, 'vms', 'vm_id')


def count_fw_rules(file_path: str) -> int:
    return _count_objects_in_array(file_path, 'fw_rules', 'fw_id')


def _count_objects_in_array(file_path: str, object_prefix: str, key: str) -> int:
    objects = 0

    for prefix, event, value in _parse_json_file(file_path):
        if prefix == object_prefix and event == 'end_array':
            break
        elif prefix == f'{object_prefix}.item.{key}':
            objects += 1

    return objects


def vm_exists(file_path: str, vm_id: str) -> bool:
    for prefix, event, value in _parse_json_file(file_path):
        if prefix == 'vms' and event == 'end_array':
            return False
        elif prefix == 'vms.item.vm_id' and value == vm_id:
            return True


