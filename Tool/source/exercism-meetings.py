from emoji import emojize, demojize
from sys import argv
import os.path
from datetime import date
import json

## TODO: Add a progress bar.

standard_name = "Job van der Wal (J08K)"

class input_parser():

    file_path = str()

    def __init__(self, file_path: str):
        if os.path.isfile(file_path):
            self.file_path = file_path
        else:
            raise Exception(f"File {file_path} does not exist in directory!")

    def rtf_parse(self):
        with open(self.file_path, "r") as file:
            file = demojize(file.read())
        file = file.split("\n")
        
        messages = list()
        for line in file:
            new_line = line.split(" (to Everyone)\\b0 : \\cf1 ")
            if len(new_line) == 2:
                new_line[0] = new_line[0][7:]
                new_line[1] = new_line[1][:-8]
                messages.append(dict(user=new_line[0], time=new_line[1][:5], message=new_line[1][7:]))
        return messages

    def txt_parse(self):
        pass

    def md_parse(self):
        pass

class output_parser():
    data = list()
    date = str()

    def __init__(self, chat_data: list, date: str, username=None):
        if username != None:
            for message in len(chat_data):
                if chat_data[message]["user"] == "Me":
                    chat_data[message]["user"] = username
        self.data = chat_data
        self.date = date

    def to_markdown(self):
        pass

    def to_json(self):
        with open(self.date+".json", "w+") as file:
            json.dump(self.data, file, indent=4)

if __name__ == "__main__":
    args = dict()
    for argument, index in zip(argv, range(len(argv))):
        ## * The name of the input file. REQUIRED
        if argument.lower() == "--input":
            args["input"] =  argv[index+1]
        
        ## * The date of the meeting.
        ## * Defaults to: The current date on the pc.
        elif argument.lower() == "--date":
            args["date"] = argv[index+1]
        
        ## * The name of the "Me" user in the chat (Which is the person who copied it).
        ## * Defaults to: "Job van der Wal (J08K)" . 
        elif argument.lower() == "--name":
            args["name"] = argv[index+1]

        ## * The type of file the program should output.
        ## * Defaults to: "markdown"
        elif argument.lower() == "--output":
            args["output"] = argv[index+1]

    chat = {}

    if "input" in args:
        if args["input"][-4:] == ".txt":
            chat = input_parser(args["input"]).txt_parse()
        elif args["input"][-4:] == ".rtf":
            chat = input_parser(args["input"]).rtf_parse()
        else:
            raise Exception("Not a valid file format (yet)!")

    if chat != {}:

        ## * Checks if date has been entered, else defaults to today's date.
        args["date"] = date.today() if "date" not in args else args["date"]

        ## * Checks if name has been entered ("which will replace the username "me" in the chat), else defaults to `standard_name`
        args["name"] = standard_name if "name" not in args else args["name"]

        ## * 
        container = output_parser(chat, args["date"], username=args["name"] if args["input"][-4:] == ".txt" else None)

        if "output" not in args or args["output"].lower() == "md" or args["output"].lower() == "markdown":
            container.to_markdown()
        elif args["output"].lower() == "json":
            container.to_json()

    else:
        ## TODO Make UI, if you just want to run the program, without arguments.
        raise Exception("No input file was given!")