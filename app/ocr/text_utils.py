# normalization

def normalize(s: str) -> str:
    # return s.lower().strip()
    return (
        s.lower()
        .replace(" ", "")
        .replace("\u00a0", "")
        .strip()
    )


def extract_text_after_heading(full_text: str, heading: str) -> str:
    lines = full_text.splitlines()

    # normalized_heading = normalize(heading)
    capture = False
    extracted = []

    for line in lines:
        if capture:
            if line.isupper():  #  opt: next-heading detection
                break
            extracted.append(line)

        if heading.lower().strip() in line.lower().strip():
            capture = True
        # if normalized_heading in normalize(line):
        #     capture = True

    return "\n".join(extracted).strip()