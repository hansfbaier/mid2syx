#!/usr/bin/env python
import smf
import argparse

parser = argparse.ArgumentParser(description='Extracts all sysex events from midi file (.mid) and appends them to a sysex dump file (.syx)')
parser.add_argument('inputfile', metavar='inputfile.mid', nargs='?',
                    help='input midi file name')
parser.add_argument('--blofeld', action='store_true',
                    help='ignore all sysex except waldorf blofeld patches')
parser.add_argument('--verbose', action='store_true',
                    help='verbose output')


args = parser.parse_args()

midfile = args.inputfile
syxfile = midfile.split('.')[0] + ".syx"

print("opening input file '%s'..." % midfile)
f = smf.SMF(midfile)
t = f.tracks[0]

print("opening output file '%s'" % syxfile)
outfile = open(syxfile, 'wb')

patchno = 0

for e in t.events:
    if e.midi_buffer[0] == 0xf0:
        patchno +=1
        buflen = len(e.midi_buffer)
        bufhex = map(hex, e.midi_buffer)

        if args.blofeld:
            if  buflen != 392:
                print("************ Sysex event number %d with size %d != 392, not a patch, skipping" % (patchno, buflen))
                print(bufhex)
                continue

        if args.verbose:
            print('Patch number %d - Writing %d bytes:' % (patchno, buflen))
            print(bufhex)
            print(100 * '=')
        outfile.write(bytearray(e.midi_buffer))

outfile.close()
print("done with %d patches" % patchno)
