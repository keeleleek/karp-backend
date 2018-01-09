import sys
import src.offline.create_metadata as metadata
import src.offline.upload_offline as upload

# TODO move stuff from upload_offline here, leave the real code there

if sys.argv[1] == '--create_metadata':
    outpath = 'config/fieldmappings.json'
    metadata.print_all(outpath)

if sys.argv[1] == '--create_mode':
   mode = sys.argv[2]
   suffix = sys.argv[3]
   upload.create_mode(mode, suffix)
   print 'Upload successful'

if sys.argv[1] == '--publish_group':
   group = sys.argv[2]
   suffix = sys.argv[3]
   upload.publish_group(group, suffix)
   print 'Upload successful'

