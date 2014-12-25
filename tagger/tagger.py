from collections import OrderedDict
import json
import socket
import struct
import sys

def prepare_data(filename):
    with open(filename, "rb") as f:
        data = f.read()

    header = struct.pack('>i', len(data))

    return header + data

def query_server(data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9000))
    s.sendall(data)

    chunks = []
    while True:
        part = s.recv(0x1000)
        if len(part) <= 0:
            break

        chunks.append(part)

    s.close()

    return "".join(chunks)

POS_FORMAT = OrderedDict([
    (1, "word_index"),
    (2, "word_form"),
    (3, "lemma"),
    (4, "pos_tag"),
    # (5, "pos_tag_exact"),
    (6, "morph_feat"),
    # (7, "head"),
    # (8, "dep_type"),
    # (9, "chunk_tag"),
    # (10, "chunk_type"),
    # (11, "ne_tag"),
    # (12, "ne_type"),
    (13, "token_id"),
])

def parse_word_for_pos(line):
    values = line.split("\t")

    # "_" is used for no value
    values = [v if v != "_" else None for v in values]

    # Skip values that doesn't make sense for POS tagging
    values = [v for i, v in enumerate(values) if i + 1 in POS_FORMAT]

    # Create a dictionary for each word
    word_with_feat = OrderedDict(zip(POS_FORMAT.values(), values))

    return word_with_feat

NE_FORMAT = OrderedDict([
    # (1, "word_index"),
    (2, "word_form"),
    (3, "lemma"),
    # (4, "pos_tag"),
    # (5, "pos_tag_exact"),
    # (6, "morph_feat"),
    # (7, "head"),
    # (8, "dep_type"),
    # (9, "chunk_tag"),
    # (10, "chunk_type"),
    (11, "ne_tag"),
    (12, "ne_type"),
    (13, "token_id"),
])

def parse_word_for_ne(line):
    values = line.split("\t")

    # Skip values that doesn't make sense for named entities
    values = [v for i, v in enumerate(values) if i + 1 in NE_FORMAT]

    # Create a dictionary for each word
    word_with_feat = OrderedDict(zip(NE_FORMAT.values(), values))

    return word_with_feat

def build_composite_entity(parts):
    return OrderedDict([
        ("word_form", " ".join([word["word_form"] for word in parts])),
        ("lemma", " ".join([word["lemma"] for word in parts])),
        ("ne_type", parts[0]["ne_type"]),
        ("token_ids", [word["token_id"] for word in parts]),
    ])

class TokenBuffer(object):
    def __init__(self):
        self.tokens = []
        self.buffer = []

    def push(self, token):
        self.buffer.append(token)

    def flush(self):
        if self.buffer:
            self.tokens.append(self.buffer)
            self.buffer = []

    def get(self):
        return self.tokens

def parse_response(response):
    sentence_buffer = TokenBuffer()
    entity_buffer = TokenBuffer()

    for line in response.splitlines():
        # Every sentence ends with an empty line
        if not line:
            sentence_buffer.flush()
            entity_buffer.flush()
            continue

        # Accumulate list of words with POS tag
        word_with_pos_feat = parse_word_for_pos(line)
        sentence_buffer.push(word_with_pos_feat)

        # Accumulate list of entites
        word_with_ne_feat = parse_word_for_ne(line)
        if word_with_ne_feat["ne_tag"] in ["B", "I"]:
            entity_buffer.push(word_with_ne_feat)
        else:
            entity_buffer.flush()

    sentences = sentence_buffer.get()
    entities = entity_buffer.get()
    entities = [build_composite_entity(tokens) for tokens in entities]
    return sentences, entities

def main(filename):
    data = prepare_data(filename)
    response = query_server(data)
    sentences, entities = parse_response(response)

    print json.dumps(OrderedDict([
        ("sentences", sentences),
        ("entities", entities),
    ]), indent=4)

if __name__ == "__main__":
    assert len(sys.argv) > 1, "Missing filename as parameter"

    main(sys.argv[1])
