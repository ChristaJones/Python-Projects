import hashlib

#create hash for password
p =  "bubbles"

s = hashlib.sha1(p.encode('UTF-8')).hexdigest()

s1 = hashlib.sha1(b"password").hexdigest()


print (s)

print(s1)
