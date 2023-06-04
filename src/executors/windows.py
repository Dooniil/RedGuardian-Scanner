import winrm
import re

def exec_command(target, login, password, definitions) -> list:
    session = winrm.Session(
        target,
        auth=(login, password),
        message_encryption='auto')

    result_list = list()

    for definition in definitions:
        result = dict(id=None, cpe=None, found=False, cpe_product=list())
        scripts = definition['scripts']
        result.update(id=definition['id'])

        condition_for_script = scripts[0]
        scripts = scripts[1:]

        for script in scripts:
            os_tests: dict = script.get('os_check')['tests']
            is_os_set = False

            for os_test in os_tests:
                for os_test_dict in os_test:
                    test_data = os_test_dict.get('test')
                    negate = test_data.get('negate') # если True, то реверснутый скрипт
                    objects_list = test_data.get('script')['object_cmd_list'] # список объектов для проверки
                    states_list = test_data.get('script')['state_cmd_list'] # список статусов для проверки

                    object_cmd = objects_list[0]
                    if not object_cmd:
                        continue

                    result_object_cmd = session.run_ps(object_cmd).std_out.decode('utf-8').strip()

                    for state_dict in states_list:
                        condition = state_dict.get('operator')
                        value = state_dict.get('value')
                        if condition == 'case insensitive equals' or condition == 'equals':
                            if value == result_object_cmd:
                                if negate:
                                    break
                                if 'windows' in os_test_dict.get('cpe') or 'alt' in os_test_dict.get('cpe'):
                                    cpe = os_test_dict.get('cpe')
                                else:
                                    result['cpe_product'].append(os_test_dict.get('cpe'))
                                is_os_set = True
                            else:
                                is_os_set = False
                                break
                        elif condition == 'less than':
                            if int(value) > int(result_object_cmd):
                                if negate:
                                    break
                                if 'windows' in os_test_dict.get('cpe') or 'alt' in os_test_dict.get('cpe'):
                                    cpe = os_test_dict.get('cpe')
                                else:
                                    result['cpe_product'].append(os_test_dict.get('cpe'))
                                is_os_set = True
                            else:
                                is_os_set = False
                                break
                        elif condition == 'greater than':
                            if int(value) < int(result_object_cmd):
                                if negate:
                                    break
                                if 'windows' in os_test_dict.get('cpe') or 'alt' in os_test_dict.get('cpe'):
                                    cpe = os_test_dict.get('cpe')
                                else:
                                    result['cpe_product'].append(os_test_dict.get('cpe'))
                                is_os_set = True
                            else:
                                is_os_set = False
                                break
                        elif condition == 'pattern match':   
                            if re.search(value, result_object_cmd):
                                if negate:
                                    break
                                if 'windows' in os_test_dict.get('cpe') or 'alt' in os_test_dict.get('cpe'):
                                    cpe = os_test_dict.get('cpe')
                                else:
                                    result['cpe_product'].append(os_test_dict.get('cpe'))
                                is_os_set = True
                            else:
                                is_os_set = False
                                break
                    else:
                        continue
                    break
                # else:
                #     continue
                # break

            if is_os_set:
                result['cpe'] = cpe
                
                vuln_test = script.get('vuln_check')['tests']
                vuln_obj_list = vuln_test[0].get('object_cmd_list')
                if len(vuln_obj_list) > 1:
                    tmp_result = session.run_ps(vuln_obj_list[0]).std_out.decode('utf-8').strip()
                    obj_cmd = vuln_obj_list[1][0] + ' "' + tmp_result + '\\' + vuln_obj_list[1][1] + '\\' + vuln_obj_list[1][2] + '\"' + vuln_obj_list[1][3]
                    result_obj_cmd = session.run_ps(obj_cmd).std_out.decode('utf-8').strip()
                    vuln_state_list = vuln_test[0].get('state_cmd_list')
                    
                    for state_dict in vuln_state_list:
                        condition = state_dict.get('operator')
                        value = state_dict.get('value')
                        if condition == 'case insensitive equals' or condition == 'equals':
                            if value == result_object_cmd:
                                result['found'] = True
                                break
                        elif condition == 'less than':
                            if '.' in value:
                                splitted_version_needed = value.split('.')
                                splitted_version_current = result_obj_cmd.split('.')
                                for i, v in enumerate(splitted_version_current):
                                    if int(v) < int(splitted_version_needed[i]):
                                        result['found'] = True
                                        break
                                    else: 
                                        result['found'] = False
                                        
                            elif int(value) > int(result_object_cmd):
                                result['found'] = True
                                break
                        elif condition == 'greater than':
                            if '.' in value:
                                splitted_version_current = value.split('.')
                                splitted_version_needed = value.split('.')
                                for i, v in enumerate(splitted_version_current):
                                    if int(v) > int(splitted_version_needed[i]):
                                        result['found'] = True
                                        break
                                    else: 
                                        result['found'] = False

                            if int(value) < int(result_object_cmd):
                                result['found'] = True
                                break
                        elif condition == 'pattern match':   
                            if re.search(value, result_object_cmd):
                                result['found'] = True
                                break
                    else: 
                        break
                    break
        result_list.append(result)
    return result_list
        