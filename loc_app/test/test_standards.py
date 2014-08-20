import loc.standard

standards = loc.standard.read_standards_directory(['datatables','standards'])

my_cas_list=['7429-90-5','123-22-2','126-90-5','7664-41-7','92-52-4']    

standards['tesl'].prefetch(my_cas_list)
standards['ncstds'].prefetch(my_cas_list)
print standards['lastds'].lookup('92-52-4')
print standards['ncstds'].lookup('7664-41-7')

pass


