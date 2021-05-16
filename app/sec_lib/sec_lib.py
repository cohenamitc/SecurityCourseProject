class SecLib(object):
    @staticmethod
    def prevent_xss_encoding(to_encode: str) -> str:
        encoding_dictionary = {
            "&": "&amp",
            "<": "&lt",
            ">": "&gt",
            "\"": "&quot",
            "'": "&#x27"
        }
        for ch in encoding_dictionary:
            to_encode = to_encode.replace(ch, encoding_dictionary[ch])
        return to_encode
