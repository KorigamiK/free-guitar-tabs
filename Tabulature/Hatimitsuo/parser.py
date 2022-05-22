import re

if __name__ == "__main__":

    url_regex = re.compile(r"https?:\/\/\S+\.[^()]+(?:\([^)]*\))*")
    white_space_regex = re.compile(r"(?<=\]).+(?=\(h)")

    with open("./links.txt") as file:
        for line in file.readlines():
            line = line.replace("\n", "")
            match = url_regex.search(line)
            if match:
                final = list(line)
                final.insert(match.start(), "(")
                final.insert(match.end() + 1, ")")
                final = "".join(final)
                final = white_space_regex.sub("", final)
                print(final)

            else:
                print(line)
