def chunk_text(text, chunk_size=300, overlap=50):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


sample_text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 20

chunks = chunk_text(sample_text, chunk_size=50, overlap=10)

print("Sample text length:", len(sample_text))
print("Number of chunks:", len(chunks))
print("First chunk length:", len(chunks[0]))
print("Second chunk length:", len(chunks[1]))
print("Overlap:", chunks[0][-10:] == chunks[1][:10])
