def get_tokens(string: str) -> list[str]:
    """
    This function tokenizes user input. Separators are spaces, but "" keeps whole as one token.
    """
    tokens = []
    _string = string.replace('" ', '"')
    current_token = {"content": "", "terminal_token": " "}
    for char in _string:
        if char == current_token["terminal_token"]:
            tokens.append(current_token["content"])
            current_token["content"] = ""
            current_token["terminal_token"] = " "
        elif char == '"':
            current_token["terminal_token"] = '"'
        else:
            current_token["content"] += char

    return tokens

if __name__ == "__main__":
    print(get_tokens('hello "jo jo jo" kkkk " lllll   llll "'))
