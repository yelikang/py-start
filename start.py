
import re

pattern = re.escape('')

full_path = re.sub(pattern, '456', '123', count=1)

print(full_path)