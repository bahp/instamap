import pickle
import math

# Configuration
PATH = 'pickle'
TAG = 'pi'
FILENAME = 'filename_%s.obj' % TAG

# Object
obj_to = math.pi

with open(FILENAME, 'wb') as f:
    pickle.dump(obj_to, f)

with open(FILENAME, 'rb') as f:
    obj_from = pickle.load(f)

# Show
print(obj_to)
print(obj_from)