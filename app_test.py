import apps.app as backapp

backapp.run_command(1, 'echo hoge > test.txt'.split())
backapp.run_command(1, 'echo hoge'.split())

res = backapp.run_command(1, 'echo hoge > old/hoge/text.txt'.split()).stdout
if res is None:
    res = ''.encode('utf-8')
print(res.decode('utf-8'))