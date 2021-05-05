test = {'ciao': {}}

test1 = {'ciao1': {}}


if 'ciao1' not in test:
    test['ciao1'] = 'asd'

if 'ciao' not in test1:
    test1['ciao'] = 'asd'


print(test,test1)