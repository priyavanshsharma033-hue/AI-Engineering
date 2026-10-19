
from rag_api import chunk_text

sample_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 20

chunks = chunk_text(sample_text, chunk_size=50, overlap=10)

print("Number of chunks:", len(chunks))
print("First chunk length:", len(chunks[0]))
print("Second chunk length:", len(chunks[1]))
print("Overlap:", chunks[0][-10:] == chunks[1][:10])

print("\nTesting short text:")
print(chunk_text("...", chunk_size=50, overlap=10))
