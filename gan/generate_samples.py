"""
Prototype-only GAN placeholder.

The supplied report describes GAN augmentation as a proposed Stage 2
enhancement and does not provide a verified GAN implementation. This module
therefore generates simple synthetic URL variants for development/testing;
it is NOT a trained GAN and must not be reported as GAN experimental results.
"""
import random

WORDS = ["login", "verify", "secure", "account", "update", "confirm"]

def generate_synthetic_urls(n=20):
    samples = []
    for _ in range(n):
        word = random.choice(WORDS)
        token = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(10))
        samples.append(f"https://secure-{word}-{token}.example.test/account")
    return samples

if __name__ == "__main__":
    for url in generate_synthetic_urls():
        print(url)
