utensils = {"fork", "spoon", "knife", "knife"}
dishes = {"bowl", "plate", "cup", "knife"}

#utensils.add("napkin")
#utensils.remove("fork")
#utensils.clear()

#utensils.update(dishes)

#mixes two sets together
#dinner_table = utensils.union(dishes)

print(utensils.difference(dishes))
print(utensils.intersection(dishes))

#for x in dinner_table:
#    print(x)