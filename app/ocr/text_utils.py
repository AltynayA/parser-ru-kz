# normalization

def normalize(s: str) -> str:
    return (
        s.lower()
        .replace(" ", "")
        .replace("\u00a0", "")
        .strip()
    )


def extract_text_after_heading(full_text: str, heading: str) -> str:
    lines = full_text.splitlines()
    heading_norm = normalize(heading)

    capture = False
    extracted = []

    for line in lines:
        line_norm = normalize(line)

        # Start capturing after heading
        if heading_norm in line_norm:
            capture = True
            continue

        # Stop if next heading (ALL CAPS heuristic)
        if capture and line.strip().isupper() and len(line.strip()) > 5:
            break

        if capture:
            extracted.append(line)

    return "\n".join(extracted).strip()
