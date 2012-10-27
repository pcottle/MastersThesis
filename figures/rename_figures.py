#!/usr/bin/python
import os, commands

figure_dirs = []

for dirpath, dirnames, filenames in os.walk('./'):
  figure_dirs = dirnames
  break

for figure_dir in figure_dirs:
  print 'entering figure directory "', figure_dir, '"'
  files = os.listdir(figure_dir)
  for file in files:
    if file == '.DS_Store':
      files.remove(file)

  if not files:
    print 'This directory ', figure_dir, ' does not contain a figure!'
    continue

  files.sort(key=lambda x: os.stat(os.path.join(figure_dir, x)).st_mtime)
  files.reverse()

  print 'found files ', files
  if files[0] == 'figure.png':
    print 'This directory checks out!'
    command = 'git add {0}'.format(os.path.join(figure_dir, files[0]))
    status, output = commands.getstatusoutput(command)
    continue

  # we need to move or convert last file
  most_recent = files[0]
  print 'most recent file', most_recent

  if most_recent[-3] == 'png':
    # just move
    print 'moving, not converting'
    os.rename(os.path.join(figure_dir, most_recent), os.path.join(figure_dir, 'figure.png'))
    continue

  # have to convert. want a command like sips -s format png another.jpg --out figure.png
  source_image = os.path.join(figure_dir, most_recent)
  source_image = source_image.replace(' ', '\ ')
  dest_image = os.path.join(figure_dir, 'figure.png')
  # convert
  command = 'sips -s format png {0} --out {1}'.format(source_image, dest_image)
  status, output = commands.getstatusoutput(command)
  if status:
    print 'command was', command
    print 'ERROR!!!', output
  else:
    print 'completed: ', output, ':DDD'

  # resize
  command = 'sips -Z 400 {0}'.format(dest_image)
  status, output = commands.getstatusoutput(command)

  # remove original
  command = 'rm {0}'.format(source_image)
  status, output = commands.getstatusoutput(command)

  # git add
  command = 'git add {0}'.format(dest_image)
  status, output = commands.getstatusoutput(command)

  # open dir
  command = 'open {0}'.format(figure_dir)
  status, output = commands.getstatusoutput(command)

print 'Done!'
