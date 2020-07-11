import emoji
from string import digits
from sys import argv

class standardVariables():
    name = "J08K (Job van der Wal)"
    defaultType = "web-txt"

class toMarkdown():
    def __init__(self, filepath):
        try:
            with open(filepath, "r", encoding="utf8") as file:
                fileData = emoji.demojize(file.read().replace("\n\n", "$$"))
                fileData = fileData.split("\n")
                toRemove = list()
                self.__fileData = list()
                for message, index in zip(fileData, range(len(fileData))):
                    if message[2] not in digits and message[2]!= ":":
                        self.__fileData[index-1] += " \n%s" % str(message.split("$$"))
                        self.__fileData.append(message)
                    else:
                        message = message.split("$$")
                        for item in message:
                            if item == "":
                                message.remove("")
                        self.__fileData.append(message)
                for index in toRemove:
                    self.__fileData.pop(index)
        except:
            raise Exception("File not found: " % filepath)

    def toMarkdown(self, filepath, date, name):
        with open(filepath, "w+", encoding="utf8") as file:
            file.write("# Meeting of %s\n\n" % date)
            for line in self.__fileData:
                if len(line[0]) == 1: pass
                else: file.write(emoji.emojize("_%s_\n\n**%s**\n\n%s\n\n---\n" % (line[0], line[1].replace("Me", name), line[2])))
            file.write("# End of meeting")    
        return(True)

if __name__ == "__main__":
    args = dict()
    for argument, index in zip(argv, range(len(argv))):
        
        ## ? The name of the output file.
        ## ? Defaults to: The name of the input file, but with ".md".
        if argument.lower() == "--output": 
            args["output"] = argv[index+1]

        ## * The name of the input file. REQUIRED
        elif argument.lower() == "--input":
            args["input"] =  argv[index+1]
        
        ## ? The date of the meeting.
        ## ? Defaults to: The current date on the pc.
        elif argument.lower() == "--date":
            args["date"] = argv[index+1]
        
        ## ? The name of the "Me" user in the chat (Which is the person who copied it).
        ## ? Defaults to: standardVariables.name . 
        elif argument.lower() == "--name":
            args["name"] = argv[index+1]

        ## ? This is the type of way you are importing the chat. (client-txt, web-txt, client-rtf)
        ## ? Defaults to: standardVariables.defaultType . 
        elif argument.lower() == "--type":
            args["type"] = argv[index+1]

    if "input" in args:
        process = toMarkdown(args["input"])
        args["name"] = args["name"] if "name" in args else standardVariables.name
        args["output"] = args["output"] if "output" in args else args["input"][:-4] + ".md"
        if "date" not in args:
            from datetime import date
            args["date"] = date.today()
        if process.toMarkdown(args["output"], args["date"], args["name"]):
            print("\nOutput file: %s\n" % args["output"])
    else:
        raise Exception("No input file given!")