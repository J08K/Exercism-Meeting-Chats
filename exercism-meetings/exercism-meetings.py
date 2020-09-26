from emoji import emojize, demojize
from sys import argv, stdout
import os.path
from datetime import date
import json

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
        
        progress = progress_bar(len(file), "RTF Parsing", "Messages")

        messages = list()
        for line in file:
            new_line = line.split(" (to Everyone)\\b0 : \\cf1 ")
            if len(new_line) == 2:
                new_line[0] = new_line[0][7:]
                new_line[1] = new_line[1][:-8]
                messages.append(dict(user=new_line[0], time=new_line[1][:5], message=new_line[1][7:]))
            progress.add_progress(1)
        progress.end_progress()
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
        progress = progress_bar(len(self.data)+2, "Parse to Markdown", "Messages")
        to_write = f"# Meeting of {str(self.date)}\n\n"
        progress.add_progress(1)
        for message in self.data:
            to_write += "## _%s:_ **%s**\n\n%s\n\n---\n\n"%(message["time"], message["user"], message["message"])
            progress.add_progress(1)
        progress.add_progress(1)
        to_write += "# End of meeting\n"
        with open(f"{self.date}.md", "w+", encoding="utf8") as file:
            file.write(emojize(to_write))
        progress.end_progress()

    def to_json(self):
        chat = dict(date=str(self.date), chat=self.data)
        with open(str(self.date)+".json", "w+") as file:
            to_dump = json.dumps(chat, indent=1)
            file.write(emojize(to_dump))

class progress_bar():

    progress = 0
    end = int()
    title = str()
    title_color = "\u001b[31m"
    reset_color = "\u001b[0m"
    done_color = "\u001b[32m"
    attribute_color = "\u001b[30;1m"
    size = int()
    attribute = str() ## ? What to show after the last bit. e.g. ""

    def __init__(self, end: int, title: str, attribute: str, size=40):
        self.end = end
        self.title = title
        self.size = size
        self.attribute = attribute
        length = self.size+len(str(self.end))+len(self.attribute)+9
        stdout.write(f"{self.title_color}[{self.title}]{self.reset_color}: 0% ["+"-"*self.size+f"] 0/{self.end} {self.attribute_color}{self.attribute}{self.reset_color}"+chr(8)*length)
        stdout.flush()

    def add_progress(self, to_add: int):
        self.progress += to_add
        length = self.size+len(str(round(self.progress/self.end*100)))+len(str(self.progress))+len(str(self.end))+len(self.attribute)+7
        bar = "["+"#"*(self.percent()-(1 if self.percent(True) == 0 else 0))+("/" if self.percent(True) != 0 else "")
        bar = bar+"-"*(self.size+1-len(bar))+"]"        
        stdout.write(f"{round(self.progress/self.end*100)}% "+bar+f" {self.progress}/{self.end} {self.attribute_color}{self.attribute}{self.reset_color}"+chr(8)*length)
        stdout.flush()

    def percent(self, selector=False):
        if not selector:
            return round(self.progress/self.end*self.size)
        else:
            return round(self.progress/self.end*(self.size))%2

    def end_progress(self):
        stdout.write(f"100% {self.done_color}["+"#"*self.size+f"]{self.reset_color} {self.progress}/{self.end} {self.attribute_color}{self.attribute}{self.reset_color}")
        stdout.flush()

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

    print("") ## * Creates an empty line on purpose.

    if chat != {}:

        ## * Checks if date has been entered, else defaults to today's date.
        args["date"] = date.today() if "date" not in args else args["date"]

        ## * Checks if name has been entered ("which will replace the username "me" in the chat), else defaults to `standard_name`
        args["name"] = standard_name if "name" not in args else args["name"]

        container = output_parser(chat, args["date"], username=args["name"] if args["input"][-4:] == ".txt" else None)

        if "output" not in args or args["output"].lower() == "md" or args["output"].lower() == "markdown":
            container.to_markdown()
        elif args["output"].lower() == "json":
            container.to_json()

    else:
        ## TODO Make UI, if you just want to run the program, without arguments.
        raise Exception("No input file was given!")