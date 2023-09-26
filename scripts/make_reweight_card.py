import json
import sys
import argparse
import numpy as np

parser = argparse.ArgumentParser()
# parser.add_argument('config', help="Input config file")
parser.add_argument('output', help="Output name for the reweight_card.dat")
#parser.add_argument('--prepend', nargs='*', default=None)
# parser.add_argument('step')
parser.add_argument('--prepend', nargs='*', default=None)


args = parser.parse_args()


def PrintBlock(val0, val1, index):
    res = []
    res.append('launch --rwgt_name=rw%i' % index)
    res.append('set SMEFT 2 %g' % (val0))
    res.append('set SMEFT 9 %g' % (val1))
    return res


# with open(args.config) as jsonfile:
#     cfg = json.load(jsonfile)

# pars = cfg['parameters']
# defs = cfg['parameter_defaults']

# for p in pars:
#     for k in defs:
#         if k not in p:
#             p[k] = defs[k]
# print pars
# print defs

output = ['change rwgt_dir rwgt']

if args.prepend is not None:
    output.extend(args.prepend)

initvals = [0.0]

res = []
res.append('launch --rwgt_name=SM' )
res.append('set SMEFT 2 0') 
res.append('set SMEFT 9 0') 


current_i = 0
output.extend(PrintBlock(0 , 0 ,current_i))
current_i += 1

# step = int(args.step)

cw=0
chwb=0

for cw in np.arange(-3, 3, 0.1875):
#         output.extend(PrintBlock(cw, chwb, current_i))
#         current_i += 1
    for chwb in np.arange(-10,10,0.625):
        output.extend(PrintBlock(cw, chwb, current_i))
        current_i += 1
            
            
# for i in xrange(len(pars)):
#     for j in xrange(i + 1, len(pars)):
#         # print i,j
#         vals = list(initvals)
#         vals[i] = pars[i]['val']
#         vals[j] = pars[j]['val']
#         output.extend(PrintBlock(pars, vals, current_i))
#         current_i += 1
#         print(vals)
# print(output)

with open(args.output, 'w') as outfile:
        outfile.write('\n'.join(output))

print '>> Created %s with %i reweighting points' % (args.output, current_i)
