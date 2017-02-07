#Amity Space Allocater

#Introduction
Amity Space Allocater is console application that allocates spaces to fellows and staff within Andela

#Installation
Download the application
```
$ git clone  https://github.com/lederp23/amity.git
$ cd amity
```


Create and Start Virtual environment
```
$ virtualenv -p /usr/bin/python3 .env
cd amity/
$ source .env/bin/activate
```

<<<<<<< HEAD

Create and Start Virtual environment
```
$ virtualenv -p /usr/bin/python3 .env
$ gicd amity/
$ source .env/bin/activate
```

=======
>>>>>>> Changes README.md
Install dependencies 
```$ pip install -r requirements.txt```

#Run the application
`python amity.py -i`

#Usage
create_room `<room_name>` - Creates a room in amity and when a new room is created it autoallocates all the unallocated people

add_person `<name> <Fellow|staff> (y|n)` - Adds person to Amity and takes the job type argument and wants accomodation

reallocate_person `<name> <Fellow|staff>` - Reallocate a particular person to a particular room

load_people - Adds people form a txt file

print_allocations `[-o=filename]` - Prints a list of all rooms and its respective members

print_unallocated `[-o=filename]`  - Prints a list of people who do not have office or living spaces 

print_room `<room_name>` - Prints all members in a particular room

Save_state `[--db=database]` - Saves all changes to the default databases or the specified database 

Load_state `<database_name>` - loads contents of the specified database
#Credits
[Kenneth Kipyegon](https://github.com/kenneth254/)