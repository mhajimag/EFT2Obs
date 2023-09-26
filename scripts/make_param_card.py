import os
import sys
import tools
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--process', '-p', default='zh-HEL', help="Label of the process, must correspond to the dir name that was created in the MG dir")
parser.add_argument('--output', '-o', default='param_card.dat', help="Output name for the param_card.dat")
# parser.add_argument('--config', '-c', default='config.json')
args = parser.parse_args()


process = args.process

sys.path.append('%s/%s' % (os.environ['PWD'], os.environ['MG_DIR']))
sys.path.append(os.path.join(os.environ['MG_DIR'], process.split('/')[-1], 'bin', 'internal'))

import check_param_card as param_card_mod

# cfg = tools.GetConfigFile(args.config)

param_card_path = '%s/%s/Cards/param_card.dat' % (os.environ['MG_DIR'], process.split('/')[-1])
print '>> Parsing %s' % param_card_path
param_card = param_card_mod.ParamCard(param_card_path)


before = []
after = []

# for block in cfg['blocks']:
#     print(block)
#     ids = [X[0] for X in param_card[block].keys()]
#     print(ids)
ids = [X[0] for X in param_card['SMEFT'].keys()]

for i in ids:
    par = param_card['SMEFT'].param_dict[(i,)]
#     print(par)
    before.append(['SMEFT', i, par.comment.strip(), par.value])
#     print(before)
    if i == 2 or i == 9:
        par.value = 0.00001
    





for i in ids:
    par = param_card['SMEFT'].param_dict[(i,)]
    after.append(['SMEFT', i, par.comment.strip(), par.value])

print '>> The following active and inactive parameter changes will be applied:'
for b, a in zip(before, after):
    if a[3] != b[3]:
        print '    - Block %-30s: Parameter %-3i %-30s: %-10g --> %-10g' % (a[0], a[1], a[2], b[3], a[3])

print '>> Writing %s' % args.output
param_card.write(args.output)
