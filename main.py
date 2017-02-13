"""
Welcome to Amity Rooms allocation System.
Usage:
    amity add_person <first_name> <last_name> <role> [(y|n)]
    amity reallocate_person <first_name> <last_name> <room_name>
    amity save_state [--db=sqlite_database]
    amity load_state <database>
    amity print_allocations [--o=filename]
    amity print_unallocated [--o=filename]
    amity load_people
    amity print_room <room_name>
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import sys
import os
import time
import cmd
from docopt import docopt, DocoptExit
from termcolor import colored, cprint
from pyfiglet import Figlet
from app.amity import Amity

AMITY = Amity()
AMITY.load_state("amity")


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)
        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.
            print('\n')
            print('Invalid Command! Use the below syntax:')
            print(e)
            print('\n')
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

def delay_print(stuff):
    """Delays printing"""
    for string in stuff:
        sys.stdout.write('%s' %string)
        sys.stdout.flush()
        time.sleep(0.001)

# This class ties all the docopt calling functions
class ScreenOut(cmd.Cmd):
    """main class"""

     # The below statements print a menu to act as a directive to the user
    os.system('clear')
    fig = Figlet(font='roman')
    print(colored(fig.renderText('Amity'),\
         'magenta', attrs=['bold']))
    intro = colored('-- Version 1.0 --\t\t Enter "q" to quit', 'cyan', attrs=['bold'])

    # The prompt that shows the user that he or she is running form the application in the cmd
    prompt = "Amity >>"


    #This cmd allows the user to parse arguments for calling the add_person function
    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> <role> [(y|n)]"""

        first_name = args['<first_name>']
        last_name = args['<last_name>']
        name = first_name + "_" + last_name
        role = args['<role>']

        # checks accomodation status
        if args['y'] and args['<role>'].lower() == "fellow":
            accomodation = "Y"
            cprint(AMITY.add_person(name, role, accomodation), "green", attrs=['bold'])
        elif args['y'] and args['<role>'] == "staff":
            cprint("✘ staff cannot be allocated accomodations", "red", attrs=["bold"])
        else:
            accomodation = "N"
            cprint(AMITY.add_person(name, role, accomodation), "green", attrs=['bold'])

    # This cmd allows the user to parse arguments for calling create_room function
    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <room_name>..."""

        # while loop to iterate over rooms created
        index = 0
        while index < len(args['<room_name>']):
            cprint("Enter the room type for " +
                   str(args['<room_name>'][index]) + "\n 1. for office\
                    \n 2. for living_space\n q. q Exit ",
                   "magenta", attrs=["bold"])
            room_type = input()
            if room_type == "1":
                room_type = "office"
                cprint(AMITY.create_room(args['<room_name>'][index], room_type),
                       "green", attrs=["bold"])
                index += 1
            elif room_type == "2":
                room_type = "living_space"
                cprint(AMITY.create_room(args['<room_name>'][index], room_type),
                       "green", attrs=["bold"])
                index += 1
            elif room_type == "q":
                index = len(args['<room_name>'])
            else:
                cprint("Enter the correct choice for " + args['<room_name>'][index], "red")

    # This cmd allows the user to parse arguments for calling the reallocate_person function
    @docopt_cmd
    def do_reallocate_person(self, args):
        """Usage: reallocate_person <first_name> <last_name> <new_room_name>"""

        first_name = args['<first_name>']
        last_name = args['<last_name>']
        name = first_name + "_" + last_name
        print(AMITY.reallocate(name, args['<new_room_name>'].lower()))

    # This cmd allows the user to call the save_state function
    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""

        if args['--db'] is None:
            print(AMITY.save_state())
        else:
            db_name = args['--db']
            print(AMITY.save_state(db_name))

    # This cmd allows the user the load_state function
    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <database>"""

        print(AMITY.load_state(args['<database>']))

    # This cmd allows the user to call the print_allocations function
    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=filename]"""

        # checks save to file
        if args['--o'] is None:
            filename = None
            cprint(AMITY.print_allocations(), "magenta", attrs=["bold"])
        else:
            filename = args['--o']
            cprint(AMITY.print_allocations(filename), "green", attrs=["bold"])

    # This cmd allows the user to call the print_unallocated function
    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=filename]"""

        # checks save to file
        if args['--o'] is None:
            filename = None
            cprint(AMITY.print_unallocated(), "magenta", attrs=["bold"])
        else:
            filename = args['--o']
            cprint(AMITY.print_unallocated(filename), "green", attrs=["bold"])

    # This cmd allows the user to call the load_people function
    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people """

        print(AMITY.load_people())

    # This cmd allows the user to call print_room function
    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <room_name>"""

        cprint(AMITY.print_room(args['<room_name>']), "magenta", attrs=["bold"])

    # This cmd allows the user to quit from the application
    def do_reset(self, arg):
        """Quits out of Interactive Mode."""

        AMITY.all_people = []
        AMITY.all_rooms = []
        AMITY.unallocated_office = []
        AMITY.unallocated_living_space = []
        cprint("✔ Amity has been wiped clean" , "green", attrs=["bold"])

    # This cmd allows the user to quit from the application
    def do_q(self, arg):
        """Quits out of Interactive Mode."""

        os.system('clear')
        bye = Figlet(font='roman')
        delay_print('\n\n' + \
                colored(bye.renderText('Goodbye...'), 'magenta', attrs=['bold']))
        exit()

if __name__ == '__main__':

    try:
        print(__doc__)
        ScreenOut().cmdloop()
    except KeyboardInterrupt:
        os.system('clear')
        font = Figlet(font='roman')
        delay_print('\n\n' + \
        colored(font.renderText('Goodbye...'), 'yellow', attrs=['bold']))